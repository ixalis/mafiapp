from django import forms
from engine.models import *
from django.contrib.auth.forms import UserCreationForm

class AutoGenerateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #Supermethod declarations
        extra = kwargs.pop('extra', {})
        super(AutoGenerateForm, self).__init__(*args, **kwargs)

        #For every fieldname in requests, make a new field
        for i, field in enumerate(extra.keys()):
            ftype = extra[field][1]
            if type(ftype) is tuple:
                choices = []
                for c in ftype:
                    choices.append((c, c))
                self.fields[field] = forms.ChoiceField(label=extra[field][0], choices=choices)
            elif ftype=='User':
                self.fields[field] = forms.ModelChoiceField(label=extra[field][0], queryset=User.objects.all())
            elif ftype=='Item':
                self.fields[field] = forms.ModelChoiceField(label=extra[field][0], queryset=Item.objects.all())
            elif ftype=='int':
                self.fields[field] = forms.IntegerField(label=extra[field][0])
            elif ftype=='UserMult':
                self.fields[field] = forms.ModelMultipleChoiceField(label=extra[field][0],queryset=User.objects.all())
            else:
                self.fields[field] = forms.CharField(label=extra[field][0])

    def get_answers(self):
        #Initialize Answers as dictionary
        answers = {}
        #For every field, return the field and the cleaned value in the dictionary
        for field, value in self.cleaned_data.items():
            answers[field]= value
        return answers

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, max_length=254, help_text='Enter a valid email address if you want email notifications')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
class ItemTransferForm(forms.Form):
    newowner = forms.ModelChoiceField(label="Who do you want to transfer it to?", queryset=User.objects.all())
    def get_answer(self):
        return self.cleaned_data['newowner']