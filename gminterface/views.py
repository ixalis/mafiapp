from django.shortcuts import render
from gamegeneration.models import *
from django.http import HttpResponse

def index(request):
    players = User.objects.all()
    items = Item.objects.all()
    abilities = Ability.objects.all()
    context = {'players':players, 'items':items, 'abilities':abilities}
    return render(request, 'gminterface/index.html', context)
    #return HttpResponse("Hello, world. You are at the index")

def playerprofile(request, playername):
    user = User.objects.get(username=playername)
    items = ItemInstance.objects.filter(owner=user)
    abilities = AbilityInstance.objects.filter(owner=user)
    context = {'user':user, 'items':items, 'abilities':abilities}
    return render(request, 'playerinterface/profile.html', context)

def itemprofile(request, itemname):
    item = Item.objects.get(name=itemname)
    context = {'item':item}
    return render(request, 'gminterface/itemprofile.html', context)

def abilityprofile(request, abilityname):
    ability = Ability.objects.get(name=abilityname)
    context = {'ability':ability}
    return render(request, 'gminterface/abilityprofile.html', context)


"""
def inventory(request):
    items = ItemInstance.objects.all()
    abilities = AbilityInstance.objects.all()
    goals = GoalInstance.objects.all()
    attributes = AttributeInstance.objects.all()

    #num_items = ItemInstance.objects.filter(owner=player).count()
    item_list = ', '.join([str(i) for i in items])
    ability_list = ', '.join([str(i) for i in abilities])
    attribute_list = ', '.join([str(i) for i in attributes])
    goal_list = ', '.join([str(i) for i in goals])

    context = {'item_list':item_list, 'ability_list':ability_list, 'goal_list':goal_list, 'attribute_list':attribute_list}
    return render(request, 'playerinterface/inventory.html', context)
    #return HttpResponse(output)
    #return HttpResponse("You are looking at %s " % poll_id)
"""
