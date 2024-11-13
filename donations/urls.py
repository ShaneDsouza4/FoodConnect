from django.urls import path
from .views import donations_view
from . import views

urlpatterns = [
    path('', views.donations_view, name='donations' ),
    path('create/', views.create_donation, name='create-donation' ),

]
