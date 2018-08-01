from gamegeneration.models import *
from django.contrib.auth.models import User
def all():
    initializeVanilla()
    initializeplayers()
    initializexgame()
def initializeVanilla():
    game = Game(name='Vanilla');
    game.save()
    base = [

        Item(name='Mint', description='Generate some not-games.'),
        Item(name='Coin', description='Um, What?'),
        Item(name='Taser', description='Defend thyself, or something.'),
        Item(name='Flower', description='Proof of your lesbianism.'),
        Item(name='Honey Jar', description='BEEEEEEEEEEEEEEEEEEEES'),
        Item(name='Mafia Counter', description='With enough signatures, can be used to count the living mafia'),
        Item(name='Shovel', description='Respect the dead!'),
        Item(name='Spirit Search', description='None of you are guilty, right? RIGHT?!'),
        Item(name='Shovel Handle', description='Respect the Dead!'),
        Item(name='Taser Handle', description='Electrify first, talk later'),

        Ability(name='Lynch Vote', description='Can you find the mafia?'),
        Ability(name='Kill', description='Congrats! You can kill someone.'),
        Ability(name='Pair Investigation', description='Awww, jealousy is cute.'),
        Ability(name='Trap', description='i know your secrets.'),
        Ability(name='Pickpocket', description='butterfingers'),
        Ability(name='Priest Sets', description='bless them'),
        Ability(name='Admire', description='i <3 u 2'),
        Ability(name='Roleblock', description='You did not have any plans, right?'),
        Ability(name='Planeswalk', description='ooOOOHHHH..... what do zombies even sound like?'),
        Ability(name='Set Investigation', description="Those cards don't match!"),
        Ability(name='Splitter Sets', description="Pick one already."),
        Ability(name='Vigilante Kill', description="Prowling the streets"),
        Ability(name='Scheme Kill', description="Plan ahead"),

        #iAttribute(name='Voted for', description='Wow, you really hate them.', atype='str', default='None', alwaysvisible='True'),
        #Attribute(name='Dead', description='You are still alive, darn.', atype='boolean', default='True'),
        #Attribute(name='Roleblocked', description='Are you even useful anymore?', atype='boolean', default='False'),
        #Attribute(name='Splashed', description='spooky', atype='boolean', default='False'),
        #Attribute(name='Tased', description='bzzzzzzzzzz', atype='boolean', default='False'),
        #Attribute(name='Alignment', description="I'm not mafia, you are!", atype='str', default='Town', alwaysvisible='True'),
        #Attribute(name='Role', description='You had one job.', atype='str', default='Vanilla', alwaysvisible='True'),

        #Attribute(name='Roleblockee', description="Hope they didn't have any plans", default='None'),
        #Attribute(name='Admiring', description="That sweet-talker", atype='User', default='None'),
        #Attribute(name='Priest Sets', description="Bless you", atype='str', default='None'),
        #Attribute(name='Trapped', description="someone knows your secret", default='None'),
        #Attribute(name='Planeswalker points', description="You've eaten some tasy brains", default='0'),

        ]
    for thing in base:
        thing.save()

def initializeplayers():
    players = [
        User.objects.create_user(username='town1', password='password'),
        User.objects.create_user(username='town2', password='password'),
        User.objects.create_user(username='town3', password='password'),
        User.objects.create_user(username='town4', password='password'),
        User.objects.create_user(username='town5', password='password'),
        User.objects.create_user(username='mafia1', password='password'),
        User.objects.create_user(username='mafia2', password='password'),
        User.objects.create_user(username='mafiask', password='password'),
        ]
    for thing in players:
        thing.save()

def initializexgame():
    vanilla = Game.objects.get(name='Vanilla')
    instances = [
        ItemInstance(itype=Item.objects.get(name='Coin'), owner=User.objects.get(username='town1')),
        ItemInstance(itype=Item.objects.get(name='Taser'), owner=User.objects.get(username='town2')),
        ItemInstance(itype=Item.objects.get(name='Honey Jar'), owner=User.objects.get(username='mafia1')),
        ItemInstance(itype=Item.objects.get(name='Coin'), owner=User.objects.get(username='town3')),
        ItemInstance(itype=Item.objects.get(name='Spirit Search'), owner=User.objects.get(username='town3')),
        ItemInstance(itype=Item.objects.get(name='Shovel'), owner=User.objects.get(username='town4')),
        ItemInstance(itype=Item.objects.get(name='Flower'), owner=User.objects.get(username='town4')),
        ItemInstance(itype=Item.objects.get(name='Flower'), owner=User.objects.get(username='mafia1')),
        ItemInstance(itype=Item.objects.get(name='Mafia Counter'), owner=User.objects.get(username='mafia2')),
        ItemInstance(itype=Item.objects.get(name='Taser'), owner=User.objects.get(username='mafiask')),
        


        AbilityInstance(itype=Ability.objects.get(name='Kill'), owner=User.objects.get(username='mafia1')),
        AbilityInstance(itype=Ability.objects.get(name='Kill'), owner=User.objects.get(username='mafia2')),
        AbilityInstance(itype=Ability.objects.get(name='Kill'), owner=User.objects.get(username='mafiask')),
        AbilityInstance(itype=Ability.objects.get(name='Pickpocket'), owner=User.objects.get(username='town1')),
        AbilityInstance(itype=Ability.objects.get(name='Roleblock'), owner=User.objects.get(username='town2')),
        AbilityInstance(itype=Ability.objects.get(name='Admire'), owner=User.objects.get(username='town3')),
        AbilityInstance(itype=Ability.objects.get(name='Pair Investigation'), owner=User.objects.get(username='town4')),
        AbilityInstance(itype=Ability.objects.get(name='Pickpocket'), owner=User.objects.get(username='town5')),
        AbilityInstance(itype=Ability.objects.get(name='Roleblock'), owner=User.objects.get(username='mafia1')),
        AbilityInstance(itype=Ability.objects.get(name='Priest Sets'), owner=User.objects.get(username='mafia2')),
        AbilityInstance(itype=Ability.objects.get(name='Pickpocket'), owner=User.objects.get(username='mafiask')),


        ]
    for thing in instances:
        thing.save()
    for user in User.objects.all():
        #for att in Attribute.objects.all():
        #    atti = AttributeInstance(itype=att, owner=user, value=att.default)
        #    atti.save()
        ai = AbilityInstance(itype=Ability.objects.get(name='Lynch Vote'), owner=user)
        ai.save()
if __name__=='__main__':
    all()
