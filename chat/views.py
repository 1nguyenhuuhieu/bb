from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
# Create your views here.
from pathlib import Path

from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ChatSerializer, LastSenderSerializer, UserSerializer

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


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
        return redirect("https://www.google.com/search?q=" + request.POST["pwd"])
    context = {
        'latest_user_id': latest_user_id
    }
    return render(request, 'home.html', context)



@login_required(login_url='index')
def doctruyen(request):
    latest_mess = Chat.objects.latest('-id')
    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['is_show_modal'] = True
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

    }

    return render(request, 'detail.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')


@csrf_exempt
@login_required
def chat_list(request):
    if request.method == "GET":
        chats = Chat.objects.all().order_by('-id')[:2]
        serializer = ChatSerializer(chats, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def last_sender(request):
    if request.method == "GET":
        sender = Chat.objects.latest('id')
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