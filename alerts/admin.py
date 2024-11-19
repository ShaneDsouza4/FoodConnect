# alerts/admin.py
from django.contrib import admin
from .models import Alert, ResponseToDonation

admin.site.register(Alert)
admin.site.register(ResponseToDonation)
