from django.urls import path 
from .views import *

urlpatterns = [
    path('Profiles/<int:seller_id>', get_seller_profile, name="Seller-profiles"),
    path("private-profile/", get_private_profile, name="private-profile"),
]
