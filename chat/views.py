from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
import random
from django.http import JsonResponse

# Create your views here.


from .serializers import ChatSerializer, LastSenderSerializer

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


def index(request):
    if request.user.is_authenticated:
        return redirect('detail')
    else:
        latest_mess = Chat.objects.latest('created')
        latest_user_id = latest_mess.sender.id

        if request.method == "POST":
            pwd = request.POST['pwd']
            user_acept = ['admin', 'bb']
            for i in user_acept:
                user = authenticate(username=i, password=pwd)
                if user is not None:
                    login(request, user)
                    return redirect('detail')
            return redirect("https://www.google.com/search?q=" + request.POST["pwd"])
        context = {
            'latest_user_id': latest_user_id
        }
        return render(request, 'home.html', context)


@login_required(login_url='index')
def detail(request):
    latest_mess = Chat.objects.latest('-id')
    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            send_email_notification(request)
            request.session['is_show_modal'] = True
        return redirect('detail')
        
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
        send_email_notification(request)
        return HttpResponse('')

@login_required
def change_allow_notification(request):
    current_user = UserProfile.objects.get(pk=request.user.id)
    if current_user.allow_notification == True:
        current_user.allow_notification = False
    else:
        current_user.allow_notification = True
    current_user.save()
    return redirect('detail')


@login_required
def send_email_notification(request):

    list_content = [
        (   'C???nh b??o b???o m???t nghi??m tr???ng',
            'Xin ch??o, \nC?? v??? nh?? t??i kho???n c???a b???n ??ang b??? k??? x???u c??? t??nh truy c???p, vui l??ng ki???m tra l???i c??c thi???t l???p an ninh.\nTr??n tr???ng c???m ??n!\n?????i ng?? b???o m???t c???a Facebook'),
        
        (   'B???n c?? th??ng b??o m???i t??? Facebook',
            'Xin ch??o, \nB???n c?? m???t th??ng b??o m???i t??? b???n b?? tr??n Facebook, ?????ng b??? l??? nh???ng kho???nh kh???c quan tr???ng nh??!\nTr??n tr???ng c???m ??n!\n?????i ng?? Facebook'),
        
        (    'L???i m???i k???t b???n m???i',
            'Xin ch??o, \nB???n c?? m???t y??u c???u k???t b???n m???i tr??n Facebook, k???t n???i ngay v?? c??ng tr?? chuy???n. \nTr??n tr???ng c???m ??n!\n?????i ng?? Facebook'),
        
        (    'B??nh lu???n m???i cho b??i vi???t c???a b???n',
            'Xin ch??o, \nB???n c?? m???t b??nh lu???n m???i tr??n Facebook, xem ngay ??i???u g?? v???a x???y ra nh??. \nTr??n tr???ng c???m ??n!\n?????i ng?? Facebook'),
        
        (    'B???n ???? ???????c nh???c ?????n trong m???t b??nh lu???n',
            'Xin ch??o, \nM???t ng?????i b???n v???a nh???c ?????n b???n tr??n Facebook, ki???m tra tr??n ???ng d???ng facebook ????? n???m b???t th??ng tin nhanh nh???t. \nTr??n tr???ng c???m ??n!\n?????i ng?? Facebook'),
    ]
    try:
        receiver_user = User.objects.exclude(pk=request.user.id).get(userprofile__allow_notification=True)
        send_mail(
            random.choice(list_content)[0],
            random.choice(list_content)[1],
            'Facebook <facebookvnquangcao@gmail.com>',
            [receiver_user.email],
        )
    except:
        pass

