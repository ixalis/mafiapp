from django import forms
from gamegeneration.models import *

class AutoGenerateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #Supermethod declarations
        extra = kwargs.pop('extra', {})
        super(AutoGenerateForm, self).__init__(*args, **kwargs)

        #For every fieldname in requests, make a new field
        for i, field in enumerate(extra.keys()):
            ftype = extra[field][1]
            if ftype=='User':
                self.fields[field] = forms.ModelChoiceField(queryset=User.objects.all())
            elif ftype=='Item':
                self.fields[field] = forms.ModelChoiceField(queryset=Item.objects.all())
            elif ftype=='int':
                self.fields[field] = forms.IntegerField()
            elif ftype=='UserMult':
                self.fields[field] = forms.ModelMultipleChoiceField(queryset=User.objects.all())
            else:
                self.fields[field] = forms.CharField(label=extra[field][0])

    def get_answers(self):
        #Initialize Answers as dictionary
        answers = {}
        #For every field, return the field and the cleaned value in the dictionary
        for field, value in self.cleaned_data.items():
            answers[field]= value
        return answers

class ItemInstanceForm(forms.ModelForm):
    class Meta:
        model = ItemInstance

class AbilityInstanceForm(forms.ModelForm):
    class Meta:
        model = AbilityInstance

class AttributeInstanceForm(forms.ModelForm):
    class Meta:
        model = AttributeInstance
