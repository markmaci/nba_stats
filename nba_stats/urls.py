from django.urls import path
from . import views

app_name = 'nba_stats'

urlpatterns = [
    path('', views.home, name='home'),
    path('player/<int:player_id>/', views.player_details, name='player_details'),
]