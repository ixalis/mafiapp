from django.shortcuts import render
from gamegeneration.models import *
from django.http import HttpResponse
from forms import *

def index(request):
    players = User.objects.all()
    items = Item.objects.all()
    abilities = Ability.objects.all()
    context = {'players':players, 'items':items, 'abilities':abilities}
    return render(request, 'gminterface/index.html', context)
    #return HttpResponse("Hello, world. You are at the index")

def playerprofile(request, playername):
    player = User.objects.get(username=playername)
    attributes = AttributeInstance.objects.filter(owner=player)
    items = ItemInstance.objects.filter(owner=player)
    abilities = AbilityInstance.objects.filter(owner=player)
    context = {'player':player, 'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'playerinterface/profile.html', context)

def itemprofile(request, itemid):
    item = Item.objects.get(id=itemid)
    context = {'item':item}
    return render(request, 'gminterface/itemprofile.html', context)

def abilityprofile(request, abilityid):
    ability = Ability.objects.get(id=abilityid)
    context = {'ability':ability}
    return render(request, 'gminterface/abilityprofile.html', context)

def attributeprofile(request, attributeid):
    attribute = Attribute.objects.get(id=attributeid)
    context = {'attribute':attribute}
    return render(request, 'gminterface/attributeprofile.html', context)

def generateitem(request, itemid):
    item = Item.objects.get(id=itemid)
    if request.method == 'POST':
        form = ItemInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            #Get answers
    else:
       form = ItemInstanceForm()
    context = {'form':form, 'main':item}
    return render(request, 'form.html', context)
