from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view

from django.http import JsonResponse
# Create your views here.
from pathlib import Path




from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ChatSerializer, LastSenderSerializer, UserSerializer

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view



def index(request):
    latest_mess = Chat.objects.latest('created')
    latest_user_id = latest_mess.sender.id

    if request.method == "POST":
        pwd = request.POST['pwd']
        user_acept = ['admin', 'bb']
        for i in user_acept:
            user = authenticate(username=i, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('doctruyen')
        return redirect("https://hellobacsi.com/search/?s=" + request.POST["pwd"])
    context = {
        'latest_user_id': latest_user_id
    }
    return render(request, 'home.html', context)

@login_required(login_url='index')
def doctruyen(request):
    latest_mess = Chat.objects.latest('created')
    latest_user_id = latest_mess.sender.id
    request.session['is_access_photos'] = True
    latest_mess = Chat.objects.latest('created')
    twomess = Chat.objects.all().order_by('-created')[:2]

    if request.method == "POST":
        if 'send_image' in request.POST:
            form = ChatForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        
        return redirect('doctruyen')
    else:
        form = ChatForm()

    if 'is_show_modal' in request.session:
        is_show_modal = True
        del request.session['is_show_modal']
    else:
        is_show_modal = False
    

    context = {
        'mess': latest_mess,
        'form': form,
        'is_show_modal': is_show_modal,
        'twomess': twomess,
        'latest_user_id': latest_user_id

    }

    return render(request, 'detail.html', context)

@login_required
def xemvideo(request, id):
    mess = Chat.objects.get(pk=id)
    context = {
        'video': mess.video.url
    }
    return render(request, 'xemvideo.html', context)


@login_required
def photos(request):
    if 'is_access_photos' in request.session:
        del request.session['is_access_photos']
        images = Chat.objects.exclude(file__exact='').exclude(file__isnull=True)
        for image in images:
            image_file = Path(image.file.url)
            if image_file.is_file():
                images = images.exclude(pk=image.id)

        context = {
            'images': images
        }
        return render(request, 'photos.html', context)

    raise Http404



def logout_view(request):
    logout(request)
    return redirect('index')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
@login_required

def chat_list(request):
    if request.method == "GET":
        chats = Chat.objects.all().order_by('-created')[:2]
        serializer = ChatSerializer(chats, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def test(request):
    return render(request, 'test.html', {})

@csrf_exempt
def last_sender(request):
    if request.method == "GET":
        sender = Chat.objects.latest('created')
        serializer = LastSenderSerializer(sender, many=False)
        return JsonResponse(serializer.data, safe=False)

@login_required
@csrf_exempt
def ajax_chat(request):
    if request.method == 'POST':
        mess = request.POST['mess']
        sender = request.user
        new_chat = Chat(
            mess = mess,
            sender = sender
        )
        new_chat.save()
        return HttpResponse('')