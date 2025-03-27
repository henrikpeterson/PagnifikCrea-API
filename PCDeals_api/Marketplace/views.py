from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render
from .serializers import *
from django.utils.timezone import localdate
from datetime import timedelta
from django.utils.timezone import now
# Create your views here.
from django.db import connection
from rest_framework.response import Response

from rest_framework import status 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def Sponsored_listing(request):
    Sp_listing = ProductListings.objects.filter(is_sponsored=True)

    Sp_ListingSerializer = ListingsSerializer(Sp_listing, many=True)

    return Response(Sp_ListingSerializer.data) 

@api_view(['GET'])
@permission_classes([AllowAny])
def All_listing(request):
    Sp_listing = ProductListings.objects.all()

    Sp_ListingSerializer = ListingsSerializer(Sp_listing, many=True)

    return Response(Sp_ListingSerializer.data) 

@api_view(['GET'])
@permission_classes([AllowAny])
def listing_details(request, listing_id):

    listing = get_object_or_404(ProductListings, id=listing_id) 

    listingSerializer = ListingsSerializer(listing) 
    
    return Response(listingSerializer.data) 

@api_view(['GET'])
@permission_classes([AllowAny])
def product_reviews(request, product_id):
    listing = get_object_or_404(ProductListings, id=product_id)
    reviews = ProductReview.objects.filter(product_id=product_id)
    serializer = ProductReviewSerializer(reviews, many=True)
    return Response(serializer.data) 

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Add_review(request):
    user = request.user
    serializer = ProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 