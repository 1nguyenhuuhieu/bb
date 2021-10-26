from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.



def index(request):
    latest_mess = Chat.objects.latest('created')
    latest_id = latest_mess.id

    if request.method == "POST":
        pwd = request.POST['pwd']
        user = authenticate(username='tea', password=pwd)
        if user is not None:
            login(request, user)
            return redirect('doctruyen')

            
        
    context = {
        'latest_id': latest_id
    }
    return render(request, 'index.html', context)

@login_required(login_url='index')
def doctruyen(request):
    is_show_modal = False
    latest_mess = Chat.objects.latest('created')

    if request.method == "POST":
        if 'send' in request.POST:
            form = ChatForm(request.POST)
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
        'is_show_modal': is_show_modal

    }

    if request.method == "POST" and 'refresh' in request.POST:
        is_show_modal = True
        context['is_show_modal'] = is_show_modal
        return render(request, 'doctruyen.html', context)


    return render(request, 'doctruyen.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')