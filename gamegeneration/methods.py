#from django.contrib.auth.models import User
from gamegeneration.models import *

#################### ITEM AND ABILITY FORMS #########################3#
questionTaser = {
        'target': ('Who is the target?', 'User'),
        "attribute": ('What attribute?', 'Attribute'),
        "value": ('What value did you want to update it to?', 'int'),
        }

######################## ITEM AND ABILITY METHODS ########################
def useTaser(parameters):
    #name = parameters['target']
    #target = User.objects.get(username=name)
    attribute = parameters['attribute']
    attribute = 'Kill'
    attributetype = Attribute.objects.get(name=attribute)
    attributeinstance = AttributeInstance.objects.get(itype=attributetype)
    attributeinstance.value = 10
    attributeinstance.save()
    description = attributetype.get_description()
    return description+'   attribute'+parameters['value']

