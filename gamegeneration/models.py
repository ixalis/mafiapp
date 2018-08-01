from django.db import models
from django.contrib.auth.models import User, Group, Permission
import datetime
from django.core.mail import EmailMessage
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

############# Abstract Game concepts ##############
class Base(models.Model):
    """
    Parent class for all other base things in a given game. 
    """
    class Meta:
        abstract = True

    #Fields for descripion/name
    name = models.CharField(max_length=200, default="Name", unique=True)
    short_description = models.CharField(max_length=200, default="This is where you enter a mini blurb", blank = True)
    long_description = models.TextField(default="This is where you enter rules.", blank=True)

    def __str__(self):
        return self.name

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
        except:
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
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recieveEmails = models.BooleanField(default=False)
    currentPlayer = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True, blank=True)

############## Defining/Generating a Game #############
class Game(models.Model):
    """
    Defines a game within the website
    """

    name = models.CharField(max_length=200, default="Game", unique=True)
    items = models.ManyToManyField(Item, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)
    rules = models.CharField(max_length=2047, blank=True)
    attributes = GenericRelation('Attribute')
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attributes = GenericRelation('Attribute')
    game = models.ForeignKey(Game)

    def __str__(self):
        return self.user.username

######### Game Management ###########
class Attribute(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    element = GenericForeignKey('content_type', 'object_id')
    
    name = models.CharField(max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField(max_length=1000, default='')
    itype = models.CharField(max_length=100, default='str')
    default = models.CharField(max_length=100, default='',null=True, blank=True)

    alwaysVisible = models.BooleanField(default=True)
    strangeVisible = models.BooleanField(default=False)

    def visible(self):
        return True



class ActionInstance(models.Model):
    """
    Base class for Items and Abilities
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True) 
    class Meta:
        abstract = True

    def __str__(self):
        return '{0} ({1})'.format(self.owner, self.itype.name)
    def use(self, parameters=None):
        parameters['itype']= self.itype
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
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    itype = models.ForeignKey(Item, on_delete=models.CASCADE)
    attributes = GenericRelation(Attribute)
    
    def transfer(self, newowner):
        self.owner = newowner
        self.save()
        return "You have successfully transfered the item "+self.itype.name

class AbilityInstance(ActionInstance):
    """
    An instance of an ability
    """
    itype = models.ForeignKey(Ability, on_delete=models.CASCADE)
    owner = models.ManyToManyField(Player)

class Message(models.Model):
    """
    A message, to be saved
    """
    addressee = models.ForeignKey(Player)    
    content = models.TextField(default="Please contact GMs")
    deliverytime = models.DateTimeField(auto_now_add=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

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
            e.send()
            try:
                e2 = EmailMessage('New Mafia Occurrence', self.content, to=[self.addressee.email])
                e2.send()
            except:
                pass
        super(Message, self).save(*args, **kwargs)
