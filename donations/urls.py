from django.urls import path
from .views import donations_view
from . import views

urlpatterns = [
    path('', views.donations_view, name='donations' ),
    # path('category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),

    path('create/', views.create_donation, name='create-donation' ),

]
