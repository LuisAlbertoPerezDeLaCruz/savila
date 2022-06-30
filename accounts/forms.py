from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput())

    first_name = forms.CharField(max_length=254, required=True)

    last_name = forms.CharField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')
