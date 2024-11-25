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
    #image=models.URLField(max_length=300, default='https://img.freepik.com/premium-vector/hand-drawn-food-bank-illustration_23-2149323575.jpg?w=1060')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_reserved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        user_name = self.user.username if self.user else "Unknown User"
        return f"Reservation {self.id}: {self.quantity} of {product_name} by {user_name}"


    def save(self, *args, **kwargs):
        if self.product.quantity >= self.quantity:
            self.product.quantity -= self.quantity
            self.product.save()
        else:
            raise ValueError("Not enough quantity available.")
        super().save(*args, **kwargs)