from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Item)
admin.site.register(Ability)
admin.site.register(ItemInstance)
admin.site.register(AbilityInstance)
admin.site.register(PlayerAttributeInstance)
admin.site.register(ItemAttributeInstance)
admin.site.register(GameAttributeInstance)
admin.site.register(Message)
admin.site.register(RandomInfo)
