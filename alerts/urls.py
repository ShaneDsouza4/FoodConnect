from django.urls import path
from .views import emergency_alert_view
from . import views
urlpatterns = [
    path('emergency/', emergency_alert_view, name='emergency_alert'),
    path('create-alerts/', views.create_alert, name='alerts'),
]