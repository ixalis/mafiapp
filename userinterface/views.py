from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from mafiapp.settings import DEBUG
from engine.models import *
from forms import *
from util import *

def debug(request):
	if (not DEBUG):
		return message(request, "Currently not in debug mode.")

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
			profile = Profile(user=user)
			profile.save()
			login(request, user)
			return redirect('home')

	form = SignUpForm()
	return render(request, 'userinterface/signup.html', {'form': form})

@login_required
def profile(request):
	return redirect('home')

@login_required
def account(request):
	if not Profile.objects.filter(user=request.user):
		profile = Profile(user=request.user)
		profile.save()
	return render(request, 'userinterface/account.html', {'user': request.user})

@login_required
def change_email(request):
	return message(request, "Not yet supported, sorry.")

@login_required
def toggle_receive_emails(request):
	profile = Profile.objects.get(user=request.user)
	profile.receiveEmails = not profile.receiveEmails
	profile.save()
	return redirect('account')

@login_required
def change_password(request):
	return message(request, "Not yet supported, sorry.")

@login_required
def home(request):
	players = Player.objects.filter(user__username=request.user.username)
	gms = GM.objects.filter(user__username=request.user.username)
	joinable_games = Game.objects.filter(can_join=True)
	context = {'players': players, 'gms': gms, 'joinable_games': joinable_games}
	return render(request, 'userinterface/home.html', context)

@login_required
def join_game(request, gameID):
	if not Game.objects.filter(id=gameID).exists():
		return message(request, "This game does not exist.")

	game = Game.objects.get(id=gameID)

	if Player.objects.filter(user__username=request.user.username).filter(game__id=gameID).exists():
		return message(request, "You cannot join " + game.name + " as a player, as you are already playing in it.")

	if GM.objects.filter(user__username=request.user.username).filter(game__id=gameID).exists():
		return message(request, "You cannot join " + game.name + " as a player, as you are GMing it.")

	player = Player(user=request.user, game=game)
	player.save()
	return message(request, "You have successfully joined " + game.name + ".")

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