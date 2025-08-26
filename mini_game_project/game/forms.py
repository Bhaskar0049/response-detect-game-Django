"""
Forms for the game application.

Currently only a simple form is required for starting a new game. The
player provides their name which is validated and then used to create
or reuse a Player instance.
"""
from django import forms


class StartGameForm(forms.Form):
    """Simple form to capture the player's name before starting a game."""

    name = forms.CharField(
        max_length=30,
        label='Your name',
        widget=forms.TextInput(attrs={'class': 'border px-2 py-1 rounded w-full'}),
    )