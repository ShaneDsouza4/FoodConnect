from django.urls import path
from .views import donations_view
from . import views

urlpatterns = [
    path('', views.donations_view, name='donations' ),
    path('create/', views.create_donation, name='create-donation'),

    path('product_detail/<int:product_id>/', views.product_view, name='product_detail' ),
    path('place-order/', views.place_order, name='place_order'),

]
