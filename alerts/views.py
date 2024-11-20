from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from utils import send_email
from .models import EmergencyAlert, ResponseToDonation
from .models import Alert
from .forms import CreateAlertForm, RespondToDonationForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum

#alerts/views.py

@login_required
def emergency_alert_view(request):
    if request.user.profile.role != 'foodbank':
        messages.error(request, "Only Foodbanks can submit emergency alerts.")
        return redirect('home')

    if request.method == 'POST':
        message = request.POST.get('message')
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
            return redirect('alert_list')
        else:
            messages.error(request, 'There was an error creating the alert. Please try again.')
            return render(request, 'webpages/alerts.html', {'form': form})

    else:
        form = CreateAlertForm()

    return render(request, 'webpages/alerts.html', {'form': form})


def alert_list(request):
    alerts = Alert.objects.filter(is_active=True)

    #For Food Banks to see their own listings
    if hasattr(request.user, 'foodbank'):
        alerts = alerts.filter(created_by=request.user)

    for alert in alerts:
        total_donated = alert.responses.aggregate(total=Sum('quantity_donated'))['total'] or 0
        alert.total_quantity_donated = total_donated
        alert.remaining_quantity_needed = alert.quantity_needed - total_donated
        if total_donated == 0:
            alert.response_status = "pending"
        elif total_donated < alert.quantity_needed:
            alert.response_status = "in_progress"
        else:
            alert.response_status = "completed"

    return render(request, 'webpages/alert_list.html', {'alerts': alerts})

@login_required
def ResponseToDonationViewX(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)

    if request.method == 'POST':
        form = RespondToDonationForm(request.POST)

        if form.is_valid():
            response = form.save(commit=False)
            response.alert = alert
            response.donor = request.user
            response.status = 'in_progress'
            response.save()

            quantity_donated = form.cleaned_data['quantity']
            alert.quantity_needed -= quantity_donated
            alert.quantity_needed = max(alert.quantity_needed, 0)

            if alert.quantity_needed == 0:
                alert.is_active = False
            else:
                alert.is_active = True

            alert.save()

            messages.success(request, 'Your donation response has been submitted successfully.')
            return redirect('alert_list')
        else:
            messages.error(request, 'There was an error with your response. Please try again.')
    else:
        form = RespondToDonationForm()

    return render(request, 'webpages/response_to_donation.html', {'form': form, 'alert': alert})

@login_required
def ResponseToDonationView(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)

    if request.method == 'POST':
        form = RespondToDonationForm(request.POST)

        if form.is_valid():
            # Create the ResponseToDonation object
            response = ResponseToDonation.objects.create(
                alert=alert,
                donor=request.user,
                quantity_donated=form.cleaned_data['quantity_donated'],
                description=form.cleaned_data['description'],
                pickup_method=form.cleaned_data['pickup_method'],
                pickup_delivery_date=form.cleaned_data['pickup_delivery_date'],
                donor_address=form.cleaned_data['donor_address']
            )
            response.save()

            #Update donation count in DB
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                profile.response_to_emergency_count += 1
                profile.save()
            elif hasattr(request.user, 'restaurant_profile'):
                restaurant = request.user.restaurant_profile
                restaurant.response_to_emergency_count += 1
                restaurant.save()

            foodbank_email = alert.created_by.email
            donor_email = request.user.email
            subject = f"New Donation Response for Alert: {alert.item_name}"
            message_to_foodbank = (
                f"{alert.created_by.username},\n\n"
                f"A donor has responded to your alert:\n\n"
                f"Item: {alert.item_name}\n"
                f"Quantity Donated: {response.quantity_donated}\n"
                f"Pickup Method: {response.pickup_method}\n"
                f"Pickup/Delivery Date: {response.pickup_delivery_date}\n"
                f"Donor Address: {response.donor_address}\n\n"
                f"Additional Details: {response.description}\n\n"
                f"Please log in to the system to manage this response.\n\n"
                f"Best Regards,\nFoodConnect Team"
            )
            message_to_donor = (
                f"{request.user.username},\n\n"
                f"Thank you for responding to the alert for {alert.item_name}.\n\n"
                f"The food bank {alert.created_by.username} has been notified.\n"
                f"Details of your response:\n"
                f"Quantity Donated: {response.quantity_donated}\n"
                f"Pickup Method: {response.pickup_method}\n"
                f"Pickup/Delivery Date: {response.pickup_delivery_date}\n\n"
                f"Best Regards,\nFoodConnect Team"
            )

            try:
                send_email(subject, message_to_foodbank, [foodbank_email])
                send_email(subject, message_to_donor, [donor_email])
                messages.success(request,
                                 'Your response to the donation has been submitted successfully, and emails have been sent.')
            except Exception as e:
                print(e)
                messages.warning(request,
                                 'Your response was submitted, but we were unable to send email notifications.')

            return redirect('alert_list')

        else:
            messages.error(request, 'There was an error in your submission. Please try again.')

    else:
        form = RespondToDonationForm()

    return render(request, 'webpages/response_to_donation.html', {'form': form, 'alert': alert})


@login_required
def ResponseStatusView(request, response_id):
    response = get_object_or_404(ResponseToDonation, id=response_id, donor=request.user)
    return render(request, 'webpages/response_status.html', {'response': response})

