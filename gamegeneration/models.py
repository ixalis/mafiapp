from django.db import models
from django.contrib.auth.models import User
import methods
import inspect

#Abstract Game concepts
class Action(models.Model):
    name = models.CharField(max_length=200, default="")
    description = models.TextField(default="Description")

    def __str__(self):
        return self.name

    def get_description(self):
        return self.description
    def set_description(self, text):
        self.description = text

    def get_methodname(self, text):
        return self.methodname
    def set_methodname(self, text):
        self.methodname = text

class Item(Action):
    def methodname(self):
        return 'use'+self.name

class Ability(Action):
    def methodname(self):
        return 'activate'+self.name

class Attribute(models.Model):
    name = models.CharField(max_length=200, default="Status")
    description = models.TextField(default="Description")

    def __str__(self):
        return self.name
    def get_description(self):
        return self.description

#Defining/Generating a Game
class Game(models.Model):
    name = models.CharField(max_length=200, default="Game")
    items = models.ManyToManyField(Item, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)
    players = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

#Actual Game management
class Instance(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)

    def __str__(self):
        return '{0} ({1})'.format(self.owner, self.itype.name)

class ActionInstance(Instance):


    def use(self, parameters=None):
        methodname = self.itype.methodname()
        method_to_call = getattr(methods, methodname)
        if parameters:
            result = method_to_call(parameters)
        else:
            result = method_to_call()
        return result

    def get_requests(self):
        requestname = 'question'+self.itype.name
        requests = getattr(methods, requestname)
        return requests


class ItemInstance(ActionInstance):
    itype = models.ForeignKey(Item)

    def transfer(self, newowner):
        self.owner = newowner

class AbilityInstance(ActionInstance):
    itype = models.ForeignKey(Ability)
    usable = models.BooleanField(default=True)

class AttributeInstance(Instance):
    itype = models.ForeignKey(Attribute)
    value = models.IntegerField(default = 1)
