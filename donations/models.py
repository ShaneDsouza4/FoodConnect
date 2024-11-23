from email.policy import default

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
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

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Donation {self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.product.quantity >= self.quantity:
            self.product.quantity -= self.quantity
            self.product.save()
        else:
            raise ValueError("Not enough quantity available.")
        super().save(*args, **kwargs)