import requests
import os
from dotenv import load_dotenv

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest, FileResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.templatetags.static import static

from .forms import SignInForm, SignUpForm, DonorProfile, DonationForm
from .models import Donors, Donations
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

            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Logged in successfully')
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


def logout_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('home')

    logout(request)
    return redirect('home')


def donate_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('login') + '?next=' + request.path)

    donor_profiles = Donors.objects.filter(user=request.user)
    if not donor_profiles.exists():
        return redirect(reverse('donor_profile') + '?next=' + request.path)

    if request.method == 'POST':
        submit_form = DonationForm(request.POST, request.FILES)
        if submit_form.is_valid():
            submit_form.save(donor_profiles.first())
            messages.add_message(request, messages.SUCCESS,
                                 'Donation added successfully')
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))

            return redirect('home')
        else:
            return render(request, "pages/donate.html", {'form': submit_form})

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
        response = requests.request('GET', api_url, headers={
                                    'X-CSCAPI-KEY': os.environ.get('COUNTY_STATE')})
        if response.status_code == 200:
            json_data = response.json()
            return JsonResponse(json_data, safe=False)

        return HttpResponseBadRequest("API error")
    except Exception as e:
        print(e)
        return HttpResponseServerError("Server error")


def app_assets_image(request: HttpRequest, donation_id: int):
    donation = Donations.objects.filter(id=donation_id).first()
    if not donation:
        return HttpResponseNotFound("Donation not found")

    if not donation.image:
        return redirect(static('img/Food.png'))

    return FileResponse(donation.image.file)
