from django.urls import path
from . import views


urlpatterns = [
    path('artists/', views.artist_list_or_create),
    path('artists/<int:artist_pk>/', views.artist_detail_or_update_or_delete),

    path('albums/', views.album_list_or_create),
    path('albums/<int:album_pk>/', views.album_detail_or_update_or_delete),

    path('top_tracks/', views.top_track_list),
    path('albums/<int:album_pk>/tracks/', views.create_track),
    path('albums/<int:album_pk>/tracks/<int:track_pk>/', views.track_detail_or_update_or_delete),
]


