import uuid
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	name = models.CharField(max_length=200)
	rules = models.TextField(blank=True)

	def __str__(self):
		return self.name

class Profile(models.Model):
	# Each User has exactly one Profile, and vice versa.
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	recieveEmails = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

class GM(models.Model):
	# Each GM is controlled by one User, and is part of one Game.
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Player(models.Model):
	# Each Player is controlled by one User, and is part of one Game.
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Condition(models.Model):
	name = models.CharField(max_length=200)
	condition_description = models.TextField(default="This is where you enter the trigger condition description.", blank=True)

	# Each Condition is part of one Game.
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

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

	# Each Item is part of one Game, can have many Owners, and can have many Triggers.
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	owners = models.ManyToManyField(Player, related_name='items')
	triggers = models.ManyToManyField(Condition, through='Trigger', through_fields=('item', 'condition'))

	def __str__(self):
		return self.name

class Trigger(models.Model):
	# Each Trigger is associated with one Item and one Condition, has one Effect when triggered, and can store arbitrary data.
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
	effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
	data = models.TextField(default="{}")

	def __str__(self):
		# Triggers are represented here as "[Item] | [Condition]: [Effect]"
		return item.name + " | " + condition.name + ": " + effect.name