from django.urls import path
from . import views

urlpatterns = [
    # URL for List of all donations
    path('', views.donations_view, name='donations' ),

    # URL to create reservation
    path('create/', views.create_donation, name='create-donation'),

    #URL to view single product
    path('product_detail/<int:product_id>/', views.product_view, name='product_detail' ),

    #URL to reserver to see the donations the reserved
    path('view_reservations/', views.view_reservations, name='view_reservations'),

    #URL for donor to see the reservations made against their donations
    path('donor-reservations/', views.donor_reservations, name='donor_reservations'),

    #URL for donor to make the reservation status,after the reserver reserves the donation
    path('reservations/<int:reservation_id>/update/', views.update_reservation_status, name='update_reservation_status'),

    #URL reserver to reserve the donation product
    path('place-order/', views.place_order, name='place_order'),

    #URL for donor to see the donations they made
    path('my-donations/', views.donor_donations, name='donor_donations'),

    #URL for donor to update the donations they made
    path('donation/<int:donation_id>/update/', views.update_donation, name='update-donation'),

    #URL for donor to delete the donations they made
    path('donation/<int:donation_id>/delete/', views.delete_donation, name='delete-donation'),
]
