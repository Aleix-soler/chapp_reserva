from datetime import date
import re
from django.forms import ModelForm, RadioSelect
from django.core.exceptions import ValidationError
from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type='date'

class PhoneInput(forms.CharField):
    input_type='tel'
    
    
class BookForm(ModelForm):
    num_guests = forms.IntegerField(max_value=4, min_value=1, required=False)
    class Meta:
        model = Book
        fields = '__all__'
        #fields = ['date_entry', 'date_exit', 'num_guests', 'type_room', 'room_number', 'price', 'user']
        widgets = {
            'date_entry': DateInput(attrs={'max': '2022-12-31', 'min': date.today()}),
            'date_exit': DateInput(attrs={'max': '2022-12-31', 'min': date.today()}),
            #'price': HiddenInput(),
            'type_room': RadioSelect(),
        }

class FirstForm(forms.Form):
    date_entry = forms.DateField(widget=DateInput(attrs={'max': '2022-12-31', 'min': date.today()}))
    date_exit = forms.DateField(widget=DateInput(attrs={'max': '2022-12-31', 'min': date.today()}))
    number_guests = forms.IntegerField(max_value=4, min_value=1)
    
    def clean(self, *args, **kwargs):
        date_entry = self.cleaned_data.get("date_entry")
        date_exit = self.cleaned_data.get("date_exit")
        
        if date_entry>date_exit:
            raise ValidationError("Entry Date is Bigger than Exit Date")
    
class SecondForm(forms.Form):
    type_room = forms.ChoiceField(choices=(('SINGLE', 'SINGLE'), ('DOUBLE', 'DOUBLE'), ('TRIPLE', 'TRIPLE'), ('QUADRUPLE', 'QUADRUPLE')), widget=forms.RadioSelect)
    price = forms.FloatField()

class ThirdForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(required=True)
    
    def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get('phone')
        if re.compile("^\+?[0-9]{0,3}? ?[0-9]{9,12}$").match(phone):
            return phone
        else: 
            raise forms.ValidationError("Phone not matching pattern (+34 666777666)")