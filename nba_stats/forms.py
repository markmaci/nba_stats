from django import forms
from django.core import validators
from .models import PlayerProfile, PlayerComment, PlayerStatSnapshot

# Dropdown options for the stats selection form
STAT_OPTIONS = (
    ('---', '---'),  # Default option
    ('Reg. Season', 'Regular Season'),  # Regular season stats
    ('Post Season', 'Post Season'),  # Postseason stats
)

# Form for creating or updating player profiles
class PlayerProfileForm(forms.ModelForm):
    """
    A form for creating or updating a player's profile. This is tied to the 
    PlayerProfile model and allows setting the player's ID and name.
    """
    class Meta:
        model = PlayerProfile  # The associated model
        fields = ['player_id', 'player_name']  # Fields exposed in the form

# Form for submitting player comments
class PlayerCommentForm(forms.ModelForm):
    """
    A form for submitting comments about a player. This is tied to the 
    PlayerComment model and allows setting the related player and the comment text.
    """
    class Meta:
        model = PlayerComment  # The associated model
        fields = ['player', 'comment_text']  # Fields exposed in the form

# Form for creating or updating player stat snapshots
class PlayerStatSnapshotForm(forms.ModelForm):
    """
    A form for submitting or updating a snapshot of a player's statistics. This is 
    tied to the PlayerStatSnapshot model and includes basic performance metrics.
    """
    class Meta:
        model = PlayerStatSnapshot  # The associated model
        fields = ['player', 'season', 'ppg', 'rpg', 'apg']  # Fields exposed in the form

# Form for searching players by name
class PlayerSearchForm(forms.Form):
    """
    A simple form for searching players by name. Includes validation to ensure
    the input is not empty and provides an accessible and styled search field.
    """
    player_name = forms.CharField(
        label='',  # No visible label
        max_length=100,  # Limit the player name to 100 characters
        required=True,  # Make this field mandatory
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search a player',  # Placeholder text in the input field
                'class': 'form-control',  # Bootstrap class for styling
                'aria-label': 'Player Name'  # Accessibility label for screen readers
            }
        ),
        error_messages={
            'required': 'Please enter a player name.'  # Custom error message for empty input
        }
    )

# Form for selecting stats view options
class StatsDropdownForm(forms.Form):
    """
    A dropdown form for selecting a statistics category (e.g., Regular Season, 
    Post Season). Ensures that the user selects a valid option.
    """
    option = forms.ChoiceField(
        choices=STAT_OPTIONS,  # Predefined options for the dropdown
        label="View Stats By:",  # Label displayed next to the dropdown
        required=True,  # Make selection mandatory
        error_messages={
            'required': 'Please select an option'  # Custom error message for no selection
        }
    )
