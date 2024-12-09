from django import forms
from django.core import validators
from .models import PlayerProfile,  PlayerComment, PlayerStatSnapshot

STAT_OPTIONS = (
    ('---', '---'),
    ('Reg. Season', 'Regular Season'),
    ('Post Season', 'Post Season'),
)

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ['player_id', 'player_name']

class PlayerCommentForm(forms.ModelForm):
    class Meta:
        model = PlayerComment
        fields = ['player', 'comment_text']

class PlayerStatSnapshotForm(forms.ModelForm):
    class Meta:
        model = PlayerStatSnapshot
        fields = ['player', 'season', 'ppg', 'rpg', 'apg']

class PlayerSearchForm(forms.Form):
    player_name = forms.CharField(
        label='',
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search a player',
                'class': 'form-control',
                'aria-label': 'Player Name'
            }
        ),
        error_messages={
            'required': 'Please enter a player name.'
        }
    )

class StatsDropdownForm(forms.Form):
    option = forms.ChoiceField(choices=STAT_OPTIONS, label="View Stats By:", required=True, 
                               error_messages={'required': 'Please select an option'})
