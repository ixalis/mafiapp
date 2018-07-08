from django import forms

class UseItemForm(forms.Form):

    def __init__(self, *args, **kwargs):
        requests = kwargs.pop('extra', {})
        super(UseItemForm, self).__init__(*args, **kwargs)

        for i, field in enumerate(requests.keys()):
            self.fields[field] = forms.CharField(label=requests[field][0])
    
    def clean_value(self):
        value = self.cleaned_data["value"]
        return value
    def get_answers(self):
        answers = {}
        for field, value in self.cleaned_data.items():
            answers[field]= value
        return answers
