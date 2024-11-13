from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyAlert
from .models import Alert
from .forms import CreateAlertForm
from .forms import ResponseToDonationForm
from django.shortcuts import render, get_object_or_404

#alerts/views.py

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
def alert_list(request):
    alerts = Alert.objects.filter(is_active=True)
    return render(request, 'webpages/alert_list.html', {'alerts': alerts})

# def donate(request, alert_id):
#     alert = get_object_or_404(Alert, id=alert_id)
#     # Your donate logic here
#     return render(request, 'donate.html', {'alert': alert})
@login_required
def ResponseToDonationView(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)

    if request.method == 'POST':
        form = ResponseToDonationForm(request.POST)  # Use the corrected form

        if form.is_valid():
            response = form.save(commit=False)
            response.alert = alert
            response.donor = request.user
            response.status = 'in_progress'
            response.save()

            alert.is_active = False  # Optionally deactivate alert after donation
            alert.save()

            messages.success(request, 'Your donation response has been submitted successfully.')
            return redirect('alert_list')
        else:
            messages.error(request, 'There was an error with your response. Please try again.')
    else:
        form = ResponseToDonationForm()  # Initialize an empty form on GET request

    return render(request, 'webpages/response_to_donation.html', {'form': form, 'alert': alert})

@login_required
def ResponseStatusView(request, response_id):
    response = get_object_or_404(ResponseToDonationForm, id=response_id, donor=request.user)
    return render(request, 'webpages/response_status.html', {'response': response})

