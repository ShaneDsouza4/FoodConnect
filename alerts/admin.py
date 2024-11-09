# alerts/admin.py
from django.contrib import admin
from .models import Alert  # Import the correct model class

admin.site.register(Alert)
