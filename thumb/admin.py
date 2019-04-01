from django.contrib import admin
from .models import ThumbUpRecord


# Register your models here.
@admin.register(ThumbUpRecord)
class ThumbAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'user']
