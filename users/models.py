from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('restaurant', 'Restaurant'),
    ('foodbank', 'Foodbank'),
    ('individual', 'Individual'),
]

CANADA_PROVINCES_AND_TERRITORIES = [
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'),
    ('NL', 'Newfoundland and Labrador'),
    ('NS', 'Nova Scotia'),
    ('ON', 'Ontario'),
    ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'),
    ('SK', 'Saskatchewan'),
    ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'),
    ('YT', 'Yukon')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='individual')

    # General fields
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, choices=CANADA_PROVINCES_AND_TERRITORIES, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # Restaurant
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)

    # Metrics for ranking (Harsh & Nishtha assistance)
    total_donations = models.IntegerField(default=0)  # Number of donations made
    donation_frequency = models.FloatField(default=0.0)  # How often donations are made
    donation_variety_count = models.IntegerField(default=0)  # Number of different types of items donated
    donation_volume = models.FloatField(default=0.0)  # Total volume of items donated
    average_rating = models.FloatField(blank=True, null=True)  # Average rating from feedback
    response_to_emergency_count = models.IntegerField(default=0)  # Times responded to emergency alerts

    # Foodbank-specific fields
    foodbank_name = models.CharField(max_length=255, blank=True, null=True)
    total_reservations = models.IntegerField(default=0)
    emergency_alerts_count = models.IntegerField(default=0)

    reviews_given = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
