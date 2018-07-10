from gamegeneration.models import *
def initializebase():
    base = [
        Item(name='Mint', description='Generate some not-games.'),
        Item(name='Coin', description='Um, What?'),
        Item(name='Taser', description='Defend thyself, or something.'),
        Item(name='Flower', description='Proof of your lesbianism.'),
        Item(name='Honey Jar', description='BEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEES'),
        Ability(name='Lynch Vote', description='Can you find the mafia?'),
        Ability(name='Kill', description='Congrats! You can kill someone.'),
        Ability(name='Pair Investigation', description='Awww, jealousy is cute.'),
        Attribute(name='Voted for', description='Wow, you really hate them.'),
        Attribute(name='Alive', description='You are still alive, darn.'),
        Attribute(name='Roleblocked', description='Are you even useful anymore?'),
        Attribute(name='Splashed', description='spooky'),
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

def intializeinstance():
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
        atti = AttributeInstance(itype=att)
        atti.save()
