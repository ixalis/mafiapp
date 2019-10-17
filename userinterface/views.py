from django.shortcuts import render, redirect
from engine.models import *
from django.contrib.auth.decorators import login_required
from forms import *
from mafiapp.settings import DEBUG

def debug(request):
	if (not DEBUG):
		return render(request, 'userinterface/message.html', {'message': "Currently not in debug mode."})

	games = Game.objects.all()
	players = Player.objects.all()
	gms = GM.objects.all()
	items = Item.objects.all()
	triggers = Trigger.objects.all()

	context = {'games': games, 'players': players, 'gms': gms, 'items': items, 'triggers': triggers}

	return render(request, 'userinterface/debug.html', context)

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')

	form = SignUpForm()
	return render(request, 'userinterface/signup.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'registration/profile.html')

@login_required
def home(request):
	players = Player.objects.filter(user__username=request.user.username)
	gms = GM.objects.filter(user__username=request.user.username)
	games = Game.objects.all()
	context = {'players': players, 'gms': gms, 'games': games}
	return render(request, 'userinterface/home.html', context)

@login_required
def new_game(request):
	if request.method == 'POST':
		form = NewGameForm(request.POST)
		if form.is_valid():
			game_name = form.cleaned_data.get('game_name')
			game = Game(name=game_name)
			game.save()
			gm = GM(user=request.user, game=game)
			gm.save()
			return redirect('gm-index', gameID=game.id)
	else:
		form = NewGameForm()
	return render(request, 'userinterface/new_game.html', {'form': form})