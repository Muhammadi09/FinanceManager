from django import forms
from django.forms import ModelForm

from .models import Transaction


class DateInput(forms.DateInput):
    input_type = 'date'


class IncomeExpForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'description']
        widgets = {
            'date': DateInput(),
        }

class DateForm(forms.Form):
    date1 = forms.DateField(widget=DateInput(), required=False)
    date2 = forms.DateField(widget=DateInput(), required=False)
    description = forms.CharField(max_length=200,
                                  widget=forms.TextInput(attrs={'placeholder': 'Description'}),
                                  required=False
                                  )
