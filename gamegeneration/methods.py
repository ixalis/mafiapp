#from django.contrib.auth.models import User
from gamegeneration.models import *
import random

################################ DJANGO INTERACTION METHODS ###############################
def get_attt(attribute, username):
    user = User.objects.get(username=username)
    att = Attribute.objects.get(name=attribute)
    atti = AttributeInstance.objects.filter(itype=att).get(owner=user)
    return getattr(atti, 'value')

def set_att(attribute, username, value):
    user = User.objects.get(username=username)
    att = Attribute.objects.get(name=attribute)
    atti = AttributeInstance.objects.filter(itype=att).get(owner=user)
    setattr(atti, 'value', value)
    atti.save()

def make_att(name, atype='str', default='0', description='No description'):
    if Attribute.objects.filter(name=name).count() == 0:
        att = Attribute(name=name, atype=atype, default=default, description=description);
        att.save()
        for user in User.objects.all():
            atti = AttributeInstance(itype=att, owner=user, value=att.default)
            atti.save()

def make_item(itype, owner):
    item = ItemInstance(itype=Item.objects.get(name=itype), owner=User.objects.get(name=owner))
    item.save()

def make_itemtype(name, description='No description'):
    if Item.objects.filter(name=name).count() == 0:
        item = Item(name=name, description=description)
        item.save()

######################################### HELPER METHODS #########################################
class default():
    questions = {}
    description = ""
    @staticmethod
    def use(parameters):
        return "You have used the item " + str(parameters['itype']) + ". GMs have been notified."
    def activate(parameters):
        return "You have used the ability " + str(parameters['itype']) + ". GMs have been notified."

def is_guilty(target, death):
    att = Attribute.objects.get(name=target+'Guilty')
    atti = AttributeInstance.objects.filter(itype=att).get(owner=target)
    return getattr(atti, 'value')


########################################## ABILITIES #############################################
class kill():
    questions = {
            'target':('Who did you kill?', 'User'),
            'time':('When did you kill them?', 'time'),
            'place':('Where did this murder take place?', 'str'),
            }

    @staticmethod
    def activate(parameters):
        set_att('Alive', parameters['target'], 'False')
        make_att(str(parameters['target'])+'Guilty', atype='boolean', default='False')
        set_att(str(parameters['target'])+'Guilty',parameters['owner'], 'True')

        return "You have killed "+str(parameters['target'])+" at "+parameters['time']+" at "+parameters['place']+'.'

class lynchvote():
    questions = {
            'target':('Who do you want to lynch?', 'User')
            }
    @staticmethod
    def activate(parameters):
        set_att('Voted for', parameters['owner'], str(parameters['target']))
        return "You have voted for "+str(parameters['target'])+"."

class pickpocket():
    questions = {
        'target': ('Who did you pickpocket?', 'User')
        } 

class pairinvestigation():
    questions = {
        'targetdeath': ('Whose death are you investigating?'),
        'target1': ('Who are you investigating?', 'User'),
        'target2': ('Who are you investigating?', 'User'),
        }

class trap():
    questions = {
        'target': ('Who are you trapping?', 'User'),
        'role': ('As what?', 'str'),
        }

class admire():
    questions = {
        'target': ('Who are you admiring?', 'User'),
        }

class roleblock(): 
    questions = {
        'target': ('Who are you roleblocking?', 'User'),
        }

########################################### ITEMS ################################################
class coin():
    questions = {
        'action':('Flip or convert?', 'str'),
        'amount':('How many?', 'int'),
        }
    @staticmethod
    def use(parameters):
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
        if action.lower()=='convert':
            answer = 'Contact a gm'
        return answer

class taser():
    questions = {
            'target':('Who have you tased?', 'User'),
            }

class honeyjar():
    questions = {
            'target':('Who have you splashed?', 'User'),
            }

class mafiacounter():
    questions = {
            'action':('Sign or Use?', 'str'),
            }
    
class shovel():
    questions = {
            'target':('Who are you shoveling?', 'str'),
            }
    
class spiritsearch():
    questions = {
            'death':('Whose death are you investigating?', 'str'),
            'group':('Who participated in the ritual?', 'Usermult'),
            }

