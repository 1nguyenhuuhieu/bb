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
    mess = ""

    if request.method == "POST":
        pwd = request.POST['pwd']
        user = authenticate(username='tea', password=pwd)
        if user is not None:
            login(request, user)
            return redirect('doctruyen')

            
        
    context = {
        'mess': mess
    }
    return render(request, 'index.html', context)

@login_required(login_url='index')
def doctruyen(request):
    if request.method == "POST" and 'send' in request.POST:
        form = ChatForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('doctruyen')
    else:
        form = ChatForm()
    mess = Chat.objects.latest('created')
    context = {
        'mess': mess,
        'form': form

    }

    return render(request, 'doctruyen.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')