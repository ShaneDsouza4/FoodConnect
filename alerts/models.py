# Create your models here.
# alerts/models.py

from django.db import models
from django.contrib.auth.models import User


class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emergency_alerts")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #For one time saving purppposes


class Alert(models.Model):
    item_name = models.CharField(max_length=100)
    original_quantity = models.PositiveIntegerField(default=0)
    quantity_needed = models.PositiveIntegerField()
    urgency_level = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_alerts"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name}-{self.created_by}"

#View that is used
class ResponseToDonation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    PICKUP_METHOD_CHOICES = [
        ('pickup', 'Pickup by Food Bank'),
        ('delivery', 'Delivery by Donor'),
    ]
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="responses")
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    quantity_donated = models.PositiveIntegerField(default=0)
    pickup_method = models.CharField(
        max_length=20,
        choices=PICKUP_METHOD_CHOICES,
        default='pickup'
    )
    pickup_delivery_date = models.DateField(blank=True, null=True)
    donor_address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} - {self.alert.item_name}"


