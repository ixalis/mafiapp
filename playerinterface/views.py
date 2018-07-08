from django.shortcuts import render, redirect
from gamegeneration.models import *
from django.http import HttpResponse
from django.views import generic
from forms import *
#from django.contrib.auth.mixins import LoginRequiredMixin

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

class inv(generic.ListView):
    model = ItemInstance
    template_name= 'playerinterface/inv.html'
    def get_queryset(self):
        #player = Player.objects.get(user=self.request.user)
        return ItemInstance.objects.filter(owner=self.request.user)
        #return ItemInstance.objects.all()

def iteminstance(request, itemid):
    item = ItemInstance.objects.filter(id=itemid)
    #itype = item.itype
    context = {'item':item, 'itemid':itemid}
    return render(request, 'iteminstance.html', context)

def itemused(request, itemid):
    item = ItemInstance.objects.get(id=itemid)
    parameters = item.get_requests()
    if request.method == 'POST':
        form = UseItemForm(request.POST, extra=parameters)
        if form.is_valid():
            #for (question, answer) in form.extra_answers():
                #save_answer(request, question, answer)
            item.use(form.get_answers())
            return redirect("profile")
    else:
        form = UseItemForm(extra = parameters)
    return render(request, "form.html", {'form':form})



def profile(request):
    user = request.user
    items = ItemInstance.objects.filter(owner=user)
    abilities = AbilityInstance.objects.filter(owner=user)
    attributes = AttributeInstance.objects.filter(owner=user)

    context = {'items':items, 'abilities':abilities, 'attributes':attributes}
    return render(request, 'playerinterface/profile.html', context)
