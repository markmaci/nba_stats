from django.urls import path
from . import views
from .views import signup, player_details, add_to_roster, user_roster, remove_from_roster, custom_logout
from django.contrib.auth import views as auth_views

app_name = 'nba_stats'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='nba_stats/login.html',
        redirect_authenticated_user=True,
        next_page='nba_stats:roster'  # Redirects to the roster page after login
    ), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('player/<int:player_id>/', views.player_details, name='player_details'),
    path('add_to_roster/<int:player_id>/', add_to_roster, name='add_to_roster'),
    path('remove_from_roster/<int:player_id>/', remove_from_roster, name='remove_from_roster'),
    path('roster/', user_roster, name='roster'),
]