from django.shortcuts import render
from gamegeneration.models import *
from abstract.models import *
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You are at the index")

def inventory(request, player):
    items = ItemInstance.objects.all()
    num_items = ItemInstance.objects.all().count()
    item_list = ', '.join([str(i) for i in items])
    context = {'item_list':item_list, 'num_items':num_items}
    return render(request, 'inventory.html', context)
    #return HttpResponse(output)
    #return HttpResponse("You are looking at %s " % poll_id)
