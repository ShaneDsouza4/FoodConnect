from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now

from .forms import CreateDonationForm, AddProductForm
from donations.models import Category, Product, Reservation


# Create your views here.

def donations_view(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products = Product.objects.filter(category_id=category_id, expiry_date__gte=now())
    else:
        products = Product.objects.filter(expiry_date__gte=now())
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
        form = AddProductForm(request.POST, request.FILES)
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
        reservation = Reservation.objects.create(
            user=request.user,
            product=product,
            quantity=quantity
        )
        product.save()

        # Getting reserver details based on User associattion
        if hasattr(request.user, 'profile'):
            reserver_phone = request.user.profile.phone_number
            reserver_name = request.user.profile.get_full_name()
        elif hasattr(request.user, 'restaurant_profile'):
            reserver_phone = request.user.restaurant_profile.restaurant_phone
            reserver_name = request.user.restaurant_profile.get_full_name()
        elif hasattr(request.user, 'foodbank'):
            reserver_phone = request.user.foodbank.foodbank_phone
            reserver_name = request.user.foodbank.get_full_name()
        else:
            reserver_phone = "Not provided"
            reserver_name = request.user.username

        # Getting donor details based on User association
        if hasattr(product.donated_by, 'profile'):
            donor_name = product.donated_by.profile.get_full_name()
            donor_phone = product.donated_by.profile.phone_number
            donor_address = f"{product.donated_by.profile.street_address}, {product.donated_by.profile.city}, {product.donated_by.profile.state}, {product.donated_by.profile.country} {product.donated_by.profile.postal_code}".strip(
                ", ")
        elif hasattr(product.donated_by, 'restaurant_profile'):
            donor_name = product.donated_by.restaurant_profile.get_full_name()
            donor_phone = product.donated_by.restaurant_profile.restaurant_phone
            donor_address = f"{product.donated_by.restaurant_profile.street}, {product.donated_by.restaurant_profile.city}, {product.donated_by.restaurant_profile.state}, {product.donated_by.restaurant_profile.country} {product.donated_by.restaurant_profile.postal_code}".strip(
                ", ")
        elif hasattr(product.donated_by, 'foodbank'):
            donor_name = product.donated_by.foodbank.get_full_name()
            donor_phone = product.donated_by.foodbank.foodbank_phone
            donor_address = f"{product.donated_by.foodbank.street}, {product.donated_by.foodbank.city}, {product.donated_by.foodbank.state}, {product.donated_by.foodbank.country} {product.donated_by.foodbank.postal_code}".strip(
                ", ")
        else:
            donor_name = product.donated_by.username
            donor_phone = "Not provided"
            donor_address = "Not provided"

        donor_email = product.donated_by.email
        reserver_email = request.user.email
        subject = f"Donation Reservation for {product.name} - Reservation #{reservation.id}"

        # Emai donor
        message_to_donor = (
            f"Dear {donor_name},\n\n"
            f"Your product '{product.name}' has been reserved by {reserver_name}.\n\n"
            f"Reservation Details:\n"
            f"Reserved Quantity: {reservation.quantity}\n"
            f"Remaining Quantity: {product.quantity}\n\n"
            f"Reserver Contact Name: {reserver_name}\n"
            f"Reserver Contact Email: {request.user.email}\n"
            f"Reserver Phone Number: {reserver_phone}\n"
            f"Please coordinate with the reserver for pickup arrangements.\n\n"
            f"Best Regards,\nFoodConnect Team"
        )

        # Email reserver
        message_to_reserver = (
            f"Dear {reserver_name},\n\n"
            f"Thank you for reserving the product '{product.name}'.\n\n"
            f"Reservation Details:\n"
            f"Reserved Quantity: {reservation.quantity}\n\n"
            f"Pickup Details:\n"
            f"Donor Contact Name: {donor_name}\n"
            f"Donor Contact Email: {product.donated_by.email}\n"
            f"Donor Phone: {donor_phone}\n"
            f"Donor Address: {donor_address}\n\n"
            f"Please coordinate with the donor for pickup arrangements.\n\n"
            f"Best Regards,\nFoodConnect Team"
        )

        try:
            # Send emails
            send_mail(subject, message_to_donor, 'no-reply@foodconnect.com', [donor_email])
            send_mail(subject, message_to_reserver, 'no-reply@foodconnect.com', [reserver_email])
            messages.success(request,
                             'Reservation placed successfully! Emails have been sent to the donor and yourself.')
        except Exception as e:
            print(e)
            messages.warning(request,
                             'Reservation placed successfully, but we were unable to send email notifications.')

        #messages.success(request, "Reservation placed successfully!")
        return render(request, '../templates/donations/reservations_list.html')

    messages.error(request, "Invalid request.")
    return redirect('product_list')

@login_required
def view_reservations(request):
    #reservations = Reservation.objects.filter(product__donated_by=request.user).select_related('product')
    reservations = Reservation.objects.filter(user=request.user).select_related('product')
    return render(request, '../templates/donations/reservations_list.html', {"reservations":reservations})

@login_required
def donor_reservations(request):
    donor_products = Product.objects.filter(donated_by=request.user)

    # Reservations for the donors products
    reservations = Reservation.objects.filter(product__in=donor_products)

    return render(request, 'donations/donor_reservations_list.html', {'reservations': reservations})

# Donations by donor
@login_required
def donor_donations(request):
    # Fetch all donations made by the logged-in donor
    donations = Product.objects.filter(donated_by=request.user)

    return render(request, 'donations/donor_donations_list.html', {
        'donations': donations,
    })

@login_required
def update_donation(request, donation_id):
    donation = get_object_or_404(Product, id=donation_id, donated_by=request.user)

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():

            donation.name = form.cleaned_data['name']
            donation.description = form.cleaned_data['description']
            donation.category_id = form.cleaned_data['category']
            donation.quantity = form.cleaned_data['quantity']
            donation.weight = form.cleaned_data['weight']
            donation.unit = form.cleaned_data['unit']
            donation.expiry_date = form.cleaned_data['expiry_date']
            if form.cleaned_data['image']:
                donation.image = form.cleaned_data['image']
            donation.save()

            messages.success(request, "Donation updated successfully!")
            return redirect('donor_donations')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        # Pre-filled formm
        form = AddProductForm(initial={
            'name': donation.name,
            'description': donation.description,
            'category': donation.category_id,
            'quantity': donation.quantity,
            'weight': donation.weight,
            'unit': donation.unit,
            'expiry_date': donation.expiry_date,
            'image': donation.image,
        })

    return render(request, 'donations/create_donation.html', {
        'form': form,
        'donation': donation,
    })

@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Product, id=donation_id, donated_by=request.user)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, "Donation deleted successfully!")
        return redirect('donor_donations')

@login_required
def reservations_for_donation(request, donation_id):
    product = get_object_or_404(Product, id=donation_id, donated_by=request.user)
    reservations = Reservation.objects.filter(product=product)

    return render(request, 'donations/reservations_for_donation.html', {'product': product, 'reservations': reservations})

@login_required
def update_reservation_status(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.product.donated_by != request.user:
            messages.error(request, "You are not authorized to update this reservation.")
            return redirect('donor_reservations')

        new_status = request.POST.get('status')
        if new_status in dict(Reservation.STATUS_CHOICES):
            reservation.status = new_status
            reservation.save()
            messages.success(request, "Reservation status updated successfully!")
        else:
            messages.error(request, "Invalid status value.")

        return redirect('donor_reservations')
