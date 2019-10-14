#from django.contrib.auth.models import User
from gamegeneration.models import *
import random
from django.db.models import Q
from functools import reduce 

################################ DJANGO INTERACTION METHODS ###############################
def user(username):
    return User.objects.get(username=username)

def get_att(name, element):
    try:
        a = Attribute.objects.filter(element=element).get(name=name)
        return a.value
    except:
        return None

def set_att(name, element, value, itype='str', default='', alwaysVisible=False, strangeVisible=False, game=Game.objects.get(name='Vanilla')):
    try:
        
        a = element.attributes.get(name=name)
        setattr(a, 'value', value)
        a.save()
    except:
        a = Attribute(name=name, element=element, value=value, itype=itype, default=default, alwaysVisible=alwaysVisible, strangeVisible=strangeVisible, game=game)
        a.save()

def make_item(itype, owner):
    game = Game.objects.get(name='Vanilla')
    item = ItemInstance(itype=Item.objects.get(name=itype), owner=owner, game=game)
    item.save()
    return item

def write_message(message, addressee, game):
    m = Message(addressee=addressee, content=message, game=game)
    m.save()

######################################### HELPER METHODS #########################################
def is_guilty(target, death):
    try:
        a = Attribute.objects.filter(name=str(target)+'Guilty').get(owner=death) 
        if a.value == 'True':
            return True
        return False
    except:
        return False

def string_to_list(string):
    return string.split(',')
def list_to_string(l):
    final = ""
    for i in l:
        final = final+i+","
    return final[:-1]

def count_mafia():
    a = Attribute.objects.filter(name='Alignment').filter(value='mafia').count()
    return a
def genability(name, user):
    a = Ability.objects.get(name=name)
    ai = AbilityInstance(itype=a, owner=user)
    ai.save()


########################################## ABILITIES #############################################
class default():
    questions = {
            'input':('textbox', 'str'),
            }
    description = ""
    @staticmethod
    def use(parameters):
        return "You have used the item " + str(parameters['itype']) + ". <br> GMs have been notified."
    @staticmethod
    def activate(parameters):
        return "You have used the ability " + str(parameters['itype']) + ".<br> GMs have been notified."

class kill():
    questions = {
            'target':('Who did you kill?', 'User'),
            'time':('When did you kill them?', 'time'),
            'place':('Where did this murder take place?', 'str'),
            'pleadguilty':('Did the target plead guilty?', 'boolean'),
            }

    @staticmethod
    def activate(parameters):
        if parameters['pleadguilty'].lower() == 'yes':
            return "You have attempted to kill {1}, at {2} and {3}, but they plead guilty.".format(parameters['target'], parameters['time'], parameters['place'])
        set_att('Alive', parameters['target'], 'False')
        for u in User.objects.all():
            set_att(str(parameters['target'])+'Guilty', itype='boolean', value='False')
        set_att(str(parameters['target'])+'Guilty',parameters['owner'], 'True', alwaysvisible=True)
        parameters['self'].delete()
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
        parameters['self'].delete()
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
        name = str(target1)+','+str(target2)+','+str(targetdeath)
        try:
            ri = RandomInfo.objects.get(name = name)
            result = ri.content
        except:
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
            ri = RandomInfo(name=name,content=str(result))
            ri.save()
        parameters['self'].delete()
        return "You have investigated "+str(target1)+ " and "+str(target2)+". and and heard about"+str(result)+ " as a possible suspect."

class admire():
    questions = {
        'target': ('Who are you admiring?', 'User'),
        }
    @staticmethod
    def activate(parameters):
        set_att('Admiring', parameters['owner'], parameters['target'], alwaysVisible=True)
        return 'You successfully admired them!'


class roleblock(): 
    questions = {
        'target': ('Who are you roleblocking?', 'User'),
        }
    @staticmethod
    def activate(parameters):
        set_att('Roleblocking', parameters['owner'], parameters['target'], alwaysVisible=True)
        set_att('Roleblocked', parameters['target'], 'True', alwaysVisible=True)
        parameters['self'].delete()
        return 'You have successfully roleblocked them!'

class priestset():
    questions = {
            'set1':('Who is in your first set?', 'UserMult'),
            'set2':('Who is in your second set?', 'UserMult'),
            }
    @staticmethod
    def activate(parameters):
        set1, set2 = "", ""
        for u in parameters['set1']:
            set1 = set1+str(u)+','
        for u in parameters['set2']:
            set1 = set1+str(u)+','
        sett = set1[:-1]+'|'+set1[:-1]
        set_att('Priest Sets', parameters['owner'], sett, alwaysVisible=True)
        return 'You have successfully priested ' + sett.replace("|", " and ")

class setinvestigation():
    questions = {
            'sett':('Who do you want to investigate?', 'UserMult'),
            'death':('Whose death are you investigating?', 'User')
            }
    @staticmethod
    def activate(parameters):
        result = False
        death = parameters['death']
        for u in parameters['sett']:
            if is_guilty(u, death):
                result = True
        parameters['self'].delete()
        if result:
            return "Someone is guilty!"
        else:
            return "No one is guilty..."

class vigilantekill():
    questions = {
            'target':('Who did you kill?', 'User'),
            'time':('When did you kill them?', 'time'),
            'place':('Where did this murder take place?', 'str'),
            }
    @staticmethod
    def activate(parameters):
        kill.activate(parameters)
        alignment = get_att('Alignment', parameters['target'])
        result = "You have killed "+parameters['target']+' at '+parameters['time']+' and '+parameters['place']+' and learned that your target was '+alignment+'.'
        parameters['self'].delete()
        if alignment=='Town':
            return result+"You will die at the end of the day."
        else:
            return result
class planeswalk():
    questions = {
            'choice':('Pick what you want to do', ('Gain 2 points', 'Spend N points to get another role')),
            'role':('If you want to get another role, what role action would you like?', 'str'),
            }
    @staticmethod
    def activate(parameters):
        if parameters['choice']=='Gain 2 points':
            n = get_att('Planeswalker points', parameters['owner'])
            set_att('Planeswalker points', parameters['owner'], str(int(n)+2))
            parameters['self'].delete()
            return "You have successfully gained 2 planeswalker points!"
        elif parameters['choice']=='Spend N points to get another role': 
            return "Contact GMs please"
        else:
            return "Contact GMs please"
class trap():
    questions = {
        'target': ('Who are you trapping?', 'User'),
        'role': ('As what?', 'str'),
        }
    @staticmethod
    def activate(parameters):
        arole = get_att('Role', parameters['target'])
        splashed = get_att('Splashed', parameters['target'])
        if splashed == 'True' or parameters['role']==arole:
            set_att('Trapped', parameters['target'], 'True')
            return 'Your Trap has succeeded!'
        parameters[self].delete()
        return 'Your Trap has failed. Sorry!'


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
        i = make_item('Taser Handle', parameters['owner'])
        set_att('Tased', str(parameters['target']), 'True', alwaysVisble=True)
        set_att('Inscribed', i, parameters['target'])
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
        if parameters['action'].lower()=='use':
            signaturelist = get_att('Signatures', parameters['self'])
            if signaturelist is None:
                return "You tried to submit a mafia counter to the gods. Unfortunately, no one has ever signed this."
            slist = string_to_list(signaturelist)
            number = len(slist)
            if number > get_majority():
                return "You tried to submit a mafia counter to the gods. Unfortunately, you do not have enough signatures."
            else:
                learner = User.objects.get(username=random.choice(slist))
                mafianumber = count_mafia()
                write_message(addressee=learner, content="From the mafia counter you signed not too long ago, you learned that there exist "+mafianumber+" mafia in the world today.", game=parameters['owner'].game)
                parameters['self'].delete()
            return "You have successfully used your mafia counter. Tell everyone to check their messages!"
        elif parameters['action'].lower()=='sign':
            signatures = get_att('Signatures', parameters['self'])
            if signatures:
                signaturelist = string_to_list(signatures)
            else:
                signaturelist = []
            if signaturelist.contains(parameters['owner']):
                return "You already signed this, silly."
            signaturelist.append(str(parameters['owner']))
            set_att('Signatures', parameters['self'], list_to_string(signaturelist))
            return "You have signed this mafia counter. Congrats!"
        elif parameters['action'].lower()=='check signatures':
            try:
                return "You have checked what people have signed this counter. It was the set of {"+get_att('Signatures', parameters['self'])+'}.'
            except Exception as e:
                return str(e)
                return "There was an error. Contact GM's to know more"
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
        i = make_item('Shovel Handle', parameters['owner'])
        set_att('Inscribed', i, str(parameters['target']), alwaysVisible=True)
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
        number = get_att('SpiritSearch'+str(parameters['death'], 'Vanilla'))
        if number:
            number = int(number)
        else:
            number = 0
        if number >= 2:
            response = random.choice(['not guilty', 'guilty'])
        else:
            response = 'not guilty'
            for user in g:
                if is_guilty(user, parameters['death']):
                    response = 'guilty'
            set_att('SpiritSearch'+str(parameters['death']), 'Vanilla', str(number+1))
        write_message('From the Spirit Search you just participated in, you have learned that someone in your party was '+response+" for "+parameters['death']+"'s death.", learner, game=parameters['owner'].game)
        return "You have used a Spirit Search on"+parameters['death']+"'s death. Someone in your group has learned something. Check everyone's messages!"

############################# GM METHODS ##############################
class GM():
    @staticmethod
    def clearvotes():
        vf = Attribute.objects.filter(name='Voted For')
        for o in vf:
            o.delete()
        return 'All the votes have been reset'
        
    @staticmethod
    def countvotes():
        answer = ""
        a = Attribute.objects.filter(name='Voted for')
        for user in User.objects.all():
            count = a.filter(value=user.username).count()
            if count > 0:
                answer = answer+user.username+': '+str(count)+'<br>'
        return answer
    
    @staticmethod
    def clear1DayAbilities():

        names = ['Pickpocket', 'Kill', 'Pair Investigation', 'Roleblock', 'Set Investigation']
        queryset = AbilityInstance.objects.filter(reduce(lambda x, y: x | y, [Q(itype=Ability.objects.get(name=att)) for att in names]))
        for i in queryset:
            i.delete()
        return 'All Cleared!'

    @staticmethod
    def generateAbilities():
        rolers = []
        for i in Attribute.objects.filter(name='Role'):
            rolers.append((i.owner, i.value))
        atters = []
        for i in Attribute.objects.filter(name='Attribute'):
            atters.append((i.owner, i.value))

        for u in rolers:
            if u[1]=='Roleblocker':
                genability('Roleblock', u[0])
            elif u[1]=='Pickpocket':
                genability('Pickpocket', u[0])
            elif u[1]=='Pair Investigator':
                genability('Pair Investigation', u[0])
                genability('Pair Investigation', u[0])
        for u in atters:
            if u[1]=='Mafia':
                genability('Kill', u[0])
        return 'Generated'

    @staticmethod
    def clearAttributes():
        names = ['Roleblocked', 'Roleblocking', 'Admiring']
        queryset = Attribute.objects.filter(reduce(lambda x, y: x | y, [Q(name=att) for att in names]))
        for i in queryset:
            i.delete()
        return 'All Cleared!'
    @staticmethod
    def dayRollover():
        votes = GM.countvotes()
        GM.clearvotes()
        GM.clearAttributes()
        GM.clear1DayAbilities()
        GM.generateAbilities()
        return votes

    @staticmethod
    def resetRoleAttributeAlive():
        for p in User.objects.all():
            u = p.profile.currentPlayer
            set_att('Role', u, 'Vanilla Townie')
            set_att('Attribute', u, 'Town')
            set_att('Alive', u, 'True')
        return 'Roles, Attributes, and Alive Status reset'
