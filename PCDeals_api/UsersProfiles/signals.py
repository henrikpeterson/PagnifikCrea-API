from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User  # ✅ Import du modèle User
from .models import SellerProfile  # ✅ Import du modèle SellerProfile

@receiver(post_save, sender=User)
def create_seller_profile(sender, instance, created, **kwargs):
    """ ✅ Crée automatiquement un profil vendeur quand un utilisateur s’inscrit """
    if created:  # Si c’est un nouvel utilisateur
        SellerProfile.objects.create(user=instance)
        