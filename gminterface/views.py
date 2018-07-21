from django.shortcuts import render
from gamegeneration.models import *
from django.http import HttpResponse
from forms import *

def index(request):
    import gamegeneration.methods as methods2
    players = User.objects.all()
    items = Item.objects.all()
    abilities = Ability.objects.all()
    gmactions = dir(methods2.GM)
    gmactions.remove('__doc__')
    gmactions.remove('__module__')
    context = {'players':players, 'items':items, 'abilities':abilities, 'gmactions':gmactions}
    return render(request, 'gminterface/index.html', context)
    #return HttpResponse("Hello, world. You are at the index")

def playerprofile(request, playername):
    player = User.objects.get(username=playername)
    attributes = AttributeInstance.objects.filter(owner=player)
    items = ItemInstance.objects.filter(owner=player)
    abilities = AbilityInstance.objects.filter(owner=player)
    context = {'player':player, 'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'gminterface/profile.html', context)

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
        form = ItemInstanceForm(initial={'itype':item})
    context = {'form':form, 'main':item}
    return render(request, 'form.html', context)

def generateability(request, abilityid):
    ability = Ability.objects.get(id=abilityid)
    if request.method == 'POST':
        form = AbilityInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            #Get answers
    else:
        form = AbilityInstanceForm(initial={'itype':ability})
    context = {'form':form, 'main':ability}
    return render(request, 'form.html', context)

def history(request):
    messages = Message.objects.all()
    context = {'messages':messages}
    return render(request, "gminterface/history.html", context)

def playerinbox(request, playername):
    user = User.objects.get(username=playername)
    messages = Message.objects.filter(addressee=user)
    context = {'messages':messages}
    return render(request, "playerinterface/inbox.html",context)

def GMAbility(request, abilityname):
    import gamegeneration.methods as methods1
    e = getattr(methods1.GM, abilityname)
    message = e()
    context={'message':message}
    return render(request, "gmmessage.html", context)
