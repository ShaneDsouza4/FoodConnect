from django.db import models
from django.contrib.auth.models import User

CANADA_PROVINCES_AND_TERRITORIES = [
    ('', 'Select State'),
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

# Indiviual
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, choices=CANADA_PROVINCES_AND_TERRITORIES, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # Metrics for analyticcs
    total_donations = models.IntegerField(default=0)
    donation_frequency = models.IntegerField(default=0)
    donation_variety_count = models.IntegerField(default=0)
    donation_volume = models.FloatField(default=0.0)
    average_rating = models.FloatField(blank=True, null=True)
    response_to_emergency_count = models.IntegerField(default=0)

    def get_full_name(self):
       return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.user.username}'s profile"

# Restauraant
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    restaurant_name = models.CharField(max_length=255)
    restaurant_phone = models.CharField(max_length=20)
    email = models.EmailField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=CANADA_PROVINCES_AND_TERRITORIES)
    country = models.CharField(max_length=100, default='Canada')
    postal_code = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # Metrics for analyticcs
    total_donations = models.IntegerField(default=0)
    donation_frequency = models.IntegerField(default=0)
    donation_variety_count = models.IntegerField(default=0)
    donation_volume = models.FloatField(default=0.0)
    average_rating = models.FloatField(blank=True, null=True)
    response_to_emergency_count = models.IntegerField(default=0)

    def get_full_name(self):
       return self.restaurant_name

    def __str__(self):
        return f"{self.user.username} - {self.restaurant_name}"

# Foodbank
class FoodBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='foodbank')
    foodbank_name = models.CharField(max_length=255)
    foodbank_phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    id_verification = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    emergency_alerts_count = models.IntegerField(default=0)

    def get_full_name(self):
       return self.foodbank_name

    def __str__(self):
        return f"{self.user.username}'s Food Bank"

