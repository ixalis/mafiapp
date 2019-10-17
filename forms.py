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
	email = forms.EmailField(required=False, max_length=200, help_text='Enter a valid email address if you want email notifications')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )

class NewGameForm(forms.Form):
	game_name = forms.CharField(label='Game Name', max_length=200)

class ChangeEmailForm(forms.Form):
	new_email = forms.CharField(label='New Email', max_length=200)

class ChangePasswordForm(forms.Form):
	password1 = forms.CharField(label='New Email', max_length=200)
	password2 = forms.CharField(label='New Email', max_length=200)