from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.mail import EmailMessage
#import methods

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
        try:
            method = getattr(methods, self.name.replace(" ", "").lower()).use
        except AttributeError:
            method = getattr(methods, 'default').use
        return method
    def get_usequestions(self):
        """
        Returns questions to be asked when using this ability, in the form
        {'field':(question, answertype), }
        """
        import methods
        try:
            questions = getattr(methods, self.name.replace(" ", "").lower()).questions
        except AttributeError:
            questions = getattr(methods, 'default').questions
        return questions
    def get_usetext(self):
        """
        Returns description for Use Form
        """
        import methods
        try:
            description = getattr(methods, self.name.replace(" ","").lower()).description
        except AttributeError:
            description = getattr(methods, 'default').description
        return description




class Ability(Base):
    """
    Defines Abilities in game
    """
    def get_usemethod(self):
        """
        Returns method defining use function for this abliity
        """
        import methods
        try:
             method = getattr(methods, self.name.replace(" ", "").lower()).activate
        except AttributeError:
            method = getattr(methods, 'default').activate
        return method
    def get_usequestions(self):
        """
        Returns questions to be asked when using this ability, in the form 
        {'field':(question, answertype), }
        """
        import methods
        try:
            questions = getattr(methods, self.name.replace(" ","").lower()).questions
        except AttributeError:
            questions = getattr(methods, 'default').questions
        return questions
    def get_usetext(self):
        """
        Return descripion for use form
        """
        import methods
        try:
            description = getattr(methods, self.name.replace(" ","").lower()).description
        except AttributeError:
            description = getattr(methods, 'default').description
        return description

class Attribute(Base):
    """
    Defines Individual attributes/characteristics of Users that can be quantified.
    """
    atype = models.CharField(max_length=200, default="str")
    default = models.CharField(max_length=200, default="str")
    alwaysvisible = models.BooleanField(max_length=200, default=False)
    nondefaultvisible = models.BooleanField(max_length=200, default=True)
    def get_atype(self):
        return self.atype
    def set_atype(self, v):
        self.atype = v

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

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{0} ({1})'.format(self.owner, self.itype.name)
    
    #Get functions
    def get_owner(self):
        return self.owner
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
        parameters['itype']= self.get_itype()
        parameters['self'] = self
        method_to_call = self.itype.get_usemethod()
        if parameters:
            result = method_to_call(parameters)
        else:
            result = method_to_call()
        return result

    def get_requests(self):
        questions = self.itype.get_usequestions()
        return questions
    def get_usetext(self):
        return self.itype.get_usetext()


class ItemInstance(ActionInstance):
    """
    An instance of a single item
    """
    itype = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def transfer(self, newowner):
        self.owner = newowner
        return "You have successfully transfered the item "+self.itype.name

class AbilityInstance(ActionInstance):
    """
    An instance of an ability
    """
    itype = models.ForeignKey(Ability, on_delete=models.CASCADE)
class AttributeInstance(Instance):
    """
    An instance of an attribute
    """
    itype = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=1000, default = '0')

class Message(models.Model):
    """
    A message, to be saved
    """
    addressee = models.ForeignKey(User, on_delete=models.CASCADE)
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
    def save(self, *args, **kwargs):
        if not self.pk:
            e = EmailMessage('New Mafia Occurrence', self.content, to=['mafiapp31415@gmail.com'])
            #e.send()
            if self.addressee.email:
                e2 = EmailMessage('New Mafia Occurrence', self.content, to=[self.addressee.email])
                #e2.send()
        super(Message, self).save(*args, **kwargs)

class RandomInfo(models.Model):
    """
    Storing random bits of information
    """
    name = models.CharField(max_length=50, default='Default')
    content = models.CharField(max_length=9999, default='')

    def __str__(self):
        return self.content

