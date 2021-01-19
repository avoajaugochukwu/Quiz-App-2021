from django import forms
from django.forms import ModelForm, TextInput
from .models import TestDetail
from django.core.exceptions import ValidationError


class TestDetailForm(forms.ModelForm):
    class Meta:
        model = TestDetail
        fields = ['username']

    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a username'})
    )

    def clean_username(self):
        new_username = self.cleaned_data.get('username')

        # Check if username is less than 2 characters
        if len(new_username) < 2:
            raise ValidationError('Username must be at least 2 characters')
        # Check if username exists
        if TestDetail.objects.filter(username__iexact=new_username).count():
            raise ValidationError(f'Username, {new_username} already taken')

        return new_username

    # def save(self):
    #     new_username = self.cleaned_data.get('username')
    #     new_test = TestDetail.objects.create(username = new_username)

    #     return new_test

    # For multiple fields
    # widgets = {
    #     'username': forms.TextInput(attrs={'class': 'form-control'}),
    #     'email': forms.EmailInput(attrs={'class': 'form-control'})
    #     ...
    # }
