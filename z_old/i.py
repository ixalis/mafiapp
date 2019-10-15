from gamegeneration.models import *
from django.contrib.auth.models import User
def all():
    initializeVanilla()
    initializeplayers()
    initializexgame()
    initializeAttributes()
def initializeVanilla():
    game = Game(name='Vanilla');
    game.save()
    base = [

        Item(name='Mint', short_description='Generate some not-games.'),
        Item(name='Coin', short_description='Um, What?'),
        Item(name='Taser', short_description='Defend thyself, or something.'),
        Item(name='Flower', short_description='Proof of your lesbianism.'),
        Item(name='Honey Jar', short_description='BEEEEEEEEEEEEEEEEEEEES'),
        Item(name='Mafia Counter', short_description='With enough signatures, can be used to count the living mafia'),
        Item(name='Shovel', short_description='Respect the dead!'),
        Item(name='Spirit Search', short_description='None of you are guilty, right? RIGHT?!'),
        Item(name='Shovel Handle', short_description='Respect the Dead!'),
        Item(name='Taser Handle', short_description='Electrify first, talk later'),

        Ability(name='Lynch Vote', short_description='Can you find the mafia?'),
        Ability(name='Kill', short_description='Congrats! You can kill someone.'),
        Ability(name='Pair Investigation', short_description='Awww, jealousy is cute.'),
        Ability(name='Trap', short_description='i know your secrets.'),
        Ability(name='Pickpocket', short_description='butterfingers'),
        Ability(name='Priest Sets', short_description='bless them'),
        Ability(name='Admire', short_description='i <3 u 2'),
        Ability(name='Roleblock', short_description='You did not have any plans, right?'),
        Ability(name='Planeswalk', short_description='ooOOOHHHH..... what do zombies even sound like?'),
        Ability(name='Set Investigation', short_description="Those cards don't match!"),
        Ability(name='Splitter Sets', short_description="Pick one already."),
        Ability(name='Vigilante Kill', short_description="Prowling the streets"),
        Ability(name='Scheme Kill', short_description="Plan ahead"),

        #iAttribute(name='Voted for', short_description='Wow, you really hate them.', atype='str', default='None', alwaysvisible='True'),
        #Attribute(name='Dead', short_description='You are still alive, darn.', atype='boolean', default='True'),
        #Attribute(name='Roleblocked', short_description='Are you even useful anymore?', atype='boolean', default='False'),
        #Attribute(name='Splashed', short_description='spooky', atype='boolean', default='False'),
        #Attribute(name='Tased', short_description='bzzzzzzzzzz', atype='boolean', default='False'),
        #Attribute(name='Alignment', short_description="I'm not mafia, you are!", atype='str', default='Town', alwaysvisible='True'),
        #Attribute(name='Role', short_description='You had one job.', atype='str', default='Vanilla', alwaysvisible='True'),

        #Attribute(name='Roleblockee', short_description="Hope they didn't have any plans", default='None'),
        #Attribute(name='Admiring', short_description="That sweet-talker", atype='User', default='None'),
        #Attribute(name='Priest Sets', short_description="Bless you", atype='str', default='None'),
        #Attribute(name='Trapped', short_description="someone knows your secret", default='None'),
        #Attribute(name='Planeswalker points', short_description="You've eaten some tasy brains", default='0'),

        ]
    for thing in base:
        thing.save()

def initializeplayers():
    vanilla = Game.objects.get(name='Vanilla')
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
    for user in User.objects.all():
        player = Player(user=user, game=vanilla)
        player.save()
        p = Profile(user=user, currentPlayer=player)
        p.save()
        
def initializexgame():
    vanilla = Game.objects.get(name='Vanilla')
    instances = [
        ItemInstance(itype=Item.objects.get(name='Coin'), owner=User.objects.get(username='town1').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Taser'), owner=User.objects.get(username='town2').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Honey Jar'), owner=User.objects.get(username='mafia1').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Coin'), owner=User.objects.get(username='town3').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Spirit Search'), owner=User.objects.get(username='town3').profile.currentPlayer, game= vanilla),
        ItemInstance(itype=Item.objects.get(name='Shovel'), owner=User.objects.get(username='town4').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Flower'), owner=User.objects.get(username='town4').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Flower'), owner=User.objects.get(username='mafia1').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Mafia Counter'), owner=User.objects.get(username='mafia2').profile.currentPlayer, game=vanilla),
        ItemInstance(itype=Item.objects.get(name='Taser'), owner=User.objects.get(username='mafiask').profile.currentPlayer, game=vanilla),
    ]
    abilities = [
        AbilityInstance(itype=Ability.objects.get(name='Kill'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Kill'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Kill'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Pickpocket'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Roleblock'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Admire'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Pair Investigation'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Pickpocket'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Roleblock'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Priest Sets'), game=vanilla),
        AbilityInstance(itype=Ability.objects.get(name='Pickpocket'), game=vanilla),

        ]
    for thing in instances:
        thing.save()
    for thing in abilities:
        thing.save()
        thing.owner.add(User.objects.get(username='town1').profile.currentPlayer)
    for user in User.objects.all():
        ai = AbilityInstance(itype=Ability.objects.get(name='Lynch Vote'), game=vanilla)
        ai.save()
        thing.owner.add(user.profile.currentPlayer)
def initializeAttributes():
    vanilla = Game.objects.get(name='Vanilla')
    attributes = [
            Attribute(name='GM', element=User.objects.get(username='admin').profile.currentPlayer, value='True', game=vanilla, alwaysVisible=True)
    ]
    for thing in attributes:
        thing.save()
if __name__=='__main__':
    all()
