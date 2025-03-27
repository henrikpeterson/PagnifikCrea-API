from rest_framework import serializers

from UsersProfiles.models import SellerProfile
from .models import *
from authentication import models as user_models

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
       model = user_models.User 
       fields = ["id", "username", "PhoneNumber"]

#class qui nous permet de definir les champs a inclure ou a exclure quand on fait appels a un serializeur depuis une vue
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Appeler le constructeur de la classe parente normalement
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        # Vérifier si le contexte contient des champs à inclure ou exclure
        if 'context' in kwargs:
            fields = kwargs['context'].get('fields', None)
            exclude = kwargs['context'].get('exclude', None)

            if fields is not None:
                # Garder uniquement les champs spécifiés dans `fields`
                allowed = set(fields)
                existing = set(self.fields)
                for field_name in existing - allowed:
                    self.fields.pop(field_name)

            if exclude is not None:
                # Exclure les champs spécifiés dans `exclude`
                for field_name in exclude:
                    self.fields.pop(field_name)

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = ['user','rating', 'comment']
        
class ListingsSerializer(DynamicFieldsModelSerializer):
    short_description = serializers.SerializerMethodField()
    #seller = SimpleUserSerializer(read_only=True)
    specifications = SpecificationSerializer(many=True)
    reviews = ProductReviewSerializer(many=True, read_only=True) 
    seller = serializers.SerializerMethodField()  # ✅ Ajout du profil vendeur
    class Meta:
        model = ProductListings
        fields = ["id", "seller", "specifications", "title", "price", "location", "Description", "short_description","image", "status", "reviews"]
    
    def get_short_description(self, obj):
        return obj.Description[:100] + "..." if obj.Description else "" 
    
    def get_seller(self, obj):
        """ ✅ Retourne l'ID du SellerProfile au lieu du User """
        if obj.seller:
            seller_profile = SellerProfile.objects.filter(user=obj.seller).first()
            if seller_profile:
                return {
                    "id": seller_profile.id,  # ✅ C'est cet ID qu'on utilisera pour rediriger
                    "username": obj.seller.username,
                    "PhoneNumber": obj.seller.PhoneNumber
                }
        return None

    def create(self, validated_data):
        """ ✅ Créer une annonce avec des spécifications dynamiques """
        specs_data = validated_data.pop('specifications', [])  # Récupère les spécifications envoyées
        listing = ProductListings.objects.create(**validated_data)

        for spec in specs_data:
            spec_obj, _ = Specification.objects.get_or_create(
                key=spec['key'], value=spec['value']
            )
            listing.specifications.add(spec_obj)  # ✅ Ajoute la spécification à l'annonce

        return listing 