from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now

from .forms import CreateDonationForm, AddProductForm
from donations.models import Category, Product, Donation


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

# views.py
@login_required
def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product_id)
    return render(request, '../templates/donations/product_detail.html', {'product': product, 'related_products': related_products})

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
                date_created=now(),
            )
            product.save()

            products_by_user = Product.objects.filter(donated_by=request.user)

            # Metrics for analytics
            def update_metrics(entity):
                # Total donations
                entity.total_donations += 1

                # Donation frequency
                one_month_ago = now() - timedelta(days=28)
                recent_donations = products_by_user.filter(date_created__gte=one_month_ago).count()
                entity.donation_frequency = recent_donations

                # Donation variety count
                unique_categories = products_by_user.values('category').distinct().count()
                entity.donation_variety_count = unique_categories

                # Donation volume
                conversion_factors = {'g': 0.001,'kg': 1, 'ml': 0.001,'liters': 1}
                normalized_weight = product.weight * conversion_factors.get(product.unit, 1)
                current_product_volume = product.quantity * normalized_weight
                entity.donation_volume += current_product_volume

                entity.save()

            if hasattr(request.user, 'profile'):
                update_metrics(request.user.profile)
            elif hasattr(request.user, 'restaurant_profile'):
                update_metrics(request.user.restaurant_profile)

            messages.success(request, 'Donation added successfully!')
            return redirect('donations')
        else:
            messages.error(request, 'Errors in the form.')
    else:
        form = AddProductForm()

    return render(request, 'donations/create_donation.html', {'form': form})
@login_required

def place_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)

        if product.quantity < quantity:
            messages.error(request, "Not enough quantity available.")
            return redirect('product_detail', product.id)

        product.quantity -= quantity
        product.amount_donated += quantity
        Donation.objects.create(
            user=request.user,
            product=product,
            quantity=quantity
        )
        product.save()
        messages.success(request, "Order placed successfully!")
        return render(request, '../templates/donations/donation_list.html')

    messages.error(request, "Invalid request.")
    # return render(request, '../templates/donations/product_detail.html', {'product': product})
