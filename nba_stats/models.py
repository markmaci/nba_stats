"""
models.py

Defines database models to store and manage additional data about NBA players.
These models supplement the application's functionality by allowing local storage
of player profiles, tags, comments, stat snapshots, and headshot data. They help
demonstrate the use of relational data structures (via foreign keys), as well as
facilitating CRUD operations and data retrieval independent of the external API.
"""

from django.db import models

class PlayerProfile(models.Model):
    """
    Represents a locally saved player profile. This stores a player's ID and name
    from the NBA API, serving as a central record that other models can reference.
    """
    player_id = models.IntegerField(unique=True)  # Unique NBA player ID
    player_name = models.CharField(max_length=100) # Display name of the player
    stats = models.JSONField(null=True, blank=True)  # JSON data for player stats
    ppg = models.FloatField(null=True, blank=True)  # Points per game
    rpg = models.FloatField(null=True, blank=True)  # Rebounds per game
    apg = models.FloatField(null=True, blank=True)  # Assists per game
    spg = models.FloatField(null=True, blank=True)  # Steals per game
    bpg = models.FloatField(null=True, blank=True)  # Blocks per game
    tovpg = models.FloatField(null=True, blank=True)  # Turnovers per game
    fg_pct = models.FloatField(null=True, blank=True)  # Field goal percentage
    ft_pct = models.FloatField(null=True, blank=True)  # Free throw percentage
    three_pt_pct = models.FloatField(null=True, blank=True)  # Three-point percentage
    point_total = models.IntegerField(null=True, blank=True)  # Career points
    rebound_total = models.IntegerField(null=True, blank=True)  # Career rebounds
    assist_total = models.IntegerField(null=True, blank=True)  # Career assists
    steal_total = models.IntegerField(null=True, blank=True)  # Career steals
    block_total = models.IntegerField(null=True, blank=True)  # Career blocks
    turnover_total = models.IntegerField(null=True, blank=True)  # Career turnovers
    seasons_played = models.IntegerField(null=True, blank=True)  # Number of seasons played

    def __str__(self):
        return self.player_name


class PlayerComment(models.Model):
    """
    Stores user comments or notes about a player. Each comment references one 
    PlayerProfile, enabling the addition of feedback, insights, or opinions.
    """
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()  # The content of the user's comment

    def __str__(self):
        return f"Comment on {self.player.player_name}"


class PlayerStatSnapshot(models.Model):
    """
    Represents a saved statistical snapshot of a player for a particular season. 
    This model references a PlayerProfile and allows storing custom stat data (e.g., 
    points per game, rebounds per game) for user-defined seasons.
    """
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='statsnapshots')
    season = models.CharField(max_length=20)  # Season identifier, e.g. "2020-21"
    ppg = models.FloatField(null=True, blank=True) # Points per game
    rpg = models.FloatField(null=True, blank=True) # Rebounds per game
    apg = models.FloatField(null=True, blank=True) # Assists per game

    def __str__(self):
        return f"{self.player.player_name} - {self.season} Snapshot"


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
