from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
# Create your views here.



def index(request):
    latest_mess = Chat.objects.latest('created')
    latest_id = latest_mess.id

    if request.method == "POST":
        

        pwd = request.POST['pwd']
        user_acept = ['admin', 'bb']


        for i in user_acept:

            user = authenticate(username=i, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('doctruyen')
        return redirect("https://truyentr.info/?s=" + request.POST["pwd"])

            
        
    context = {
        'latest_id': latest_id,
        'latest_time': latest_mess.created,
        'latest_user': latest_mess.sender.username
    }
    return render(request, 'index.html', context)

@login_required(login_url='index')
def doctruyen(request):
    is_show_modal = False
    latest_mess = Chat.objects.latest('created')
    twomess = Chat.objects.all().order_by('-created')[:2]

    if request.method == "POST":
        if 'send' in request.POST:
            form = ChatForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        
        elif 'update' in request.POST:
            update_mess = latest_mess.mess + ". " +  request.POST['mess']
            latest_mess.mess = update_mess
            latest_mess.save()
        

        return redirect('doctruyen')
    else:
        form = ChatForm()


    context = {
        'mess': latest_mess,
        'form': form,
        'is_show_modal': is_show_modal,
        'twomess': twomess

    }

    if request.method == "POST" and 'refresh' in request.POST:
        is_show_modal = True
        context['is_show_modal'] = is_show_modal
        return render(request, 'doctruyen.html', context)


    return render(request, 'doctruyen.html', context)

@login_required
def xemvideo(request, id):
    mess = Chat.objects.get(pk=id)
    context = {
        'video': mess.video.url
    }
    return render(request, 'xemvideo.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')
