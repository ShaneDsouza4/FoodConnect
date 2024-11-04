from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def landing_view(request):
    return render(request, 'users/landing.html')


def signup_view(request):
    if request.method == 'POST':

        # Basic user info
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Profile info
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        id_verification = request.FILES.get('id_verification')

        # Role based fields
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_contact_number = request.POST.get('restaurant_contact_number')
        foodbank_name = request.POST.get('foodbank_name')
        foodbank_contact_number = request.POST.get('foodbank_contact_number')

        # Check for existing username or email
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "A user with that username or email already exists.")
            return render(request, 'users/signup.html', request.POST)

        # Create the User and Profile
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password)

        # Updating the Profile with role specific data
        profile = user.profile
        profile.role = role
        profile.phone_number = phone_number
        profile.street_address = street_address
        profile.city = city
        profile.state = state
        profile.country = country
        profile.id_verification = id_verification

        # Save role specific fields based on selected role
        if role == 'restaurant':
            profile.restaurant_name = restaurant_name
            profile.restaurant_contact_number = restaurant_contact_number
        elif role == 'foodbank':
            profile.foodbank_name = foodbank_name
            profile.foodbank_contact_number = foodbank_contact_number

        profile.save()
        return redirect('home')

    return render(request, 'users/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect already logged-in users to the home page

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def home_view(request):
    role = request.user.profile.role #Access user profile to get the role
    return render(request, 'users/home.html', {'role': role})


def logout_view(request):
    logout(request)
    return redirect('landing')  # Redirect to the landing page



@login_required
def emergency_alert_view(request):
    # Implement the emergency alert functionality here
    return render(request, 'users/emergency_alert.html')

@login_required
def donate_view(request):
    # Implement the donate functionality here
    return render(request, 'users/donate.html')