#from django.contrib.auth.models import User
from gamegeneration.models import *

#################### ITEM AND ABILITY FORMS #########################3#
questiontaser = {
        'target': ('Who is the target?', 'User'),
        "attribute": ('What attribute?', 'Attribute'),
        "value": ('What value did you want to update it to?', 'int'),
        }
questionlynchvote = {
        'target': ("Who are you voting for?", 'User'),
        }
questioncoin = {
        'action': ('Flip or Convert', 'Option'),
        'amount': ('How many?', 'int'),
        }
questionkill = {
        'target': ('Who did you kill?', 'User'),
        'time': ('When did this happen?', 'time'),
        'place': ('Where did you kill them', 'str'),
        }


######################## ITEM AND ABILITY METHODS ########################
def usetaser(parameters):
    #name = parameters['target']
    #target = User.objects.get(username=name)
    attribute = parameters['attribute']
    attribute = 'Kill'
    attributetype = Attribute.objects.get(name=attribute)
    attributeinstance = AttributeInstance.objects.get(itype=attributetype)
    attributeinstance.value = 10
    attributeinstance.save()
    description = attributetype.get_description()
    return description+'   attribute'+parameters['value']

def activatelynchvote(parameters):
    pass

def usecoin(parameters):
    pass

def activatekill(parameters):
    pass
