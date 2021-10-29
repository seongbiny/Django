from django.urls import path
from . import views

urlpatterns = [
    path('music/', views.music_list),
    path('music/<int:music_pk>/', views.music_detail),
    path('artists/', views.artist_list),
    path('artists/<int:artist_pk>/', views.artist_detail),
    path('artists/<int:artist_pk>/music/', views.artist_music),
]