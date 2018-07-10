from django.shortcuts import render, redirect
from gamegeneration.models import *
from django.http import HttpResponse
from django.views import generic
from forms import *


def profile(request):
    """
    View for User Profile
    """
    user = request.user
    items = ItemInstance.objects.filter(owner=user)
    abilities = AbilityInstance.objects.filter(owner=user)
    attributes = AttributeInstance.objects.filter(owner=user)

    context = {'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'playerinterface/profile.html', context)

def iteminstance(request, itemid):
    """
    View for a single item instance
    """
    item = ItemInstance.objects.get(id=itemid)
    itype = item.get_itype()
    description = itype.get_description()
    name = itype.get_name()
    context = {'name':name, 'description':description, 'itemid':itemid}
    return render(request, 'iteminstance.html', context)

def itemuse(request, itemid):
    """
    View for form for using an item
    """
    item = ItemInstance.objects.get(id=itemid)
    requests = item.get_requests()

    if request.method == 'POST':
        form = AutoGenerateForm(request.POST, extra=requests)
        if form.is_valid():
            parameters = form.get_answers()
            message = item.use(form.get_answers())
            #Display the message you get at the end
            return HttpResponse(message)
    else:
        form = AutoGenerateForm(extra = requests)
    
    #Render the form
    context = {'form':form}
    return render(request, "form.html", context)
