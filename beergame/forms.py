from .models import Game
from django import forms


class NewGameForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        help_text='Give the name you like to the game'
    )

    class Meta:
        model = Game
        fields = ['name', 'name']
