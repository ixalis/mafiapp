from gamegeneration.models import *
def all():
    initializebase()
    initializeplayers()
    initializeinstance()
def initializebase():
    base = [
        Item(name='Mint', description='Generate some not-games.'),
        Item(name='Coin', description='Um, What?'),
        Item(name='Taser', description='Defend thyself, or something.'),
        Item(name='Taser Handle', description='You have already done all you can'),
        Item(name='Flower', description='Proof of your lesbianism.'),
        Item(name='Honey Jar', description='BEEEEEEEEEEEEEEEEEEEES'),
        Item(name='Mafia Counter', description='With enough signatures, can be used to count the living mafia'),
        Item(name='Shovel', description='Respect the dead!'),
        Item(name='Spirit Search', description='None of you are guilty, right? RIGHT?!'),
        Ability(name='Lynch Vote', description='Can you find the mafia?'),
        Ability(name='Kill', description='Congrats! You can kill someone.'),
        Ability(name='Pair Investigation', description='Awww, jealousy is cute.'),
        Ability(name='Trap', description='i know your secrets.'),
        Ability(name='Pickpocket', description='butterfingers'),
        Ability(name='Priest Sets', description='bless you'),
        Ability(name='Admire', description='i <3 u 2'),
        Ability(name='Roleblock', description='You did not have any plans, right?'),
        Ability(name='Planeswalk', description='ooOOOHHHH..... what do zombies even sound like?'),
        
        Attribute(name='Voted for', description='Wow, you really hate them.', atype='str', default='None'),
        Attribute(name='Alive', description='You are still alive, darn.', atype='boolean', default='True'),
        Attribute(name='Roleblocked', description='Are you even useful anymore?', atype='boolean', default='False'),
        Attribute(name='Splashed', description='spooky', atype='boolean', default='False'),
        ]
    for thing in base:
        thing.save()

def initializeplayers():
    players = [
        User(username='player1', password='password'),
        User(username='player2', password='password'),
        ]
    for thing in players:
        thing.save()

def initializeinstance():
    instances = [
        ItemInstance(itype=Item.objects.get(name='Coin'), owner=User.objects.get(username='player1')),
        ItemInstance(itype=Item.objects.get(name='Taser'), owner=User.objects.get(username='player2')),
        ItemInstance(itype=Item.objects.get(name='Honey Jar'), owner=User.objects.get(username='player1')),
        AbilityInstance(itype=Ability.objects.get(name='Lynch Vote'), owner=User.objects.get(username='player1')),
        AbilityInstance(itype=Ability.objects.get(name='Lynch Vote'), owner=User.objects.get(username='player2')),
        AbilityInstance(itype=Ability.objects.get(name='Kill'), owner=User.objects.get(username='player1')),
        ]
    for thing in instances:
        thing.save()
    for att in Attribute.objects.all():
        for user in User.objects.all():
            atti = AttributeInstance(itype=att, owner=user, value=att.default)
            atti.save()
if __name__=='__main__':
    all()
