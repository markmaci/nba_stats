"""
File: views.py
Author: Mark Maci, markmaci@bu.edu, 12/10/2024
Description: This module defines views to handle rendering and processing of the NBA stats application pages.
It includes:
- The home page view, which provides a search form for players.
- A search view for listing found players.
- A detailed player page view, showing career totals and seasonal breakdowns.
"""

from nba_api.stats.endpoints import playercareerstats
from django.shortcuts import render, redirect
from .forms import PlayerSearchForm, StatsDropdownForm
from nba_api.stats.static import players
from .utils import get_player_name_and_image
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Roster, UserProfile
from django.shortcuts import get_object_or_404

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                favorite_team=form.cleaned_data.get('favorite_team', '')
            )
            # Log the user in
            login(request, user)
            return redirect('nba_stats:home')
    else:
        form = SignupForm()

    return render(request, 'nba_stats/signup.html', {'form': form})

def custom_logout(request):
    logout(request)  # Logs the user out
    return redirect('nba_stats:home')  # Redirect to the home page

def home(request):
    """
    Render the home page with a player search form. When a player name is submitted via POST,
    the first matching player's ID is used to redirect to that player's details page.
    """
    if request.method == 'POST':
        form = PlayerSearchForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['player_name'].title()
            player_info = players.find_players_by_full_name(player_name)

            if player_info:
                # Redirect to the first found player's details page
                player_id = player_info[0]['id']
                return redirect('nba_stats:player_details', player_id=player_id)
            else:
                # No players found, re-render form with error message
                form = PlayerSearchForm()
                return render(request, 'nba_stats/home.html', {'form': form, 'error': 'No players found.'})
    else:
        form = PlayerSearchForm()

    return render(request, 'nba_stats/home.html', {'form': form})


def search_player(request):
    """
    Display and process a player search form. If a valid player name is posted, display a list
    of matching players. Otherwise, show an error or re-render the search form.
    """
    if request.method == 'POST':
        form = PlayerSearchForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['player_name'].title()
            player_info = players.find_players_by_full_name(player_name)

            # Render a list of players if found, otherwise show an error
            if player_info:
                return render(request, 'nba_stats/search_results.html', {'players': player_info})
            else:
                return render(request, 'nba_stats/search_results.html', {'error': 'No players found.'})
    else:
        form = PlayerSearchForm()

    return render(request, 'nba_stats/search.html', {'form': form})


def player_details(request, player_id):
    """
    Show detailed stats for a particular player, identified by player_id.

    The view:
    - Fetches the player's career stats and calculates career per-game averages.
    - Provides a dropdown form to select either Regular Season or Post Season stats by year.
    - On form submission (POST), updates the chosen_stats table accordingly.
    - Renders a page with the player's headshot, name, career totals, per-game averages,
      and a selected seasonal breakdown if requested.
    """
    # Retrieve comprehensive career stats
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_dict = career.get_normalized_dict()
    career_stats = career_dict['CareerTotalsRegularSeason'][0] if career_dict['CareerTotalsRegularSeason'] else None

    # Get player's display name and headshot image
    player_name, headshot_url = get_player_name_and_image(player_id)

    dropdown_form = StatsDropdownForm()

    # Compute career per-game averages if career_stats are available
    if career_stats and career_stats.get('GP', 0) > 0:
        gp = career_stats.get('GP', 0) or 0
        pts = career_stats.get('PTS', 0) or 0
        reb = career_stats.get('REB', 0) or 0
        ast = career_stats.get('AST', 0) or 0
        stl = career_stats.get('STL', 0) or 0
        blk = career_stats.get('BLK', 0) or 0

        pts_pg = round(pts / gp, 2) if gp > 0 else 0
        reb_pg = round(reb / gp, 2) if gp > 0 else 0
        ast_pg = round(ast / gp, 2) if gp > 0 else 0
        stl_pg = round(stl / gp, 2) if gp > 0 else 0
        blk_pg = round(blk / gp, 2) if gp > 0 else 0
    else:
        pts_pg = reb_pg = ast_pg = stl_pg = blk_pg = 0

    chosen_stats = []
    chosen_title = None

    # Process the dropdown form for selecting seasonal stats
    if request.method == 'POST':
        dropdown_form = StatsDropdownForm(request.POST)
        if dropdown_form.is_valid():
            option = dropdown_form.cleaned_data['option']
            if option == 'Reg. Season':
                chosen_stats = career_dict.get('SeasonTotalsRegularSeason', [])
                chosen_title = "Regular Season"
            elif option == 'Post Season':
                chosen_stats = career_dict.get('SeasonTotalsPostSeason', [])
                chosen_title = "Post Season"

            # Compute per-game averages for the chosen stats
            for season in chosen_stats:
                gp_s = season.get('GP', 0) or 0
                pts = season.get('PTS', 0) or 0
                reb = season.get('REB', 0) or 0
                ast = season.get('AST', 0) or 0
                stl = season.get('STL', 0) or 0
                blk = season.get('BLK', 0) or 0

                if gp_s > 0:
                    season['PPG'] = round(pts / gp_s, 2)
                    season['RPG'] = round(reb / gp_s, 2)
                    season['APG'] = round(ast / gp_s, 2)
                    season['STLPG'] = round(stl / gp_s, 2)
                    season['BLKPG'] = round(blk / gp_s, 2)
                else:
                    season['PPG'] = season['RPG'] = season['APG'] = season['STLPG'] = season['BLKPG'] = 0

                if season['FG3_PCT'] is None:
                    season['FG3_PCT'] = 0

    context = {
        'player_id': player_id,
        'player_name': player_name,
        'headshot_url': headshot_url,
        'career_stats': career_stats,
        'dropdown_form': dropdown_form,
        'pts_pg': pts_pg,
        'reb_pg': reb_pg,
        'ast_pg': ast_pg,
        'stl_pg': stl_pg,
        'blk_pg': blk_pg,
        'chosen_stats': chosen_stats,
        'chosen_title': chosen_title
    }

    return render(request, 'nba_stats/player_details.html', context)

@login_required
def add_to_roster(request, player_id):
    player_name, player_image_url = get_player_name_and_image(player_id)

    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if player already in the user's roster
    if Roster.objects.filter(user=user_profile, player_id=player_id).exists():
        return JsonResponse({'status': 'error', 'message': 'Player already in roster'})

    # Add player to roster
    Roster.objects.create(
        user=user_profile,
        player_id=player_id,
        player_name=player_name,
        player_image_url=player_image_url
    )

    return JsonResponse({'status': 'success', 'message': f'{player_name} added to roster!'})

@login_required
def user_roster(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    roster = user_profile.roster.all()

    return render(request, 'nba_stats/roster.html', {'roster': roster})

@login_required
def remove_from_roster(request, player_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    player = get_object_or_404(Roster, user=user_profile, player_id=player_id)

    player.delete()
    return redirect('nba_stats:roster')