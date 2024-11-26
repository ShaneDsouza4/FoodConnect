from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now

from donations.models import Product
from .forms import SignUpForm, CreateRestaurantForm, CreateFoodBankForm, CreateIndividualForm, EditRestaurantForm, \
    EditFoodBankForm, EditIndividualForm
from django import forms


from alerts.models import EmergencyAlert
from .models import Profile, Restaurant, FoodBank

from django.db.models import Q
from django.contrib.auth.decorators import login_required

from utils import send_email_to_us
from datetime import datetime


# Landing page view
def landing_view(request):
    products = Product.objects.filter(expiry_date__gte=now()).order_by('-date_created')[:8]
    return render(request, 'webpages/index.html', {'products': products})

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
            if not User.objects.filter(username=username).exists():
                 messages.success(request, f"No user found with username: {username}")
            else:
                messages.success(request, f"Incorrect Password for username: {username}")
        return redirect('login')
    else:
        return render(request, 'webpages/login.html')

# Logout user view
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

# Restaurant Signup View
def signup_restaurant(request):
    if request.method == 'POST':
        # Take all inputs from webpage, and put in signup form
        form = CreateRestaurantForm(request.POST, request.FILES)

        # If user has filled the form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Check if username exists in the DB
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'webpages/restaurant_signup.html', {'form': form})

            # Check if email exists in the DB
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please choose a different one.')
                return render(request, 'webpages/restaurant_signup.html', {'form': form})

            # Create new Restaruant User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Restaurant Model for the restaurant user with additional fields
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

            # Authenticate and Login
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
        restaurantform = CreateRestaurantForm() #Empty Form
        return render(request, 'webpages/restaurant_signup.html', {'form': restaurantform})

# Food Bank Signup View
def signup_foodbank(request):
    if request.method == 'POST':
        # Take all inputs from webpage, and put in signup form
        form = CreateFoodBankForm(request.POST, request.FILES)

        # If user has filled the form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Check if username exists in the DB
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'webpages/foodbank_signup.html', {'form': form})

            # Check if email exists in the DB
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please choose a different one.')
                return render(request, 'webpages/foodbank_signup.html', {'form': form})

            # Create new Food Bank User
            user = User.objects.create_user(username=username, email=email, password=password)

            # Food Bank Model for the foodbank user with additional fields
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

            #Authenticate and login the restaurant user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Food Bank registered successfully.')
                return redirect('landing')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Error: There was a problem registering, please try again.')
            return redirect('foodbank_signup')

    foodbankform = CreateFoodBankForm() #Empty Form
    return render(request, 'webpages/foodbank_signup.html', {'form': foodbankform})

# Individual Signup Form View
def signup_individual(request):
    if request.method == 'POST':
        # Take all inputs from webpage, and put in signup form
        form = CreateIndividualForm(request.POST, request.FILES)

        # If user has filled the form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Check if username exists in the DB
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'webpages/individual_signup.html', {'form': form})

            # Check if email exists in the DB
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please choose a different one.')
                return render(request, 'webpages/individual_signup.html', {'form': form})

            # Create new User
            user = User.objects.create_user(username=username, email=email, password=password)

            # Profile for the user with additional fields
            profile = Profile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                street_address=form.cleaned_data['street_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                postal_code=form.cleaned_data['postal_code'],
                id_verification=form.cleaned_data['id_verification']
            )
            profile.save()

            # Authenticate new user and log them in
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. Welcome!')
                return redirect('landing')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'There was a problem with your registration. Please try again.')
            return redirect('individual_signup')

    form = CreateIndividualForm() #Empty Form
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


#Contact Us
def contact_view(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']

        recipient_list=[email]
        full_message = f"This message is from {name}.\n\n{message}"

        try:
            send_email_to_us(subject, full_message, recipient_list)
            messages.success(request, 'Message sent succesfully.')
        except Exception as e:
            print(e)
            messages.error(request, 'Message was not sent.')
            return redirect('contact_us')
    return render(request, 'webpages/contact.html')

#User Profile
def user_profile(request):
    if 'profile_view_count' not in request.session:
        request.session['profile_view_count'] = 0
    request.session['profile_view_count'] += 1

    last_login = request.COOKIES.get('last_login')
    response = render(request, 'webpages/user_profile.html', {
        'last_login': last_login,
        'view_count': request.session['profile_view_count']
    })
    response.set_cookie('last_login', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return response

def edit_profile(request):
    user = request.user #User instance

    if hasattr(user, 'restaurant_profile'): #if user linked to Restaurant
        restaurant = user.restaurant_profile
        if request.method == 'POST':
            form = EditRestaurantForm(request.POST)

            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.save()

                restaurant.restaurant_name = form.cleaned_data['restaurant_name']
                restaurant.restaurant_phone = form.cleaned_data['restaurant_phone']
                restaurant.street = form.cleaned_data['street']
                restaurant.city = form.cleaned_data['city']
                restaurant.state = form.cleaned_data['state']
                restaurant.country = form.cleaned_data['country']
                restaurant.postal_code = form.cleaned_data['postal_code']
                restaurant.website = form.cleaned_data['website']
                restaurant.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile')
        else:
            form = EditRestaurantForm(initial={
                'email': user.email,
                'restaurant_name': restaurant.restaurant_name,
                'restaurant_phone': restaurant.restaurant_phone,
                'street': restaurant.street,
                'city': restaurant.city,
                'state': restaurant.state,
                'country': restaurant.country,
                'postal_code': restaurant.postal_code,
                'website': restaurant.website,
            })
    elif hasattr(user, 'foodbank'): #if user linked to Food Bank
        foodbank = user.foodbank
        if request.method == 'POST':
            form = EditFoodBankForm(request.POST)

            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.save()

                foodbank.foodbank_name = form.cleaned_data['foodbank_name']
                foodbank.foodbank_phone = form.cleaned_data['foodbank_phone']
                foodbank.street = form.cleaned_data['street']
                foodbank.city = form.cleaned_data['city']
                foodbank.state = form.cleaned_data['state']
                foodbank.country = form.cleaned_data['country']
                foodbank.postal_code = form.cleaned_data['postal_code']
                foodbank.website = form.cleaned_data['website']
                foodbank.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile')
        else:
            form = EditFoodBankForm(initial={
                'email': user.email,
                'foodbank_name': foodbank.foodbank_name,
                'foodbank_phone': foodbank.foodbank_phone,
                'street': foodbank.street,
                'city': foodbank.city,
                'state': foodbank.state,
                'country': foodbank.country,
                'postal_code': foodbank.postal_code,
                'website': foodbank.website,
            })
    elif hasattr(user, 'profile'):  # if profile linked to Food Bank
        profile = user.profile
        if request.method == 'POST':
            form = EditIndividualForm(request.POST)
            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.save()

                profile.first_name = form.cleaned_data['first_name']
                profile.last_name = form.cleaned_data['last_name']
                profile.phone_number = form.cleaned_data['phone_number']
                profile.street_address = form.cleaned_data['street_address']
                profile.city = form.cleaned_data['city']
                profile.state = form.cleaned_data['state']
                profile.country = form.cleaned_data['country']
                profile.postal_code = form.cleaned_data['postal_code']
                profile.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile')
        else:
            form = EditIndividualForm(initial={
                'email': user.email,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'phone_number': profile.phone_number,
                'street_address': profile.street_address,
                'city': profile.city,
                'state': profile.state,
                'country': profile.country,
                'postal_code': profile.postal_code,
            })
    else:
        messages.error(request, 'Unable to identify your profile type.')
        return redirect('landing')
    return render(request, 'webpages/edit_profile.html', {"form": form})