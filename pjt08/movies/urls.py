from django.urls import path
from . import views


urlpatterns = [
    path('actors/', views.actor_list_or_create),
    path('actors/<int:actor_pk>/', views.actor_detail_or_update_or_delete),

    path('movies/', views.movie_list_or_create),
    path('movies/<int:movie_pk>/', views.movie_detail_or_update_or_delete),

    path('top_reviews/', views.top_review_list),
    path('movies/<int:movie_pk>/reviews/', views.create_review),
    path('movies/<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail_or_update_or_delete),
]


