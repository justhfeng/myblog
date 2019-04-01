from django.contrib import admin
from .models import Blog, BlogType


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_time', 'last_updated_time', 'get_read_time', 'is_deleted']  # 外面不能有,
    ordering = ['-id', ]


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


'''
@admin.register(ReadTime)
class ReadTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'read_time', 'blog']
'''
