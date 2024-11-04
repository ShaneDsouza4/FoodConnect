from django.urls import path
from .views import signup_view, home_view, landing_view, login_view, logout_view, emergency_alert_view, donate_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('home/', home_view, name='home'),
    path('signup/', signup_view, name='signup'),

    path('login/', login_view, name='login'),

    path('logout/', logout_view, name='logout'),
    path('emergency_alert/', emergency_alert_view, name='emergency_alert'),
    path('donate/', donate_view, name='donate'),
]
