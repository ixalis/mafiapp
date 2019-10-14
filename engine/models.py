import uuid
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	name = models.CharField(max_length=200)
	rules = models.TextField(blank=True)
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	recieveEmails = models.BooleanField(default=False)
	currentPlayer = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.user.username

class Player(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Condition(models.Model):
	name = models.CharField(max_length=200)
	condition_description = models.TextField(default="This is where you enter the trigger condition description.", blank=True)

	def __str__(self):
		return self.name

class Effect(models.Model):
	name = models.CharField(max_length=200)
	effect_description = models.TextField(default="This is where you enter the effect description.", blank=True)

	def __str__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=200)
	short_description = models.CharField(max_length=200, default="This is where you enter an item description.", blank=True)
	long_description = models.TextField(default="This is where you enter long rules text.", blank=True)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	owners = models.ManyToManyField(Player)
	triggers = models.ManyToManyField(Condition, through='Trigger', through_fields=('item', 'condition'))

	def __str__(self):
		return self.name

class Trigger(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
	effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
	data = models.TextField(default="{}")

	def __str__(self):
		return item.name + " | " + condition.name + ": " + effect.name