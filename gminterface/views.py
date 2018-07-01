from django.shortcuts import render
from gamegeneration.models import *
from abstract.models import *
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You are at the index")

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
