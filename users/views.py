from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib import messages

from alerts.models import EmergencyAlert
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm


from django.db.models import Q
from django.contrib.auth.decorators import login_required

def landing_view(request):
    return render(request, 'webpages/index.html')
    #return render(request, 'users/landing.html')

def about_view(request):
    return render(request, 'webpages/about.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('landing')
        else:
            messages.success(request, 'There was an Error, please try again.')
            return redirect('login')
    else:
        return render(request, 'webpages/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('landing')


def signup_view(request):
    if request.method == 'POST':
        # Basic user info
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Profile info (to be filled after creation)
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        id_verification = request.FILES.get('id_verification')

        # Check for existing username or email
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "A user with that username or email already exists.")
            return render(request, 'users/signup.html', {'form_data': request.POST})

        try:
            # Create the User (signals.py will create Profile)
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            # Populate the profile fields post-creation
            profile = user.profile
            profile.role = role
            profile.phone_number = phone_number
            profile.street_address = street_address
            profile.city = city
            profile.state = state
            profile.country = country
            profile.id_verification = id_verification

            if role == 'restaurant':
                profile.restaurant_name = request.POST.get('restaurant_name')
            elif role == 'foodbank':
                profile.foodbank_name = request.POST.get('foodbank_name')

            profile.save()

            # Clear any previous messages
            for message in messages.get_messages(request):
                message.used = True

            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect to login after successful signup

        except IntegrityError:
            messages.error(request, "An error occurred during signup. Please try again.")
            return render(request, 'users/signup.html', {'form_data': request.POST})

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

@login_required
def home_view(request):
    role = request.user.profile.role
    latest_alert = EmergencyAlert.objects.order_by('-created_at').first()
    return render(request, 'users/home.html', {
        'role': role,
        'latest_alert': latest_alert
    })

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
