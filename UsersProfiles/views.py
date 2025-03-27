from django.shortcuts import render
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
def get_seller_profile(request, seller_id):
    seller = get_object_or_404(SellerProfile, id=seller_id)
    sellerSerializer = SellerProfileSerializer(seller)
    return Response(sellerSerializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_article(request, pk):
    try:
        seller = SellerProfile.objects.get(id=pk)
    except SellerProfile.DoesNotExist:
        return Response({"error": "Vendeur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SellerProfileSerializer(seller, data=request.data)  # Utilisez request.data ici
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_private_profile(request):
    try:
        profile = SellerProfile.objects.get(user=request.user)  # ✅ Trouver le profil du vendeur
        serializer = UserPrivateProfileSerializer(profile)  # ✅ Sérialiser le profil
        return Response(serializer.data, status=status.HTTP_200_OK)
    except SellerProfile.DoesNotExist:
        return Response({"error": "Profil vendeur introuvable."}, status=status.HTTP_404_NOT_FOUND)
    