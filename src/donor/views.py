import requests
import os
from dotenv import load_dotenv

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse

from .forms import SignInForm, SignUpForm, DonorProfile, DonationForm
from .models import Donors
from .utils import get_random_quotes


load_dotenv()


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        submit_form = SignInForm(request.POST)

        if submit_form.user_exists():
            user = authenticate(
                request, username=submit_form.cleaned_data['username'], password=submit_form.cleaned_data['password'])
            if user is None:
                submit_form.add_error('password', 'Invalid credentials')
                return render(request, "pages/login.html", {'form': submit_form, 'is_register': False})

            messages.add_message(request, messages.SUCCESS,
                                 'Logged in successfully')
            login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))

            return redirect('home')
        else:
            return render(request, "pages/login.html", {'form': submit_form, 'is_register': False})

    form = SignInForm(data={"next": request.GET.get('next')})
    form.errors.clear()
    return render(request, "pages/login.html", {'form': form, 'is_register': False, 'quote': get_random_quotes()})


def signup_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        submit_form = SignUpForm(request.POST)
        if submit_form.is_valid():
            submit_form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Account created successfully. Sign in to continue')
            return redirect('login')
        else:
            return render(request, "pages/login.html", {'form': submit_form, 'is_register': True})

    form = SignUpForm()
    return render(request, "pages/login.html", {'form': form, 'is_register': True})


def donate_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('login') + '?next=' + request.path)

    donor_profiles = Donors.objects.filter(user=request.user)
    if not donor_profiles.exists():
        return redirect(reverse('donor_profile') + '?next=' + request.path)

    form = DonationForm(data={"next": request.GET.get('next')})
    form.errors.clear()

    return render(request, "pages/donate.html", {'form': form})


def donor_profile_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('login') + '?next=' + request.path)

    if request.method == 'POST':
        submit_form = DonorProfile(request.POST)
        if submit_form.is_valid():
            submit_form.save(request.user)
            messages.add_message(request, messages.SUCCESS,
                                 'Donor profile created successfully')
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))

            return redirect('donate')
        else:
            return render(request, "pages/donor_profile.html", {'form': submit_form})

    form = DonorProfile(data={"next": request.GET.get('next')})
    form.errors.clear()
    return render(request, "pages/donor_profile.html", {'form': form})


def get_cities_api(request: HttpRequest, state_iso2: str):
    api_url = "https://api.countrystatecity.in/v1/countries/IN/states/"
    api_url += state_iso2 + "/cities"

    try:
        print(os.environ.get('COUNTY_STATE'))
        response = requests.request('GET', api_url, headers={
                                    'X-CSCAPI-KEY': os.environ.get('COUNTY_STATE')})
        print(response.text)
        if response.status_code == 200:
            json_data = response.json()
            return JsonResponse(json_data, safe=False)

        return HttpResponseBadRequest("API error")
    except Exception as e:
        print(e)
        return HttpResponseServerError("Server error")
