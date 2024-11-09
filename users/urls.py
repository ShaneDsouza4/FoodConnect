from django.urls import path
from .views import signup_view, home_view, landing_view, logout_view, emergency_alert_view, donate_view, \
    about_view
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', landing_view, name='landing'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('signup/', signup_view, name='signup'),

    path('restaurant/signup/', views.signup_restaurant, name='restaurant_signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    #path('logout/', logout_view, name='logout'),
    path('register/', views.register_user, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('emergency_alert/', emergency_alert_view, name='emergency_alert'),
    path('donate/', donate_view, name='donate'),
]
