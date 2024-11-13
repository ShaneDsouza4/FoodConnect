# Create your models here.
# alerts/models.py

from django.db import models
from django.contrib.auth.models import User


class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emergency_alerts")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #For one time saving purppposes

    # def _str_(self):
    #     return f"Emergency Alert from {self.user.username} created on {self.created_at}"

class Alert(models.Model):
    item_name = models.CharField(max_length=100)
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

class ResponseToDonation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="responses")
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


