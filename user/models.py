from django.db import models
from django.contrib.auth.admin import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name='昵称')

    def get_nickname(self):
        if Profile.objects.filter(user=self).exists():
            return Profile.objects.get(user=self).nickname
        else:
            return '未填写昵称'

    def get_nickname_and_username(self):
        if Profile.objects.filter(user=self).exists():
            return self.username + '(' + Profile.objects.get(user=self).nickname + ')'
        else:
            return self.username

    def get_nickname_or_username(self):
        if Profile.objects.filter(user=self).exists():
            return Profile.objects.get(user=self).nickname
        else:
            return self.username

    User.get_nickname = get_nickname  # 此处不能有（）
    User.get_nickname_and_username = get_nickname_and_username
    User.get_nickname_or_username = get_nickname_or_username

