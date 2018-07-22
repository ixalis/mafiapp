#from django.contrib.auth.models import User
from gamegeneration.models import *
import random

################################ DJANGO INTERACTION METHODS ###############################
def user(username):
    return User.objects.get(username=username)

def get_att(attribute, user):
    att = Attribute.objects.get(name=attribute)
    atti = AttributeInstance.objects.filter(itype=att).get(owner=user)
    return getattr(atti, 'value')

def set_att(attribute, user, value):
    att = Attribute.objects.get(name=attribute)
    atti = AttributeInstance.objects.filter(itype=att).get(owner=user)
    setattr(atti, 'value', value)
    atti.save()

def make_att(name, atype='str', default='0', description='No description', alwaysvisible=False, nondefaultvisible=True):
    if Attribute.objects.filter(name=name).count() == 0:
        att = Attribute(name=name, atype=atype, default=default, description=description, alwaysvisible=alwaysvisible, nondefaultvisible=nondefaultvisible);
        att.save()
        for user in User.objects.all():
            atti = AttributeInstance(itype=att, owner=user, value=att.default)
            atti.save()

def make_item(itype, owner):
    item = ItemInstance(itype=Item.objects.get(name=itype), owner=owner)
    item.save()

def make_itemtype(name, description='No description'):
    if Item.objects.filter(name=name).count() == 0:
        item = Item(name=name, description=description)
        item.save()

def write_message(message, addressee):
    m = Message(addressee=addressee, content=message)
    m.save()

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
    try:
        if Attribute.objects.filter(name='Dead').get(owner=death) == 'False':
            return False
        att = Attribute.objects.get(name=str(target)+'Guilty')
        atti = AttributeInstance.objects.filter(itype=att).get(owner=target)
        v = getattr(atti, 'value')
        if v=='True':
            return True
        return False
    except:
        return False

def clearattribute(name):
    a = Attribute.objects.get(name=name)
    ai = AttributeInstance.objects.filter(itype=a)
    for att in ai:
        setattr(att, 'value', a.default)
        att.save()

def string_to_list(string):
    return string.split(',')
def list_to_string(l):
    final = ""
    for i in l:
        final = final+i+","
    return final[:-1]

def count_mafia():
    a = Attribute.objects.get(name='Alignment')
    return AttributeInstance.filter(itype=a).filter(value='Mafia').count()


########################################## ABILITIES #############################################
class kill():
    questions = {
            'target':('Who did you kill?', 'User'),
            'time':('When did you kill them?', 'time'),
            'place':('Where did this murder take place?', 'str'),
            }

    @staticmethod
    def activate(parameters):
        set_att('Dead', parameters['target'], 'True')
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
    @staticmethod
    def activate(parameters):
        inventory = ItemInstance.objects.filter(owner=user(parameters['target']))
        loot = random.choice(inventory)
        setattr(loot,'owner', parameters['owner'])
        loot.save()
        return "You have pickpocketed "+str(parameters['target'])+" and recieved the item "+ str(loot.itype.name)+"."

class pairinvestigation():
    questions = {
        'targetdeath': ('Whose death are you investigating?'),
        'target1': ('Who are you investigating?', 'User'),
        'target2': ('Who are you investigating?', 'User'),
        }
    @staticmethod
    def activate(parameters):
        target1, target2, targetdeath = parameters['target1'], parameters['target2'], parameters['targetdeath']
        guilty1 = is_guilty(target1, targetdeath)
        guilty2 = is_guilty(target2, targetdeath)
        if guilty1 and guilty2:
            result = random.choice([target1, target2])
        elif guilty1:
            result = target1
        elif guilty2:
            result = target2
        else:
            result = random.choice([target1, target2])
        return "You have investigated "+str(target1)+ " and "+str(target2)+". and and heard about"+str(result)+ " as a possible suspect."

class trap():
    questions = {
        'target': ('Who are you trapping?', 'User'),
        'role': ('As what?', 'str'),
        }
    @staticmethod
    def activate(parameters):
        arole = get_att('Role', parameters['target'])
        splashed = get_att('Splashed', parameters['target'])
        if parameters['role'] == arole or splashed == 'True':
            set_att('Roleblocked', parameters['target'], 'True')
            return 'Your Trap has succeeded!'
        return 'Your Trap has failed. Sorry!'
"""
Day Abilities; To implement
"""
class admire():
    questions = {
        'target': ('Who are you admiring?', 'User'),
        }

class roleblock(): 
    questions = {
        'target': ('Who are you roleblocking?', 'User'),
        }
    @staticmethod
    def activate(parameters):
        set_att('Roleblocked', parameters['target'], 'True')

########################################### ITEMS ################################################
class coin():
    questions = {
        'amount':('How many flips?', 'int'),
        }
    @staticmethod
    def use(parameters):
        amount = parameters['amount']
        answer = "You flipped a coin. How exciting. You get the result "
        for i in range(int(amount)):
            r = random.randint(0,1)
            if r==0:
                answer = answer+'H'
            else:
                answe = answer+'T'
        return answer+"."

class taser():
    questions = {
            'target':('Who have you tased?', 'User'),
            }
    @staticmethod
    def use(parameters):
        name = 'Taser Handle with '+str(parameters['target'])+' inscribed'
        make_itemtype(name)
        make_item(name, parameters['owner'])
        set_att('Tased', parameters['target'], 'True')
        parameters['self'].delete()
        return 'You have tased '+str(parameters['target'])+ ' and recieved a '+name+'.'

class honeyjar():
    questions = {
            'target':('Who have you splashed?', 'User'),
            }
    @staticmethod
    def use(parameters):
        if get_att('Splashed', parameters['target']) == 'True':
            return 'You have attempted to splash '+parameters['target']+'and failed because they were already sticky.'
        set_att('Splashed', parameters['target'], 'True')
        parameters['self'].delete()
        return 'You have splashed '+str(parameters['target'])+' with a honey jar.'

class mafiacounter():
    questions = {
            'action':('What do you want to do with it?', ('sign', 'unsign', 'use', 'check signatures', 'clear signatures')),
            }
    @staticmethod
    def use(parameters):
        name = 'MCsignature'+str(parameters['self'].id)
        if parameters['action'].lower()=='use':
            try:
                signaturelist = RandomInfo.objects.get(name=name).content
            except:
                return "You tried to submit a mafia counter to the gods. Unfortunately, no one has ever signed this."
            slist = string_to_list(signaturelist)
            number = len(slist)
            if number > get_majority():
                return "You tried to submit a mafia counter to the gods. Unfortunately, you do not have enough signatures."
            else:
                learner = User.objects.get(username=random.choice(slist))
                mafianumber = count_mafia()
                write_message(addressee=learner, content="From the mafia counter you signed not too long ago, you learned that there exist "+mafianumber+" mafia in the world today.")
                parameters['self'].delete()
            return "You have successfully used your mafia counter. Tell everyone to check their messages!"
        elif parameters['action'].lower()=='sign':
            try:
                ri = RandomInfo.objects.get(name=name)
                signaturestr = ri.content
                signaturelist = string_to_list(signaturestr)
                if signaturelist.contains(parameters['owner']):
                    return "You already signed this, silly."
                signaturelist.append(str(parameters['owner']))
                setattr(ri, 'content', list_to_string(signaturelist))
                ri.save()
            except Exception as e:
                ri = RandomInfo(name=name, content=str(parameters['owner']))
                ri.save()
            return "You have signed this mafia counter. Congrats!"
        elif parameters['action'].lower()=='check signatures':
            try:
                return "You have checked what people have signed this counter. It was the set of {"+RandomInfo.objects.get(name=name).content+'}.'
            except Exception as e:
                return str(e)
                return "You tried to check what signatures were on this counter. Unfortunately, no one has ever signed this."
        elif parameters['action'].lower()=='clear signatures':
            si = RandomInfo.objects.filter(name=name)
            for s in si:
                si.delete()
            return "All done!"


class shovel():
    questions = {
            'target':('Who are you shoveling?', 'str'),
            }
    @staticmethod
    def use(parameters):
        name = 'Shovel Handle with '+str(parameters['target'])+' inscribed'
        make_itemtype(name)
        make_item(name, parameters['owner'])
        role = get_att('Role', parameters['target'])
        alignment = get_att('Alignment', parameters['target'])
        return 'You have shoveled '+str(parameters['target'])+'. You uncover a piece of paper that tells you that their role is '+role+' and their alignment lies with '+alignment
    
class spiritsearch():
    questions = {
            'death':('Whose death are you investigating?', 'str'),
            'group':('Who participated in the ritual?', 'UserMult'),
            }
    @staticmethod
    def use(parameters):
        g = parameters['group']
        learner = random.choice(g)

        try:
            tracker = RandomInfo.objects.get(name="SpiritSearch"+str(parameters['self'].id))
        except:
            tracker = RandomInfo(name="SpiritSearch"+str(parameters['self'].id), content="")
            tracker.save()
        number = len(tracker.content)
        if number >= 2:
            response = random.choice(['not guilty', 'guilty'])

        else:
            response = 'not guilty'
            for user in g:
                if is_guilty(user, parameters['death']):
                    response = 'guilty'
        write_message('From the Spirit Search you just participated in, you have learned that someone in your party was '+response+" for "+parameters['death']+"'s death.", learner)
        setattr(tracker, 'content', tracker.content+'I')
        return "You have used a Spirit Search on"+parameters['death']+"'s death. Someone in your group has learned something. Check everyone's messages!"


############################# GM METHODS ##############################
class GM():
    @staticmethod
    def clearvotes():
        clearattribute('Voted For')
        return 'All the votes have been reset'
        
    @staticmethod
    def countvotes():
        answer = ""
        a = Attribute.objects.get(name='Voted for')
        ai = AttributeInstance.objects.filter(itype=a)
        for user in User.objects.all():
            count = ai.filter(value=user.username).count()
            if count > 0:
                answer = answer+user.username+': '+str(count)+'<br>'
        return answer
    @staticmethod
    def clearRBTase():
        clearattribute('Roleblocked')
        clearattribute('Tased')
        return 'All done!'
