"""
File: forms.py
Author: Mark Maci, markmaci@bu.edu, 12/10/2024
Description: This file contains Django forms for user signup/login, player search across the NBA API, and stat dropdown selection
for regular and post-season stats.
"""
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(forms.ModelForm):
    """A form for user signup, extending Django's ModelForm to include custom fields and validation."""

    # Password field with password input widget for security
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Password"
    )
    
    # Confirm password field to ensure user inputs matching passwords
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Confirm Password"
    )

    class Meta:
        """Metadata for the SignupForm, specifying the model and fields used."""
        model = User
        fields = ['username', 'email']

    # Optional field for user's favorite NBA team
    favorite_team = forms.CharField(
        max_length=100, 
        required=False, 
        label="Favorite NBA Team"
    )

    def clean(self):
        """Custom validation to ensure passwords match."""
        cleaned_data = super().clean()  # Get cleaned data from the parent class
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Raise a validation error if passwords do not match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data  # Return the cleaned data

class PlayerSearchForm(forms.Form):
    """A form for searching players by name."""

    # Field for player name input, with additional attributes for better user experience
    player_name = forms.CharField(
        label='',
        max_length=100,  # Maximum character limit for player name
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search a player',
                'class': 'form-control',  # Bootstrap styling class
                'aria-label': 'Player Name'
            }
        ),
        error_messages={
            'required': 'Please enter a player name.'
        }
    )

# Tuple of stat options for dropdown menu
STAT_OPTIONS = (
    ('---', '---'),
    ('Reg. Season', 'Regular Season'),
    ('Post Season', 'Post Season'),
)

class StatsDropdownForm(forms.Form):
    """A form for selecting stat options from a dropdown menu."""

    # Dropdown menu field for selecting stats category
    option = forms.ChoiceField(
        choices=STAT_OPTIONS,
        label="View Stats By:",
        required=True,  # Field is required
        error_messages={
            'required': 'Please select an option'
        }
    )