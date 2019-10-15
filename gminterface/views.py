from django.shortcuts import render, redirect
from engine.models import *

forbidden_redirect = 'https://parahumans.wordpress.com/' # 'gm-forbidden'

def is_gm(user, gameID):
	try:
		for gm in GM.objects.all():
			if gm.game.id == gameID and gm.user.id == user.id:
				return True
			return False
	except:
		return False

def forbidden(request):
	return render(request, 'gminterface/forbidden.html')

def index(request, gameID):
	if not is_gm(request.user, gameID):
		return redirect(forbidden_redirect)

	game = GM.objects.get(game__id=gameID)
	gms = GM.objects.filter(game__id=gameID)
	players = Player.objects.filter(game__id=gameID)
	items = Item.objects.filter(game__id=gameID)
	conditions = Condition.objects.filter(game__id=gameID)
	triggers = Trigger.objects.filter(game__id=gameID)
	context = {'game': game, 'gms': gms, 'players': players, 'items': items, 'conditions': conditions, 'triggers': triggers}
	return render(request, 'gminterface/index.html', context)

def playerprofile(request, gameID, username):
	if not is_gm(request.user, gameID):
		return redirect(forbidden_redirect)

	player = Player.objects.filter(game__id=gameID).filter(player__user__username=username)
	items = Item.objects.filter(owners__user__username=username)
	context = {'player': player, 'items': items}
	return render(request, 'gminterface/playerprofile.html', context)

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