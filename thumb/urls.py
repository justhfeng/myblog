from django.urls import path
from .views import thumb_up

urlpatterns = [
    path('', thumb_up, name='thumb_up')
]
