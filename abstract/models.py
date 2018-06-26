from django.db import models

# Create your models here.
class Alignment(models.Model):
    name = models.CharField(max_length=200, default="Alignment")
    description = models.TextField(default="Description")

    def __str__(self):
        return self.name
    
class Action(models.Model):
    #game = models.ForeignKey(Game)
    name = models.CharField(max_length=200, default="Item")
    description = models.TextField(default="Description")
    effect = models.ManyToManyField('Attribute')

    def __str__(self):
        return self.name

class Item(Action):
    pass

class Ability(Action):
    pass

class Attribute(models.Model):
    #game = models.ForeignKey(Game)
    name = models.CharField(max_length=200, default="Status")
    description = models.TextField(default="Description")

    def __str__(self):
        return self.name

class Goal(models.Model):
    #game = models.ForeignKey(Game)
    name = models.CharField(max_length=200, default="Goal")
    description = models.TextField(default="Description")

    def __str__(self):
        return self.name
