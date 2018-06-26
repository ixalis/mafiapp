from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(ItemInstance)
admin.site.register(AbilityInstance)
admin.site.register(AttributeInstance)
admin.site.register(GoalInstance)
