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
        (   'Cảnh báo bảo mật nghiêm trọng',
            'Xin chào, \nCó vẻ như tài khoản của bạn đang bị kẻ xấu cố tình truy cập, vui lòng kiểm tra lại các thiết lập an ninh.\nTrân trọng cảm ơn!\nĐội ngũ bảo mật của Facebook'),
        
        (   'Bạn có thông báo mới từ Facebook',
            'Xin chào, \nBạn có một thông báo mới từ bạn bè trên Facebook, đừng bỏ lỡ những khoảnh khắc quan trọng nhé!\nTrân trọng cảm ơn!\nĐội ngũ Facebook'),
        
        (    'Lời mời kết bạn mới',
            'Xin chào, \nBạn có một yêu cầu kết bạn mới trên Facebook, kết nối ngay và cùng trò chuyện. \nTrân trọng cảm ơn!\nĐội ngũ Facebook'),
        
        (    'Bình luận mới cho bài viết của bạn',
            'Xin chào, \nBạn có một bình luận mới trên Facebook, xem ngay điều gì vừa xảy ra nhé. \nTrân trọng cảm ơn!\nĐội ngũ Facebook'),
        
        (    'Bạn đã được nhắc đến trong một bình luận',
            'Xin chào, \nHình như bạn bè vừa nhắc đến bạn trên Facebook, kiểm tra trên ứng dụng facebook để nắm bắt thông tin nhanh nhất. \nTrân trọng cảm ơn!\nĐội ngũ Facebook'),
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

