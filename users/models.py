from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('restaurant', 'Restaurant'),
    ('foodbank', 'Foodbank'),
    ('individual', 'Individual'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)  # ID card image
    #is_verified = models.BooleanField(default=False)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='individual')

    # General Feilds for the form
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # Role specific fields
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)
    restaurant_contact_number = models.CharField(max_length=50, blank=True, null=True)
    foodbank_name = models.CharField(max_length=255, blank=True, null=True)
    foodbank_contact_number = models.CharField(max_length=50, blank=True, null=True)

def __str__(self):
        return f"{self.user.username}'s profile"
