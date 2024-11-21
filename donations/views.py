from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now

from .forms import CreateDonationForm, AddProductForm
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
        form = AddProductForm(request.POST)
        if form.is_valid():
            # Create a new Product object
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category_id=form.cleaned_data['category'],
                quantity=form.cleaned_data['quantity'],
                weight=form.cleaned_data['weight'],
                unit=form.cleaned_data['unit'],
                expiry_date=form.cleaned_data['expiry_date'],
                image=form.cleaned_data['image'],
                donated_by=request.user,
            )
            product.save()

            messages.success(request, 'Donation added successfully!')
            return redirect('donations')
        else:
            messages.error(request, 'Errors in the form.')
    else:
        form = AddProductForm()

    return render(request, 'donations/create_donation.html', {'form': form})