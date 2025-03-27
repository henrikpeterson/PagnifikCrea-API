from django.urls import path 
from .views import *

urlpatterns = [
    path('marketplace/listings/', Sponsored_listing, name="Sponsored-listing"),
    path('marketplace/listing_review/<int:product_id>/', product_reviews, name="review-listing"),
    path('marketplace/listings/all/', All_listing, name="All-listing"),
    path('marketplace/listings/<int:listing_id>/', listing_details, name='listing-detail')

]