import uuid
from django.db import models

class Player(models.Model):
	username = models.CharField(primary_key=True, max_length=200, unique=True)
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)

	class Meta:
		ordering = ('username',)

	def __str__(self):
		return self.username

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
	owners = models.ManyToManyField(Player)
	triggers = models.ManyToManyField(Condition, through='Trigger', through_fields=('item', 'condition'))

	def __str__(self):
		return self.name

class Trigger(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
	effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
	data = models.TextField(default="{}")

	def __str__(self):
		return item.name + " | " + condition.name + ": " + effect.name