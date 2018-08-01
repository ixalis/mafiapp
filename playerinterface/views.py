from django.shortcuts import render, redirect
from gamegeneration.models import *
from django.http import HttpResponse
from django.views import generic
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def is_gm(user):
    return True
    try:
        return user.profile.currentPlayer.attributes.get("GM").value == 'True'
    except:
        return False

def home(request):
    """
    Home page
    """
    return render(request, 'home.html', {})

@login_required
def dashboard(request):
    """
    View for User Profile
    """
    player = request.user.profile.currentPlayer
    items = player.iteminstance_set.all()
    abilities = player.abilityinstance_set.all()
    attributes = []
    attributesme = player.attributes.all()
    for a in attributesme:
        if a.visible():
            attributes.append(a)
    context = {'user':request.user, 'player':player, 'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'playerinterface/profile.html', context)

@login_required
def itemuse(request, itemid):
    """
    View for form for using an item
    """
    item = ItemInstance.objects.get(id=itemid)
    if item.owner != request.user.profile.currentPlayer and not is_gm(request.user):
        return redirect('dashboard')

    requests = item.get_requests()
    if request.method == 'POST':
        form = AutoGenerateForm(request.POST, extra=requests)
        if form.is_valid():
            parameters = form.get_answers()
            parameters['owner'] = request.user.profile.currentPlayer
            message = item.use(parameters)
            m = Message(addressee=parameters['owner'], content=message, game=request.user.profile.currentPlayer.game)
            m.save()
            #Display the message you get at the end
            context = {"message":message}
            return render(request, 'gmmessage.html', context)
    else:
        form = AutoGenerateForm(extra = requests)
    
    #Render the form
    context = {'form':form, 'main':item.itype.name, 'instruction':item.get_usetext()}
    return render(request, "form.html", context)

def itemtransfer(request, itemid):
    """
    View form for transfering an item
    """
    item = ItemInstance.objects.get(id=itemid)
    if item.owner != request.user.profile.currentPlayer and not is_gm(request.user):
        return redirect('dashboard')

    requests = item.get_requests()
    if request.method == 'POST':
        form = ItemTransferForm(request.POST)
        if form.is_valid():
            owner = form.get_answer()
            message = item.transfer(owner)
            item.save()
            m = Message(addressee=owner, content=message, game=request.user.profile.currentPlayer.game)
            #Display the message you get at the end
            context = {"message":message}
            return render(request, 'gmmessage.html', context)
    else:
        form = ItemTransferForm()
    
    #Render the form
    context = {'form':form, 'main':item.get_itype().get_name()}
    return render(request, "form.html", context)



@login_required
def abilityactivate(request, abilityid):
    """
    View for form for using an item
    """
    ability = AbilityInstance.objects.get(id=abilityid)
    if ability.owner != request.user.profile.currentPlayer and not is_gm(request.user):
        return redirect('dashboard')
    
    requests = ability.get_requests()
    if request.method == 'POST':
        form = AutoGenerateForm(request.POST, extra=requests)
        if form.is_valid():
            parameters = form.get_answers()
            parameters['owner'] = request.user.profile.currentPlayer
            message = ability.use(parameters)
            m = Message(addressee=parameters['owner'], content=message, game=request.user.profile.currentPlayer.game)
            m.save()
            #Display the message you get at the end
            context = {"message":message}
            return render(request, "gmmessage.html", context)
    else:
        form = AutoGenerateForm(extra = requests)
    
    #Render the form
    context = {'form':form, 'main':ability.itype.name, 'instruction':ability.get_usetext()}
    return render(request, "form.html", context)

@login_required
def profile(request):
    game = request.user.profile.currentPlayer.game
    context = {"message":"You are currently playing the game"+str(game)}
    return render(request, "gmmessage.html", context)

@login_required
def inbox(request):
    player = request.user.profile.currentPlayer
    messages = Message.objects.filter(addressee=player)
    context = {'messages':messages}
    return render(request, "playerinterface/inbox.html", context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'playerinterface/signup.html', {'form': form})
