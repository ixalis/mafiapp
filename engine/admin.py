from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Profile)
admin.site.register(Player)
admin.site.register(Condition)
admin.site.register(Effect)
admin.site.register(Item)
admin.site.register(Trigger)