from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CreateDonationForm
from donations.models import Donation, Category, Product


# Create your views here.

def donations_view(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, '../templates/donations/donations.html', {'products':page_obj, 'categories': categories, 'page_obj': page_obj,'current_category': int(category_id) if category_id else None,})

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