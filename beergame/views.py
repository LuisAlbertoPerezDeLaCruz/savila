from django.shortcuts import get_object_or_404, redirect, render
from .models import Game
from .forms import NewGameForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html', {})


@login_required
def new_game(request):
    game = Game()
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.save()
            return redirect('home')
    else:
        form = NewGameForm()
    return render(request, 'new_game.html', {'game': game, 'form': form})
