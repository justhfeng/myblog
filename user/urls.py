from django.urls import path
from . import views

urlpatterns = [
    path('login_for_modal_form/', views.login_for_modal_form, name='login_for_modal_form'),
    path('login/', views.login2, name='login'),  # 記得從views導入對應方法
    path('register/', views.register, name='register'),  # 注册网页
    path('logout/', views.logout, name='logout'),  # 退出
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('change_email/', views.change_email, name='change_email'),
    path('send_vc/', views.send_vc, name='send_vc'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
]