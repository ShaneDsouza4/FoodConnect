from email.policy import default

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Donation(models.Model):
    item = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    urgency_level = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('liters', 'Liters'),
        ('ml', 'Milliliters'),
    ]
    name = models.CharField(max_length=100)
    donated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    rating = models.PositiveIntegerField(default=0)
    amount_donated = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)
    image=models.URLField(max_length=300, default='https://img.freepik.com/premium-vector/hand-drawn-food-bank-illustration_23-2149323575.jpg?w=1060')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
