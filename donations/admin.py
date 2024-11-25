from django.contrib import admin

from donations.models import Reservation, Category, Product

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Category)
admin.site.register(Product)
