from django import forms

class AutoGenerateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #Supermethod declarations
        extra = kwargs.pop('extra', {})
        super(AutoGenerateForm, self).__init__(*args, **kwargs)

        #For every fieldname in requests, make a new field
        for i, field in enumerate(extra.keys()):
            self.fields[field] = forms.CharField(label=extra[field][0])

    def get_answers(self):
        #Initialize Answers as dictionary
        answers = {}
        #For every field, return the field and the cleaned value in the dictionary
        for field, value in self.cleaned_data.items():
            answers[field]= value
        return answers
