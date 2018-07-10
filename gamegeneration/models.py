from django.db import models
from django.contrib.auth.models import User
import datetime

############# Abstract Game concepts ##############
class Base(models.Model):
    """
    Parent class for all other base things in a given game. 
    """
    class Meta:
        abstract = True

    #Fields for descripion/name
    name = models.CharField(max_length=200, default="Name")
    description = models.TextField(default="This is where you enter a description.", blank = True)

    def __str__(self):
        return self.name

    #Get/Set functions
    def get_description(self):
        return self.description
    def set_description(self, text):
        self.description = text
    def get_name(self):
        return self.name
    def set_name(self, text):
        self.name = text

class Item(Base):
    """
    Defines items in the game
    """
    def get_usemethod(self):
        """
        Returns method defining use function for this item
        """
        import methods
        methodname = 'use'+self.name.replace(" ", "").lower()
        method = getattr(methods, methodname)
        return method
    def get_usequestions(self):
        """
        Returns questions to be asked when using this ability, in the form
        {'field':(question, answertype), }
        """
        import methods
        name = 'question'+self.name.replace(" ", "").lower()
        questions = getattr(methods, name)
        return questions



class Ability(Base):
    """
    Defines Abilities in game
    """
    def get_usemethod(self):
        """
        Returns method defining use function for this abliity
        """
        import methods
        methodname = 'activate'+self.name.replace(" ", "").lower()
        method = getattr(methods, methodname)
        return method
    def get_usequestions(self):
        """
        Returns questions to be asked when using this ability, in the form 
        {'field':(question, answertype), }
        """
        import methods
        name = 'question'+self.name.replace(" ", "").lower()
        questions = getattr(methods, name)
        return questions

class Attribute(Base):
    """
    Defines Individual attributes/characteristics of Items, Abilities, or Users that can be quantified.
    """
    pass




############## Defining/Generating a Game #############
class Game(models.Model):
    """
    Defines a game within the website
    """

    name = models.CharField(max_length=200, default="Game")
    #Allows the creator to pick what items and abilities to include in the game. Can be None
    items = models.ManyToManyField(Item, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)
    #Defines what players are playing this game. Can be none
    players = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    #Get functions
    def get_items(self):
        return self.items
    def get_abilities(self):
        return self.abilities
    def get_players(self):
        return self.players

    #Add functions
    def add_item(self, item):
        self.items.add(item)
    def add_ability(self, ability):
        self.abilities.add(ability)
    def add_player(self, player):
        self.players.add(player)




######### Game Management ###########
class Instance(models.Model):
    """
    Base Class for all instances. Defines an owner for each instance, and which game it belongs to.
    """
    class Meta:
        abstract = True

    owner = models.ForeignKey(User)
    #game = models.ForeignKey(Game)

    def __str__(self):
        return '{0} ({1})'.format(self.owner, self.itype.name)
    
    #Get functions
    def get_owner(self):
        return self.owner
    #def get_game(self):
    #    return self.game
    def get_itype(self):
        return self.itype


class ActionInstance(Instance):
    """
    Base class for Items and abilities
    """
    class Meta:
        abstract = True
    def use(self, parameters=None):
        parameters['owner'] = self.get_owner()
        method_to_call = self.itype.get_usemethod()
        if parameters:
            result = method_to_call(parameters)
        else:
            result = method_to_call()
        return result

    def get_requests(self):
        questions = self.itype.get_usequestions()
        return questions


class ItemInstance(ActionInstance):
    """
    An instance of a single item
    """
    itype = models.ForeignKey(Item)

class AbilityInstance(ActionInstance):
    """
    An instance of an ability
    """
    itype = models.ForeignKey(Ability)

class AttributeInstance(Instance):
    """
    An instance of an attribute
    """
    itype = models.ForeignKey(Attribute)
    value = models.IntegerField(default = 0)

class Message(models.Model):
    """
    A message, to be saved
    """
    addressee = models.ForeignKey(User)
    content = models.CharField(max_length=1000)
    deliverytime = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        ordering = ['deliverytime']
    def __str__(self):
        return "(" + "{:%H:%M:%S}".format(self.deliverytime) +") "+self.content

    def get_addressee(self):
        return self.addresee
    def get_content(self):
        return self.content
    def get_time(self):
        return self.deliverytime

