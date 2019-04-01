from . import views
from django.urls import path

urlpatterns = [
    path('add_comment/', views.add_comment, name='add_comment')  # 为什么这个地方是add_comment,确保不冲突就行
]

# urlpatterns = [
#     path('add_comment/<int:blog_id>', views.blog_detail, name='add_comment')  # 为什么这个地方是add_comment,确保不冲突就行
# ]