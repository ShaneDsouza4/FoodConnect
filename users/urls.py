from django.urls import path
from .views import signup_view, home_view, landing_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('home/', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
]
