from django.contrib import admin
from users.models import Profile, Restaurant, FoodBank

# Register your models here.
admin.site.register(Profile)
admin.site.register(Restaurant)
admin.site.register(FoodBank)