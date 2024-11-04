from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from .models import Profile

def landing_view(request):
    return render(request, 'users/landing.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        id_verification = request.FILES.get('id_verification')

        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            # Update the profile with ID verification file if provided
            if id_verification:
                user.profile.id_verification = id_verification
                user.profile.save()

            # Redirect to home page after successful signup
            return redirect('home')

        except Exception as e:
            # Log any unexpected errors
            #logger.error("Unexpected error occurred during signup: %s", e)
            error_message = "An unexpected error occurred. Please try again."
            return render(request, 'users/signup.html', {'error_message': error_message})

    return render(request, 'users/signup.html')



def home_view(request):
    return render(request, 'users/home.html')