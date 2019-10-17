from django.shortcuts import render, redirect
from engine.models import *
from django.http import HttpResponse
from django.views import generic
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# @login_required
# def dashboard(request):
#     """
#     View for User Profile
#     """
#     player = request.user.profile.currentPlayer
#     items = player.iteminstance_set.all()
#     abilities = player.abilityinstance_set.all()
#     attributes = []
#     attributesme = player.attributes.all()
#     for a in attributesme:
#         if a.visible():
#             attributes.append(a)
#     context = {'user':request.user, 'player':player, 'items':items, 'abilities':abilities, 'attributes':attributes}
#     return render(request, 'playerinterface/profile.html', context)

# @login_required
# def itemuse(request, itemid):
#     """
#     View for form for using an item
#     """
#     item = ItemInstance.objects.get(id=itemid)
#     if item.owner != request.user.profile.currentPlayer and not is_gm(request.user):
#         return redirect('dashboard')

#     requests = item.get_requests()
#     if request.method == 'POST':
#         form = AutoGenerateForm(request.POST, extra=requests)
#         if form.is_valid():
#             parameters = form.get_answers()
#             parameters['owner'] = request.user.profile.currentPlayer
#             message = item.use(parameters)
#             m = Message(addressee=parameters['owner'], content=message, game=request.user.profile.currentPlayer.game)
#             m.save()
#             #Display the message you get at the end
#             context = {"message":message}
#             return render(request, 'gmmessage.html', context)
#     else:
#         form = AutoGenerateForm(extra = requests)
    
#     #Render the form
#     context = {'form':form, 'main':item.itype.name, 'instruction':item.get_usetext()}
#     return render(request, "form.html", context)

# def itemtransfer(request, itemid):
#     """
#     View form for transfering an item
#     """
#     item = ItemInstance.objects.get(id=itemid)
#     if item.owner != request.user.profile.currentPlayer and not is_gm(request.user):
#         return redirect('dashboard')

#     requests = item.get_requests()
#     if request.method == 'POST':
#         form = ItemTransferForm(request.POST)
#         if form.is_valid():
#             owner = form.get_answer()
#             message = item.transfer(owner)
#             item.save()
#             m = Message(addressee=owner, content=message, game=request.user.profile.currentPlayer.game)
#             #Display the message you get at the end
#             context = {"message":message}
#             return render(request, 'gmmessage.html', context)
#     else:
#         form = ItemTransferForm()
    
#     #Render the form
#     context = {'form':form, 'main':item.get_itype().get_name()}
#     return render(request, "form.html", context)