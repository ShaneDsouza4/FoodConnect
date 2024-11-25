from django.urls import path
from . import views

urlpatterns = [
    path('', views.donations_view, name='donations' ),
    path('create/', views.create_donation, name='create-donation'),

    path('product_detail/<int:product_id>/', views.product_view, name='product_detail' ),
    path('view_reservations/', views.view_reservations, name='view_reservations'),

    path('donor-reservations/', views.donor_reservations, name='donor_reservations'),

path('donations/<int:donation_id>/reservations/', views.reservations_for_donation, name='reservations_for_donation'),

path('reservations/<int:reservation_id>/update/', views.update_reservation_status, name='update_reservation_status'),

    path('place-order/', views.place_order, name='place_order'),
    path('my-donations/', views.donor_donations, name='donor_donations'),

    path('donation/<int:donation_id>/update/', views.update_donation, name='update-donation'),

    path('donation/<int:donation_id>/delete/', views.delete_donation, name='delete-donation'),
]
