from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from gotrue.errors import AuthApiError

from .forms import registerform
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from supabase import create_client

import os

# Load Supabase credentials
SUPABASE_URL = "https://rsdvkupcprtchpzuxgtd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJzZHZrdXBjcHJ0Y2hwenV4Z3RkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgwODEyNDIsImV4cCI6MjA1MzY1NzI0Mn0.9SQn2rXp4j6p8Em_FVhEHukZdzpYqV4lF5T8PT_gVAc"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_view(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = registerform()
    return render(request, 'api/register.html/', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST["username"]
        password = request.POST["password"]

        try:
            # Authenticate with Supabase
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            if response:
                return redirect('dashboard')  # Redirect to dashboard
            else:
                messages.error(request, "Failed login attempt")
                return redirect('login')

        except AuthApiError as e:
            messages.error(request, "Failed login attempt")
            return redirect('login')

    return render(request, "api/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, "api/home.html")

#@login_required
def dashboard_view(request):
    return render(request, 'api/dashboard.html', {'user': request.user})



