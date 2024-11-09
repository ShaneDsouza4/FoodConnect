from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyAlert
from .models import Alert
from .forms import CreateAlertForm


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

@login_required
def create_alert(request):
    if request.method == 'POST':
        form = CreateAlertForm(request.POST)
        if form.is_valid():
            alert = Alert(
                item_name=form.cleaned_data['item_name'],
                quantity_needed=form.cleaned_data['quantity_needed'],
                urgency_level=form.cleaned_data['urgency_level'],
                description=form.cleaned_data['description'],
                created_by=request.user
            )
            alert.save()

            messages.success(request, 'Alert created successfully!')
            return redirect('alerts')
        else:
            messages.error(request, 'There was an error creating the alert. Please try again.')
            return redirect('alerts')
    else:
        form = CreateAlertForm()

    return render(request, 'webpages/alerts.html', {'form': form})


