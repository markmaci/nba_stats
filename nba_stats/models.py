"""
models.py

Defines database models to store and manage additional data about NBA players.
These models supplement the application's functionality by allowing local storage
of player profiles, tags, comments, stat snapshots, and headshot data. They help
demonstrate the use of relational data structures (via foreign keys), as well as
facilitating CRUD operations and data retrieval independent of the external API.
"""

from django.db import models
class Team(models.Model):
    """
    Represents an NBA team.

    Attributes:
        abbreviation (str): The team's abbreviation (e.g., 'LAL' for Los Angeles Lakers).
        name (str): The full name of the team.
        city (str): The city where the team is based.
        conference (str): The conference the team belongs to (e.g., 'Western', 'Eastern').
        division (str): The division the team belongs to (e.g., 'Pacific', 'Central').
    """
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    conference = models.CharField(max_length=50, blank=True)
    division = models.CharField(max_length=50, blank=True)

    def __str__(self):
        """Returns the string representation of the team."""
        return self.name

class Season(models.Model):
    """
    Represents an NBA season.

    Attributes:
        year (int): The ending year of the season (e.g., 2023 for the 2022-2023 season).
    """
    year = models.IntegerField(unique=True)

    def __str__(self):
        """Returns the string representation of the season."""
        return f"{self.year -1}-{self.year}"

class Player(models.Model):
    """
    Represents an NBA player.

    Attributes:
        first_name (str): The player's first name.
        last_name (str): The player's last name.
        full_name (str): The player's full name (unique identifier).
        player_identifier (str): A unique identifier or slug for the player (optional).
        team (Team): The team the player is currently associated with.
        position (str): The player's position on the court (e.g., 'Guard', 'Forward').
        height (str): The player's height (e.g., '6-8' for 6 feet 8 inches).
        weight (int): The player's weight in pounds.
        birth_date (date): The player's birth date.
        headshot_url (URL): URL to the player's headshot image.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, unique=True)
    # 'full_name' serves as a unique identifier for each player
    player_identifier = models.CharField(max_length=20, unique=True, blank=True)
    # 'player_identifier' can store a unique slug from the data source
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=20, blank=True)
    height = models.CharField(max_length=10, blank=True)
    # Height is stored as a string to accommodate formats like '6-8'
    weight = models.IntegerField(null=True, blank=True)
    # Weight in pounds
    birth_date = models.DateField(null=True, blank=True)
    headshot_url = models.URLField(blank=True, null=True)
    # URL to the player's headshot image

    def __str__(self):
        """Returns the string representation of the player."""
        return self.full_name

class PlayerSeasonStats(models.Model):
    """
    Represents a player's statistics for a specific season.

    Attributes:
        player (Player): The player these stats belong to.
        season (Season): The season these stats are for.
        team (Team): The team the player was on during the season.
        games_played (int): The number of games the player played in the season.
        points_per_game (Decimal): The average points scored per game.
        rebounds_per_game (Decimal): The average rebounds per game.
        assists_per_game (Decimal): The average assists per game.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    games_played = models.IntegerField(null=True, blank=True)
    points_per_game = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rebounds_per_game = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assists_per_game = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # Additional stats can be added as needed (e.g., steals, blocks)

    class Meta:
        unique_together = ('player', 'season')
        # Ensures each player has only one set of stats per season

    def __str__(self):
        """Returns the string representation of the player's season stats."""
        return f"{self.player.full_name} - {self.season.year}"

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
