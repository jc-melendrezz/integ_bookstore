from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.Charfield(required=True, max_length=30)
    last_name = forms.Charfield(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
