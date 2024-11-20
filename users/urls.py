from django.urls import path
from .views import signup_view, home_view, landing_view, logout_view, emergency_alert_view, donate_view, \
    about_view, signup_individual
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', landing_view, name='landing'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('signup/', signup_individual, name='individual_signup'),
    path('restaurant/signup/', views.signup_restaurant, name='restaurant_signup'),
    path('foodbank/signup/', views.signup_foodbank, name='foodbank_signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    #path('logout/', logout_view, name='logout'),
    path('register/', views.register_user, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='webpages/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='webpages/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='webpages/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='webpages/password_reset_complete.html'), name='password_reset_complete'),
    path('emergency_alert/', emergency_alert_view, name='emergency_alert'),
    path('donate/', donate_view, name='donate'),
    path('contact/', views.contact_view, name='contact_us'),

    path('profile/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
