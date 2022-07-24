from .models import Game, Course
from django import forms


class NewGameForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        help_text='Give the name you like to the game'
    )

    class Meta:
        model = Game
        fields = ['name', 'max_turns']


class NewCourseForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        help_text='Give the course name'
    )

    class Meta:
        model = Course
        fields = ['name']
