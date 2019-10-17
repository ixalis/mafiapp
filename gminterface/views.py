from django.shortcuts import render, redirect
from engine.models import *
from django.contrib.auth.decorators import login_required
from util import *

def is_gm(user, gameID):
	return GM.objects.filter(game__id=gameID).filter(user=user).exists()

@login_required
def index(request, gameID):
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = Game.objects.get(id=gameID)
	gms = GM.objects.filter(game__id=gameID)
	players = Player.objects.filter(game__id=gameID)
	items = Item.objects.filter(game__id=gameID)
	conditions = Condition.objects.filter(game__id=gameID)
	triggers = Trigger.objects.filter(item__game__id=gameID)
	context = {'game': game, 'gms': gms, 'players': players, 'items': items, 'conditions': conditions, 'triggers': triggers}
	return render(request, 'gminterface/index.html', context)

@login_required
def stop_gming(request, gameID):
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = Game.objects.get(id=gameID)
	gm = GM.objects.filter(game__id=gameID).filter(user=request.user)
	gm.delete()
	return message(request, "You have successfully stopped GMing for " + game.name)

@login_required
def delete_game(request, gameID):
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = Game.objects.get(id=gameID)
	m = game.name + " has been successfully deleted."
	game.delete()
	return message(request, m)

@login_required
def toggle_joining(request, gameID):
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	game = Game.objects.get(id=gameID)
	game.can_join = not game.can_join
	game.save()
	return redirect('gm-index', gameID=gameID)

@login_required
def player(request, gameID, playerID):
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	player = Player.objects.filter(id=playerID).filter(game__id=gameID)
	if (player.exists()):
		items = Item.objects.filter(owners__id=playerID)
		context = {'player': player.first(), 'items': items}
		return render(request, 'gminterface/player.html', context)

	return message(request, "That player does not exist.")

@login_required
def item(request, gameID, itemID):
	if not is_gm(request.user, gameID):
		return message(request, "You are not a GM of this game.")

	item = Item.objects.filter(itemID).filter(game__id=gameID)
	if (item.count() == 1):
		owners = Player.objects.filter(items__id=itemID)
		context = {'item': item.first(), 'owners': owners}
		return render(request, 'gminterface/item.html', context)

	return message(request, "That item does not exist.")


# def itemprofile(request, itemid):
# 	if not is_gm(request.user, gameID):
# 		return redirect(forbidden_redirect)

# 	item = Item.objects.get(id=itemid)
# 	context = {'item':item}
# 	return render(request, 'gminterface/itemprofile.html', context)

# def generateitem(request, itemid):
# 	if not is_gm(request.user, gameID):
# 		return redirect(forbidden_redirect)

# 	item = Item.objects.get(id=itemid)
# 	if request.method == 'POST':
# 		form = ItemInstanceForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('index')
# 	else:
# 		form = ItemInstanceForm(initial={'itype':item})
# 	context = {'form':form, 'main':item}
# 	return render(request, 'form.html', context)

# def deleteitem(request, itemid):
# 	if not is_gm(request.user, gameID):
# 		return redirect(forbidden_redirect)\

# 	item = ItemInstance.objects.get(id=itemid)
# 	item.delete()
# 	return redirect('playerprofile', item.owner.username)