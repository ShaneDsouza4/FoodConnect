# Create your models here.
# alerts/models.py

from django.db import models
from django.contrib.auth.models import User

class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emergency_alerts")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #For one time saving purppposes

    def _str_(self):
        return f"Emergency Alert from {self.user.username} created on {self.created_at}"