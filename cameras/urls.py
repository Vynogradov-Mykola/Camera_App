from django.urls import path
from . import views

urlpatterns = [
    path('', views.camera_list, name='camera_list'),
    path('stream/', views.camera_stream, name='camera_stream'),
    path('video_feed/', views.video_feed, name='video_feed'),
]
