from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from engine.models import *
from forms import *
from util import *

@login_required
def index(request, gameID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")

	player = Player.objects.filter(game__id=gameID).filter(user=request.user)
	if not player.exists():
		return message(request, "You are not playing in that game.")

	player = player.first()
	items = Item.objects.filter(game__id=gameID).filter(owners=player)
	context = {'game': game.first(), 'player': player, 'items': items}
	return render(request, 'playerinterface/index.html', context)