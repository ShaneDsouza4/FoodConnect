#alerts/urls.py
from django.urls import path
from .views import emergency_alert_view
from . import views
urlpatterns = [
    path('create-alerts/', views.create_alert, name='alerts'),
    path('alerts/', views.alert_list, name='alert_list'),
    path('alerts/respond-to-donation/<int:alert_id>/', views.ResponseToDonationView, name='respond_to_donation'),
    path('response/<int:response_id>/status/', views.ResponseStatusView, name='response_status'),
    path('donate/<int:alert_id>/', views.ResponseToDonationView, name='donate'),
]