from django.shortcuts import render
from gamegeneration.models import *
from abstract.models import *
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You are at the index")

def inventory(request, playername):
    user = User.objects.get(username=playername)
    player = Player.objects.get(user=user)
    items = ItemInstance.objects.filter(owner=player)
    abilities = AbilityInstance.objects.filter(owner=player)
    goals = GoalInstance.objects.filter(owner=player)
    attributes = AttributeInstance.objects.filter(owner=player)

    #num_items = ItemInstance.objects.filter(owner=player).count()
    item_list = ', '.join([str(i) for i in items])
    ability_list = ', '.join([str(i) for i in abilities])
    attribute_list = ', '.join([str(i) for i in attributes])
    goal_list = ', '.join([str(i) for i in goals])

    context = {'item_list':item_list, 'ability_list':ability_list, 'goal_list':goal_list, 'attribute_list':attribute_list}
    return render(request, 'playerinterface/inventory.html', context)
    #return HttpResponse(output)
    #return HttpResponse("You are looking at %s " % poll_id)
