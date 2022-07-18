from .models import Game, Course
from django import forms


class NewGameForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        help_text='Give the name you like to the game'
    )

    class Meta:
        model = Game
        fields = ['name', 'course']

    def __init__(self, institution, *args, **kwargs):
        super(NewGameForm, self).__init__(
            *args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(
            institution__pk=institution.pk)
