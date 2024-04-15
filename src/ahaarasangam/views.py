from django.shortcuts import render, redirect
from django.http import HttpRequest

def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, "pages/home.html", {})

