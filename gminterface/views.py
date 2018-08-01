from django.shortcuts import render, redirect
from gamegeneration.models import *
from django.http import HttpResponse
from forms import *
from django.contrib.auth.decorators import user_passes_test

def is_gm(user):
    return True
    try:
        return user.profile.currentPlayer.attributes.get('GM').value == 'True'
    except:
        return False

@user_passes_test(is_gm)
def index(request):
    import gamegeneration.methods as methods2
    players = Player.objects.all()
    items = Item.objects.all()
    abilities = Ability.objects.all()
    gmactions = dir(methods2.GM)
    gmactions.remove('__doc__')
    gmactions.remove('__module__')
    context = {'players':players, 'items':items, 'abilities':abilities, 'gmactions':gmactions}
    return render(request, 'gminterface/index.html', context)

@user_passes_test(is_gm)
def playerprofile(request, playername):
    player = User.objects.get(username=playername).profile.currentPlayer
    attributes = player.attributes.all()
    items = player.iteminstance_set.all()
    abilities = player.abilityinstance_set.all()
    context = {'player':player, 'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'gminterface/playerprofile.html', context)

@user_passes_test(is_gm)
def itemprofile(request, itemid):
    item = Item.objects.get(id=itemid)
    context = {'item':item}
    return render(request, 'gminterface/itemprofile.html', context)

@user_passes_test(is_gm)
def abilityprofile(request, abilityid):
    ability = Ability.objects.get(id=abilityid)
    context = {'ability':ability}
    return render(request, 'gminterface/abilityprofile.html', context)

@user_passes_test(is_gm)
def generateitem(request, itemid):
    item = Item.objects.get(id=itemid)
    if request.method == 'POST':
        form = ItemInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ItemInstanceForm(initial={'itype':item})
    context = {'form':form, 'main':item}
    return render(request, 'form.html', context)

@user_passes_test(is_gm)
def generateability(request, abilityid):
    ability = Ability.objects.get(id=abilityid)
    if request.method == 'POST':
        form = AbilityInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AbilityInstanceForm(initial={'itype':ability})
    context = {'form':form, 'main':ability}
    return render(request, 'form.html', context)

@user_passes_test(is_gm)
def deleteitem(request, itemid):
    item = ItemInstance.objects.get(id=itemid)
    item.delete()
    return redirect('playerprofile', item.owner.username)
@user_passes_test(is_gm)
def deleteability(request, abilityid):
    ability = Abilityinstance.objects.get(id=abilityid)
    ability.delete()
    return redirect('playerprofile', ability.owner.user.username)

@user_passes_test(is_gm)
def changeattribute(request, attid):
    att = Attribute.objects.get(id=attid)
    if request.method == 'POST':
        form = AttributeForm(request.POST, instance=att)
        if form.is_valid():
            form.save()
            return redirect(att.element.user.username)
    else:
        form = AttributeForm(instance=att)
    context={'form':form, 'main':att}
    return render(request, 'form.html', context)

@user_passes_test(is_gm)
def history(request):
    messages = request.user.profile.currentPlayer.game.message_set.all()
    context = {'messages':messages}
    return render(request, "gminterface/history.html", context)

@user_passes_test(is_gm)
def playerinbox(request, playername):
    player = User.objects.get(username=playername).profile.currentPlayer
    messages = player.message_set.all()
    context = {'messages':messages}
    return render(request, "playerinterface/inbox.html",context)

@user_passes_test(is_gm)
def GMAbility(request, abilityname):
    import gamegeneration.methods as methods1
    e = getattr(methods1.GM, abilityname)
    message = e()
    m = Message(content=message, game=request.user.profile.currentPlayer.game)
    m.save()
    m.addressee.add(request.user.profile.currentPlayer)
    context={'message':message}
    return render(request, "gmmessage.html", context)
