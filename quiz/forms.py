from django import forms
from django.forms import ModelForm, TextInput
from .models import TestDetail


class TestDetailForm(forms.Form):
    username = forms.CharField(
                    min_length=2, 
                    max_length=200, 
                    widget=forms.TextInput(
                        attrs={
                                'class': 'form-control', 
                                'placeholder': 'Please enter a username'
                                }
                        )
                    )
    
    

    # error_messages = {
    #     'username': {
    #         'required': ('Please provide a username'),
    #         'min_length': ('Your username must be at least 2 characters')
    #     }
    # }

