from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator

from donor.forms import GetLocationForm
from donor.models import Donations


def home(request: HttpRequest):
    form = GetLocationForm(request.GET)
    query_state = request.GET.get('state')
    query_city = request.GET.get('city')
    donations = Donations.objects.filter(
        available=True).order_by('date').reverse()

    if query_state and query_state != '0':
        state_iso2 = query_state.split(';')[1]
        donations = Donations.objects.filter(
            available=True, donor__state_iso2=state_iso2).order_by('date').reverse()

    if query_city and query_city != '0' and query_state and query_state != '0':
        donations = donations.filter(
            donor__city=query_city).order_by('date').reverse()

    paginator = Paginator(donations, 10)
    page = paginator.get_page(request.GET.get('page', 1)).object_list
    return render(request, "pages/home.html", {"form": form, "donations": page})
