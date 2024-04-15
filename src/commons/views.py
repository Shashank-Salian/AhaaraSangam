from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import SignInForm, SignUpForm


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        print(request.user)
        return redirect('home')
    
    if request.method == 'POST':
        submit_form = SignInForm(request.POST)
        
        if submit_form.user_exists():
            user = authenticate(request, username=submit_form.cleaned_data['username'], password=submit_form.cleaned_data['password'])
            if user is None:
                submit_form.add_error('password', 'Invalid credentials')
                return render(request, "pages/login.html", { 'form': submit_form, 'is_register': False })
            
            messages.add_message(request, messages.SUCCESS, 'Logged in successfully')
            login(request, user)
            return redirect('home')
        else:
            return render(request, "pages/login.html", { 'form': submit_form, 'is_register': False })
        
    form = SignInForm()
    return render(request, "pages/login.html", { 'form': form, 'is_register': False })


def signup_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        submit_form = SignUpForm(request.POST)
        if submit_form.is_valid():
            submit_form.save()
            messages.add_message(request, messages.SUCCESS, 'Account created successfully. Sign in to continue')
            return redirect('login')
        else:
            return render(request, "pages/login.html", { 'form': submit_form, 'is_register': True })
        
    form = SignUpForm()
    return render(request, "pages/login.html", { 'form': form, 'is_register': True })
