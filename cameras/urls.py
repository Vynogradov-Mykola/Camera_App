from django.urls import path
from . import views

urlpatterns = [
    path('', views.camera_list, name='camera_list'),
    path('stream/', views.camera_stream, name='camera_stream'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('motion_events/', views.motion_events_view, name='motion_events'),
    path('series/', views.series_list_view, name='series_list'),
    path('series/add/', views.series_add_view, name='series_add'),
]

