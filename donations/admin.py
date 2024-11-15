from django.contrib import admin

from donations.models import Donation, Category, Product

# Register your models here.
admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Product)
