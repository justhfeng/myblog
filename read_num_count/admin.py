from django.contrib import admin
from .models import ReadNum, ReadNumDetail


# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['read_num', 'content_object', 'object_id']  # 外面不能有,


@admin.register(ReadNumDetail)
class ReadNumAggAdmin(admin.ModelAdmin):
    list_display = ['read_num', 'content_object', 'object_id', 'read_date']  # 外面不能有,
