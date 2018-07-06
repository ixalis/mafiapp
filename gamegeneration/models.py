from django.db import models
from abstract.models import Item, Ability, Attribute, Goal
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200, default="Game")

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)

    def __str__(self):
        return self.user.username

class Instance(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)

    def __str__(self):
        return '{0} ({1})'.format(self.owner, self.itype.name)

class ItemInstance(Instance):
    itype = models.ForeignKey(Item)

class AbilityInstance(Instance):
    itype = models.ForeignKey(Ability)
    usable = models.BooleanField(default=True)

class AttributeInstance(Instance):
    itype = models.ForeignKey(Attribute)
    #value = models.CharField(max_length=200, default="value")
    value = models.IntegerField(default = 1)

class GoalInstance(Instance):
    itype = models.ForeignKey(Goal)
