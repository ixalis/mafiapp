from django.shortcuts import render, redirect
from engine.models import *
from django.contrib.auth.decorators import login_required
from util import *

def is_gm(user, gameID):
	return GM.objects.filter(game__id=gameID).filter(user=user).exists()

@login_required
def index(request, gameID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = game.first()
	gms = GM.objects.filter(game__id=gameID)
	players = Player.objects.filter(game__id=gameID)
	items = Item.objects.filter(game__id=gameID)
	conditions = Condition.objects.filter(game__id=gameID)
	triggers = Trigger.objects.filter(item__game__id=gameID)
	context = {'game': game, 'gms': gms, 'players': players, 'items': items, 'conditions': conditions, 'triggers': triggers}
	return render(request, 'gminterface/index.html', context)

@login_required
def stop_gming(request, gameID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = game.first()
	gm = GM.objects.filter(game__id=gameID).filter(user=request.user)
	gm.delete()
	return message(request, "You have successfully stopped GMing for " + game.name)

@login_required
def delete_game(request, gameID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = game.first()
	m = game.name + " has been successfully deleted."
	game.delete()
	return message(request, m)

@login_required
def toggle_joining(request, gameID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = game.first()
	game.can_join = not game.can_join
	game.save()
	return redirect('gm-index', gameID=gameID)

@login_required
def player(request, gameID, playerID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	player = Player.objects.filter(id=playerID).filter(game__id=gameID)
	if not player.exists():
		return message(request, "That player does not exist.")

	items = Item.objects.filter(owners__id=playerID)
	context = {'game': game.first(), 'player': player.first(), 'items': items}
	return render(request, 'gminterface/player.html', context)

@login_required
def item(request, gameID, itemID):
	game = Game.objects.filter(id=gameID)
	if not game.exists():
		return message(request, "That game does not exist.")
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	item = Item.objects.filter(itemID).filter(game__id=gameID)
	if not item.exists():
		return message(request, "That item does not exist.")

	owners = Player.objects.filter(items__id=itemID)
	context = {'game': game.first, 'item': item.first(), 'owners': owners}
	return render(request, 'gminterface/item.html', context)