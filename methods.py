from gamegeneration.models import *
##### ITEM AND ABILITY FORMS ####
questionTaser = {
        'target': ('Who is the target?', 'User'),
        "attribute": ('What attribute?', 'Attribute'),
        "value": ('What value did you want to update it to?', 'int'),
        }

##### ITEM AND ABILITY METHODS #####
def useMint():
    return "meow"

def activateKill():
    return "HI"

def useTaser(parameters):

    return parameters['target']+'attribute'+parameters['value']
    #return "what's up"

