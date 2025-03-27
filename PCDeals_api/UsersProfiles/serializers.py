from PAGNIFIKCREA_API import settings
from .models import SellerProfile
from rest_framework import serializers
from .models import SellerProfile, Certificat
from Marketplace.models import ProductListings
from authentication.models import User

class simpleproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListings
        fields = ["id", "title", "price", "location", "Description", "image"]

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
       model = User 
       fields = ["id","email","username", "PhoneNumber"]

class SellerProfileSerializer(serializers.ModelSerializer):
    average_seller_rating = serializers.ReadOnlyField()  # ✅ Affiche la note moyenne du vendeur
    total_product = serializers.ReadOnlyField()  # ✅ Affiche le nombre total de produits vendus
    products = serializers.SerializerMethodField()
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = ["user", "bio", "photo", "location", "is_trainer", "joined_at", "total_product", "average_seller_rating", "products"]
    
    def get_products(self, obj):
        products = ProductListings.objects.filter(seller=obj.user)  # ✅ Récupère les produits du vendeur
        return simpleproductSerializer(products, many=True).data  # ✅ Sérialisation des produits

class CertificateSerializer(serializers.ModelSerializer):
    """ ✅ Sérialiseur des certificats obtenus """
    class Meta:
        model = Certificat
        fields = ["title", "issued_at", "certificate_file"]

class UserPrivateProfileSerializer(serializers.ModelSerializer):
    """ ✅ Sérialiseur du profil privé de l'utilisateur """
    total_courses_followed = serializers.SerializerMethodField()
    average_seller_rating = serializers.ReadOnlyField()  # ✅ Affiche la note moyenne du vendeur
    courses_progress = serializers.SerializerMethodField()
    certificates = serializers.SerializerMethodField() 
    photo = serializers.SerializerMethodField()

    products = serializers.SerializerMethodField()
    user = SimpleUserSerializer(read_only=True)
    total_product = serializers.ReadOnlyField()

    class Meta:
        model = SellerProfile
        fields = [
            "bio", "user", "photo", "location",  
            "total_courses_followed", "courses_progress", "certificates",
            "total_product", "average_seller_rating", "products"
        ]

    def get_certificates(self, obj):
        return obj.user.certifications.count()  # ✅ Nombre total de certificats obtenus
    
    def get_total_courses_followed(self, obj):
        """ ✅ Nombre total de cours suivis """
        return obj.user.courses_followed.count()
    
    def get_courses_progress(self, obj):
        """ ✅ Progression des cours suivis (exemple simplifié) """
        return [
            {"course": course.title, 
             "image": course.image.url,
             "progress": course.get_progress(obj.user)}  # ✅ Utilise la méthode get_progress
            for course in obj.user.courses_followed.all()
        ]

    def get_total_products_sold(self, obj):
        """ ✅ Nombre total de produits vendus """
        Owned_products = ProductListings.objects.filter(seller=obj.user)
        return Owned_products.count()

    def get_products(self, obj):
        """ ✅ Liste des produits vendus """
        products = ProductListings.objects.filter(seller=obj.user)
        return simpleproductSerializer(products, many=True).data 
    
    def get_photo(self, obj):
        request = self.context.get("request")
        if request:
            if obj.photo:
                return request.build_absolute_uri(obj.photo.url)
            return request.build_absolute_uri(settings.MEDIA_URL + "profiles/utilisateur.png")
        return obj.photo.url if obj.photo else settings.MEDIA_URL + "profiles/utilisateur.png"  # ✅ Fallback si pas de request