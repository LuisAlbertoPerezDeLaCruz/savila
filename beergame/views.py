from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {})


def new_game(request):
    pass
