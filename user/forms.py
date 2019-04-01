from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名或邮箱', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            if not User.objects.filter(email=username).exists():
                raise forms.ValidationError('用户名或密码错误，请重新输入')
            else:
                username = User.objects.get(email=username).username
                user = auth.authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError('用户名或密码错误，请重新输入')
        self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=3, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'}
    ))
    email = forms.CharField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
    ))
    vc_received = forms.CharField(label='验证码', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入验证码'}
    ))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}
    ))
    password_again = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}
    ))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')
        return username

    # 导入request
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')  # 修改成request
        super(RegForm, self).__init__(*args, **kwargs)

    # ！！！！如下这些都是在用户提交的时候进行判断，而非发送验证码的时候判断
    # 判断输入的邮箱地址是否为空，以及邮箱是否已经被绑定
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if email == '':
            raise forms.ValidationError('邮箱为空，请重新输入！')
        # 判断邮箱是否已注册
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已经被注册，请重新输入！')  # 为什么不在发送验证码的时候进行判断
        email_send = self.request.session.get('email_send_reg', '')  # 有可能未发送邮箱
        vc_send = self.request.session.get('vc_send_reg', '')
        # 在验证码已发送的前提下，判断邮箱是否一致
        if email != email_send and vc_send != '':
            raise forms.ValidationError('邮箱不匹配，请重新发送验证码！')
        return email

    def clean_vc_received(self):
        vc_received = self.cleaned_data['vc_received'].strip()
        # 判断验证码是否为空
        if vc_received == '':
            raise forms.ValidationError('验证码为空，请重新输入！')
        # 判断是否已发送验证码
        vc_send = self.request.session.get('vc_send_reg', '')
        if vc_send == '':
            raise forms.ValidationError('请先点击发送验证码')
        # 判断验证码是否一致
        if vc_received != vc_send:
            raise forms.ValidationError('验证码错误，请重新输入')
        return vc_received

    def clean_password_again(self):  # 为什么非得是clean_password_again
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致，请重新输入！')  # form怎么知道在哪里显示


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}))

    # 判断用户是否登陆
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证用户登陆情况
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登陆')
        return self.cleaned_data

    # 昵称不能为空
    def clean_nickname_new(self):
        nickname_new = self.cleaned_data['nickname_new']
        if nickname_new.strip() == '':
            raise forms.ValidationError('昵称不能为空')
        return nickname_new


class ChangeEmailForm(forms.Form):
    email = forms.CharField(
        label='新的邮箱地址',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入新的邮箱地址'})
    )
    vc_received = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入收到的验证码'})
    )  # 用户输入的验证码

    # 导入request
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')  # 修改成request
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    # ！！！！如下这些都是在用户提交的时候进行判断，而非发送验证码的时候判断
    # 判断输入的邮箱地址是否为空，以及邮箱是否已经被绑定
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if email == '':
            raise forms.ValidationError('邮箱为空，请重新输入！')
        # 判断邮箱是否已注册
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已经被注册，请重新输入！')  # 为什么不在发送验证码的时候进行判断
        email_send = self.request.session.get('email_send_change_email', '')  # 有可能未发送邮箱
        vc_send = self.request.session.get('vc_send_change_email', '')
        # 在验证码已发送的前提下，判断邮箱是否一致
        if email != email_send and vc_send != '':
            raise forms.ValidationError('邮箱不匹配')
        return email

    def clean_vc_received(self):
        vc_received = self.cleaned_data['vc_received'].strip()
        # 判断验证码是否为空
        if vc_received == '':
            raise forms.ValidationError('验证码为空，请重新输入！')
        # 判断是否已发送验证码
        vc_send = self.request.session.get('vc_send_change_email', '')
        if vc_send == '':
            raise forms.ValidationError('请先点击发送验证码')
        # 判断验证码是否一致
        if vc_received != vc_send:
            raise forms.ValidationError('验证码错误，请重新输入')
        return vc_received

    def clean(self):
        # 验证用户登陆情况
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登陆')
        # email_received = self.cleaned_data['email_received']  # !!!!报KeyError，有可能去要将判断放置到clean_field当中
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'请输入旧密码'}
    ))
    new_password = forms.CharField(label='新密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入新密码'}
    ))
    new_password_again = forms.CharField(label='确认密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请再次输入新密码'}
    ))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断旧密码是否准确
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码错误，请重新输入')
        # 判断两次输入的密码是否一致
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入密码不一致，请重新输入！')
        return self.cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.CharField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '请输入你的邮箱'}
    ))
    vc_received = forms.CharField(label='验证码', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入你的验证码'}
    ))
    new_password = forms.CharField(label='新密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入新密码'}
    ))
    new_password_again = forms.CharField(label='确认密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请再次输入新密码'}
    ))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')  # 修改成request
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    # 判断邮箱和验证码是否一致，邮箱是否有对应用户
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if email == '':
            raise forms.ValidationError('邮箱为空，请重新输入！')
        email_send = self.request.session.get('email_send_reset_password', '')  # 有可能未发送邮箱
        vc_send = self.request.session.get('vc_send_reset_password', '')
        # 在验证码已发送的前提下，判断邮箱是否一致
        if email != email_send and vc_send != '':
            raise forms.ValidationError('邮箱不匹配')
        return email

    def clean_vc_received(self):
        vc_received = self.cleaned_data['vc_received'].strip()
        # 判断验证码是否为空
        if vc_received == '':
            raise forms.ValidationError('验证码为空，请重新输入！')
        # 判断是否已发送验证码
        vc_send = self.request.session.get('vc_send_reset_password', '')
        if vc_send == '':
            raise forms.ValidationError('请先点击发送验证码')
        # 判断验证码是否一致
        if vc_received != vc_send:
            raise forms.ValidationError('验证码错误，请重新输入')
        return vc_received

    # 验证两次输入的新密码是否一致
    def clean(self):
        email = self.cleaned_data['email']
        # 判断邮箱是否已注册
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱未注册，请重新输入！')
        else:
            self.cleaned_data['user'] = User.objects.get(email=email)
            # 判断两次输入的密码是否一致
            new_password = self.cleaned_data['new_password']
            new_password_again = self.cleaned_data['new_password_again']
            if new_password != new_password_again or new_password == '':
                raise forms.ValidationError('两次输入密码不一致，请重新输入！')
        return self.cleaned_data

