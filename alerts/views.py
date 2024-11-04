from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyAlert


@login_required
def emergency_alert_view(request):
    # Only foodbank user role
    if request.user.profile.role != 'foodbank':
        messages.error(request, "Only Foodbanks can submit emergency alerts.")
        return redirect('home')

    if request.method == 'POST':
        message = request.POST.get('message')

        # Create the Emergency Alert
        EmergencyAlert.objects.create(user=request.user, message=message)
        messages.success(request, "Emergency alert submitted successfully.")
        return redirect('home')

    return render(request, 'alerts/emergency_alert.html')