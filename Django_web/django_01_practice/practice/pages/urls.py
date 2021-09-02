from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('lotto/', views.lotto, name='lotto'),
]
