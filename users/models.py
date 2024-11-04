from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)  # ID card image

    def __str__(self):
        return f"{self.user.username}'s profile"
