from django.shortcuts import render, redirect
from gamegeneration.models import *
from django.http import HttpResponse
from django.views import generic
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def is_gm(user):
    return user.username=='admin'

def home(request):
    """
    Home page
    """
    return render(request, 'home.html', {})

@login_required
def profile(request):
    """
    View for User Profile
    """
    user = request.user
    #if is_gm(user):
    #    return redirect('index')
    items = ItemInstance.objects.filter(owner=user)
    abilities = AbilityInstance.objects.filter(owner=user)
    attributes = []
    attributesme = AttributeInstance.objects.filter(owner=user)
    for itype in Attribute.objects.all():
        if itype.alwaysvisible:
            try:
                attributes.append(attributesme.get(itype=itype))
            except:
                pass
        elif itype.nondefaultvisible:
            try:
                attribute = attributesme.get(itype=itype)
                if itype.default != attribute.value:
                    attributes.append(attribute)
            except:
                pass
    context = {'user':user, 'player':user, 'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'playerinterface/profile.html', context)

@login_required
def itemuse(request, itemid):
    """
    View for form for using an item
    """
    item = ItemInstance.objects.get(id=itemid)
    if item.get_owner() != request.user and not is_gm(request.user):
        return redirect('profile')

    requests = item.get_requests()
    if request.method == 'POST':
        form = AutoGenerateForm(request.POST, extra=requests)
        if form.is_valid():
            parameters = form.get_answers()
            message = item.use(parameters)
            m = Message(addressee=parameters['owner'], content=message)
            m.save()
            #Display the message you get at the end
            context = {"message":message}
            return render(request, 'gmmessage.html', context)
    else:
        form = AutoGenerateForm(extra = requests)
    
    #Render the form
    context = {'form':form, 'main':item.get_itype().get_name(), 'instruction':item.get_usetext()}
    return render(request, "form.html", context)

def itemtransfer(request, itemid):
    """
    View form for transfering an item
    """
    item = ItemInstance.objects.get(id=itemid)
    if item.get_owner() != request.user and not is_gm(request.user):
        return redirect('profile')

    requests = item.get_requests()
    if request.method == 'POST':
        form = ItemTransferForm(request.POST)
        if form.is_valid():
            owner = form.get_answer()
            message = item.transfer(owner)
            item.save()
            m = Message(addressee=owner, content=message)
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
    if ability.get_owner() != request.user and not is_gm(request.user):
        return redirect('profile')
    
    requests = ability.get_requests()
    if request.method == 'POST':
        form = AutoGenerateForm(request.POST, extra=requests)
        if form.is_valid():
            parameters = form.get_answers()
            message = ability.use(parameters)
            m = Message(addressee=parameters['owner'], content=message)
            m.save()
            #Display the message you get at the end
            context = {"message":message}
            return render(request, "gmmessage.html", context)
    else:
        form = AutoGenerateForm(extra = requests)
    
    #Render the form
    context = {'form':form, 'main':ability.get_itype().get_name(), 'instruction':ability.get_usetext()}
    return render(request, "form.html", context)

def inbox(request):
    user = request.user
    messages = Message.objects.filter(addressee=user)
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
