from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, CreateRestaurantForm, CreateFoodBankForm, CreateIndividualForm
from django import forms


from alerts.models import EmergencyAlert
from .models import Profile, Restaurant, FoodBank

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

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #loginuser
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered successfully.')
            return redirect('landing')
        else:
            print("Form errors:", form.errors)
            messages.success(request, 'Error: There was a problem registering, please try again.')
            return redirect('register')
    else:
        return render(request, 'webpages/register.html', {"form": form})

def signup_restaurant(request):
    if request.method == 'POST':
        form = CreateRestaurantForm(request.POST, request.FILES)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return redirect('restaurant_signup')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            restaurant = Restaurant.objects.create(
                user=user,
                restaurant_name=form.cleaned_data['restaurant_name'],
                restaurant_phone=form.cleaned_data['restaurant_phone'],
                email=email,
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                postal_code=form.cleaned_data['postal_code'],
                website=form.cleaned_data['website'],
                id_verification=form.cleaned_data['id_verification']
            )
            restaurant.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Restaurant registered successfully.')
                return redirect('landing')
        else:
            print("Form errors:", form.errors)
            messages.success(request, 'Error: There was a problem registering, please try again.')
            return redirect('restaurant_signup')
    else:
        restaurantform = CreateRestaurantForm()
        return render(request, 'webpages/retaurant_signup.html', {'form': restaurantform})

def signup_foodbank(request):
    if request.method == 'POST':
        form = CreateFoodBankForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return redirect('foodbank_signup')

            user = User.objects.create_user(username=username, email=email, password=password)

            foodbank = FoodBank.objects.create(
                user=user,
                foodbank_name=form.cleaned_data['foodbank_name'],
                foodbank_phone=form.cleaned_data['foodbank_phone'],
                email=email,
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                postal_code=form.cleaned_data['postal_code'],
                website=form.cleaned_data['website'],
                id_verification=form.cleaned_data['id_verification']
            )
            foodbank.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Food Bank registered successfully.')
                return redirect('landing')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Error: There was a problem registering, please try again.')
            return redirect('foodbank_signup')

    foodbankform = CreateFoodBankForm()
    return render(request, 'webpages/foodbank_signup.html', {'form': foodbankform})

def signup_individual(request):
    if request.method == 'POST':
        form = CreateIndividualForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return redirect('individual_signup')

            user = User.objects.create_user(username=username, email=email, password=password)

            profile = Profile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                street_address=form.cleaned_data['street_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                id_verification=form.cleaned_data['id_verification']
            )
            profile.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. Welcome!')
                return redirect('landing')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'There was a problem with your registration. Please try again.')
            return redirect('individual_signup')

    form = CreateIndividualForm()
    return render(request, 'webpages/individual_signup.html', {'form': form})

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
