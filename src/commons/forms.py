from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

import re

class SignInForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'pattern': '^[a-z0-9_]{3,30}$'}))
    password = forms.CharField(max_length=100, min_length=8, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def user_exists(self) -> bool:
        if not super().is_valid():
            return False
        
        if not User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', 'User does not exist')
            return False
        
        return True
    


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=30, min_length=2, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}))
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'pattern': '^[a-z0-9_]{3,30}$'}))
    password = forms.CharField(max_length=100, min_length=8, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=100, min_length=8, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        
        usrpattern = '^[a-z0-9_]{3,30}$'
        usrname = self.cleaned_data['username']
        emailpattern = '^([A-Za-z0-9](\.|_){0,1})+[A-Za-z0-9]\@([A-Za-z0-9])+((\.){0,1}[A-Za-z0-9]){2}\.[a-z]{2,3}$'
        emailstr = self.cleaned_data['email']

        valid_form = True

        if not re.match(emailpattern, emailstr):
            self.add_error('email', ValidationError('Invalid email.'))
            valid_form = False
            
        if not re.match(usrpattern, usrname):
            self.add_error('username', ValidationError('Invalid username. Username must contain only letters, numbers and underscores.'))
            valid_form = False

        if not self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', ValidationError('Passwords do not match'))
            valid_form = False
        
        if User.objects.filter(username=usrname).exists():
            self.add_error('username', ValidationError('Username already exists'))
            valid_form = False

        return valid_form
    
    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'], first_name=self.cleaned_data['name'])
        user.save()
        return user

