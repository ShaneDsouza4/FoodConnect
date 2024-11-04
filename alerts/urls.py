from django.urls import path
from .views import emergency_alert_view

urlpatterns = [
    path('emergency/', emergency_alert_view, name='emergency_alert'),
]