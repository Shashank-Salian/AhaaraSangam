from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

import re

from .raw_data import IN_STATES
from .models import Donors, Donations


class SignInForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'pattern': r'^[a-z0-9_]{3,30}$'}))
    password = forms.CharField(max_length=100, min_length=8, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def user_exists(self) -> bool:
        if not super().is_valid():
            return False

        if not User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', 'User does not exist')
            return False

        return True


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=30, min_length=2, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
                             'placeholder': 'Email', 'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}))
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'pattern': r'^[a-z0-9_]{3,30}$'}))
    password = forms.CharField(max_length=100, min_length=8, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=100, min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False

        usrpattern = r'^[a-z0-9_]{3,30}$'
        usrname = self.cleaned_data['username']
        emailpattern = r'^([A-Za-z0-9](\.|_){0,1})+[A-Za-z0-9]\@([A-Za-z0-9])+((\.){0,1}[A-Za-z0-9]){2}\.[a-z]{2,3}$'
        emailstr = self.cleaned_data['email']

        valid_form = True

        if not re.match(emailpattern, emailstr):
            self.add_error('email', ValidationError('Invalid email.'))
            valid_form = False

        if not re.match(usrpattern, usrname):
            self.add_error('username', ValidationError(
                'Invalid username. Username must contain only letters, numbers and underscores.'))
            valid_form = False

        if not self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', ValidationError(
                'Passwords do not match'))
            valid_form = False

        if User.objects.filter(username=usrname).exists():
            self.add_error('username', ValidationError(
                'Username already exists'))
            valid_form = False

        return valid_form

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'], first_name=self.cleaned_data['name'])
        user.save()
        return user


class DonorProfile(forms.Form):
    organization_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Organization Name'}))
    contact_number = forms.CharField(max_length=13, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Contact Number', 'type': 'tel'}))
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Address'}))

    states_choice = [('0', 'Select State')]
    states_choice.extend(
        [(f"{s['name']};{s['iso2']}", s['name']) for s in IN_STATES])

    state = forms.CharField(widget=forms.Select(
        attrs={'placeholder': 'State'}, choices=states_choice))
    city = forms.CharField(widget=forms.Select(
        attrs={'placeholder': 'City'}, choices=[('0', 'Select City')]))

    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def get_state_info(self):
        return self.cleaned_data['state'].split(';')

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False

        is_valid_form = True

        if len(self.cleaned_data['organization_name']) < 3:
            self.add_error('organization_name', ValidationError(
                'Please enter a valid organization name.'))
            is_valid_form = False

        if len(self.cleaned_data['contact_number']) < 10:
            self.add_error('contact_number', ValidationError(
                'Please enter a valid contact number.'))
            is_valid_form = False

        if self.cleaned_data['state'] == '0':
            self.add_error('state', ValidationError('Please select a state.'))
            is_valid_form = False

        if self.cleaned_data['city'] == '0':
            self.add_error('city', ValidationError('Please select a city.'))
            is_valid_form = False

        if len(self.cleaned_data['address']) < 5:
            self.add_error('address', ValidationError(
                'Please enter a valid address.'))
            is_valid_form = False

        return is_valid_form

    def save(self, user):
        [state_name, state_iso2] = self.get_state_info()
        city_name = self.cleaned_data['city']
        donor = Donors(user=user, organization_name=self.cleaned_data['organization_name'], contact_number=self.cleaned_data[
                       'contact_number'], address=self.cleaned_data['address'], state=state_name, city=city_name, state_iso2=state_iso2)

        donor.save()


class DonationForm(forms.Form):
    items = forms.CharField(max_length=500, required=True, label="Food Items (separate by comma ',')",
                            widget=forms.Textarea(attrs={'placeholder': 'Food items'}))
    amount = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': 'Amount in KG'}), label="Amount in KG")
    category = forms.ChoiceField(choices=Donations.FOOD_TYPE)
    image = forms.ImageField(required=False)
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False

        is_valid_form = True

        if len(self.cleaned_data['items']) < 3:
            self.add_error('items', ValidationError(
                'Please enter valid food items.'))
            is_valid_form = False

        return is_valid_form

    def save(self, donor):
        donation = Donations(donor=donor, items=self.cleaned_data['items'], amount=self.cleaned_data[
                             'amount'], food_type=self.cleaned_data['category'], image=self.cleaned_data['image'])
        donation.save()


class GetLocationForm(forms.Form):
    states_choice = [('0', 'Select State')]
    states_choice.extend(
        [(f"{s['name']};{s['iso2']}", s['name']) for s in IN_STATES])

    state = forms.CharField(widget=forms.Select(
        attrs={'placeholder': 'State'}, choices=states_choice), required=False)
    city = forms.CharField(widget=forms.Select(
        attrs={'placeholder': 'City'}, choices=[('0', 'Select City')]), required=False)

    def get_state_name(self):
        return self.cleaned_data['state'].split(';')[0]

    def get_state_iso2(self):
        return self.cleaned_data['state'].split(';')[1]
