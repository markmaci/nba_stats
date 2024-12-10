"""
File: models.py
Author: Mark Maci, markmaci@bu.edu, 12/10/2024
Description: This file contains Django models for user profiles, rosters, and player headshots for the nba_stats application.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.CharField(max_length=100, blank=True, null=True)  # Optional favorite NBA team

    def __str__(self):
        return self.user.username


class Roster(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="roster")
    player_id = models.IntegerField()  # NBA player ID from the API
    player_name = models.CharField(max_length=100)
    player_image_url = models.URLField()  # URL for the player's headshot

    def __str__(self):
        return f"{self.player_name} (Added by {self.user.user.username})"


class PlayerHeadShot(models.Model):
    """
    Stores a player's headshot image data. This model is separate and can be used 
    to cache player images locally, providing a consistent reference regardless of 
    external API changes.
    """
    player_id = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=100, default="N/A")
    player_image_url = models.URLField(default="https://via.placeholder.com/150")  # URL to player's headshot
    background_colour = models.CharField(max_length=7, blank=True, null=True, default="#FFFFFF") 
    # This could be used for styling player pages based on a team color or aesthetic

    def __str__(self):
        return f"{self.player_name} Head Shot"
