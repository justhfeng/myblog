from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


# 新建一个ProfileInline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# 然后将ProfileInline放入到UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ['username', 'nickname', 'email', 'is_active', 'is_superuser', 'is_staff']

    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'


# 重新注册UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# 注册ProfileAdmin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname']

