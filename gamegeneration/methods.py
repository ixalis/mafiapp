#from django.contrib.auth.models import User
from gamegeneration.models import *
import random

#################### ITEM AND ABILITY FORMS #########################3#
questiontaser = {
        'target': ('Who is the target?', 'User'),
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
    target = parameters['target']
    #Work in progress
    return 'You have tased ' + target + '. They can not kill you for the next 15 minutes, and are roleblocked for today.'

def activatelynchvote(parameters):
    #work in progress
    target = parameters['target']
    pass

def usecoin(parameters):
    action = parameters['action']
    amount = parameters['amount']
    answer = ""
    if action.lower() == 'flip':
        for i in range(int(amount)):
            r = random.randint(0,1)
            if r==0:
                answer = answer+'H'
            else:
                answer = answer +'T'
    return answer

def activatekill(parameters):
    pass
