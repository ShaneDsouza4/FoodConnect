from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CreateDonationForm
from donations.models import Donation


# Create your views here.
def donations_view(request):
    donations = Donation.objects.filter(is_active=True)  # Fetch active alerts
    return render(request, '../templates/donations/donations.html', {'donations':donations})

@login_required
def create_donation(request):
    if request.method == 'POST':
        form = CreateDonationForm(request.POST)
        if form.is_valid():
            alert = Donation(
                item=form.cleaned_data['item'],
                quantity=form.cleaned_data['quantity'],
                urgency_level=form.cleaned_data['urgency_level'],
                description=form.cleaned_data['description'],
                created_by=request.user
            )
            alert.save()

            messages.success(request, 'Donation created successfully!')
            return redirect('donations')
        else:
            messages.error(request, 'There was an error creating the donation. Please try again.')
            return redirect('create-donations')
    else:
        form = CreateDonationForm()

    return render(request, 'donations/create_donation.html', {'form': form})