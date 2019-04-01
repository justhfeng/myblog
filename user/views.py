import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from .forms import LoginForm, RegForm, ChangeNicknameForm, ChangeEmailForm, ChangePasswordForm, ResetPasswordForm
from .models import Profile


def login_for_modal_form(request):
    login_form = LoginForm(request.POST)
    data = dict()
    if login_form.is_valid():
        data['status'] = 'SUCCESS'
        user = login_form.cleaned_data['user']
        auth.login(request, user)
    else:
        data['status'] = 'FAIL'
    return JsonResponse(data)


# 登陆验证
def login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(request, username=username, password=password)
        referer = request.META.get('HTTP_REFERER', reverse('home'))
        if user is not None:
            auth.login(request, user)
            return redirect(referer)
        else:
            return render(request, 'error.html', {'message': '密码错误，无法登陆！', 'redirect_to': referer})


# login和login2的区别在于login2的登陆方法是利用Django Form
def login2(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # 未将验证放入form当中
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # user = auth.authenticate(request, username=username, password=password)
            # if user is not None:
            #     print(request.GET.get('from'))
            #     auth.login(request, user)
            #     return redirect(request.GET.get('from'), reverse('home'))
            # else:
            #     # return render(request, 'error.html', {'message': '密码错误，无法登陆！', 'redirect_to': referer})
            #     form.add_error(None, '用户名或密码错误，请重新登陆！')
            user = form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('home'))
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def user_info(request):
    return render(request, 'user/user_info.html')


def logout(request):
    if not request.user.is_authenticated:  # 若用户未登陆，重新跳转到home界面
        return redirect(reverse('home'))
    auth.logout(request)
    return redirect(request.GET.get('from'), reverse('home'))


def register(request):
    redirect_to = request.GET.get('from', reverse('home'))
    # 若用户已经登陆，则跳转到其他界面
    if request.user.is_authenticated:
        return redirect(redirect_to)
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        print(reg_form.is_valid())
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 注册用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['email_send_reg']
            del request.session['vc_send_reg']
            del request.session['send_time']
            # 用户登陆
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(redirect_to)
    else:
        reg_form = RegForm()
    context = dict()  # 这个需要放在最外侧，否则错误提示出不来
    context['form'] = reg_form
    context['page_title'] = '用户注册'
    context['form_title'] = '用户注册'
    context['submit_text'] = '提交'
    context['return_back'] = redirect_to
    return render(request, 'user/reg.html', context)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if not request.user.is_authenticated:
        return redirect(redirect_to)

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
        context = dict()
        context['form'] = form
        context['page_title'] = '修改昵称'
        context['form_title'] = '修改昵称'
        context['submit_text'] = '提交'
        context['return_back'] = redirect_to
        return render(request, 'form.html', context)


def change_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    # 判断用户是否登陆
    if not request.user.is_authenticated:
        return redirect(redirect_to)

    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            # 绑定邮箱
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['email_send_change_email']
            del request.session['vc_send_change_email']
            del request.session['send_time']
            return redirect(redirect_to)
    else:
        form = ChangeEmailForm()
    context = dict()
    context['form'] = form
    context['page_title'] = '修改邮箱地址'
    context['form_title'] = '修改邮箱地址'
    context['submit_text'] = '提交'
    context['return_back'] = redirect_to
    return render(request, 'user/change_email.html', context)


def send_vc(request):
    email = request.GET.get('email')
    vc_name = request.GET.get('vc_name')  # 为了保证send_vc能够被重复调用，且保证session不混用，选择传入对应名称
    email_name = request.GET.get('email_name')
    data = dict()
    send_vc_not_registered = True if request.GET.get('send_vc_not_registered') == 'True' else False
    email_check = User.objects.filter(email=email).exists()
    if email_check ^ send_vc_not_registered and email != '':  # 修改邮箱，只有在邮箱未注册时才发送代码；修改密码，只有在邮箱已注册时才发送代码
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        if now - int(request.session.get('send_time', 0)) < 30:  # 存在一个问题，发送过快
            data['status'] = 'FAIL'
            data['message'] = '验证码发送过快，请稍等！'
        else:
            # 保存验证码和对应的邮箱
            request.session[vc_name] = code  # 用于注册、还是用于修改邮箱
            request.session[email_name] = email
            request.session['send_time'] = now  # 每次点击都会变，因此储存起来；取数的时候没有取0
            # 发送验证码
            send_mail(
                '验证码',
                '您的验证码：%s' % code,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
            data['message'] = '邮件已发送'
    else:
        data['status'] = 'FAIL'
        if email_check:
            data['message'] = '邮箱已注册，请重新输入邮箱'
        else:
            data['message'] = '邮箱未注册，请重新输入邮箱'
    return JsonResponse(data)


def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            return redirect(reverse('login'))
    else:
        form = ChangePasswordForm()
    context = dict()
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '提交'
    context['return_back'] = redirect_to
    return render(request, 'form.html', context)


def reset_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST, request=request)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = form.cleaned_data['user']
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['email_send_reset_password']
            del request.session['vc_send_reset_password']
            del request.session['send_time']
            return redirect(reverse('login'))
    else:
        form = ResetPasswordForm()
    context = dict()
    context['form'] = form
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '提交'
    context['return_back'] = redirect_to
    return render(request, 'user/reset_password.html', context)
