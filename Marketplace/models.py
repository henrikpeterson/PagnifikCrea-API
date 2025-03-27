from django.db import models
from shortuuid.django_fields import ShortUUIDField, ShortUUID
from django.utils.html import mark_safe
from django.utils.text import slugify
from authentication import models as user_models
from django.db.models import Avg

STATUS = (
    ("Published", "Published"),
    ("Disabled", "Disabled"),
    ("isSponsored", "isSponsored")
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"), 
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"), 
)

# Create your models here.
class ProductListings(models.Model):
    title = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255) 

    Description = models.TextField() 
    Published_Date = models.DateTimeField(auto_now_add=True) 

    image = models.ImageField(upload_to='Computer_image', blank=True, null=True, default="product.png")
    seller = models.ForeignKey(user_models.User, related_name="product_owned", on_delete=models.SET_NULL, null=True, blank=True) 

    is_sponsored = models.BooleanField(blank=True, null=True, default=False)
    status = models.CharField(choices=STATUS, max_length=25, default="Published")
    sku = ShortUUIDField(unique=True, length=5, max_length=50, prefix="SKU", alphabet="1234567890") 

    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title 
    
    def listing_image(self):
        """ Afficher l'image dans Django Admin """
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        return "Pas d'image"
    
    @property
    def average_rating(self):
        result = self.reviews.aggregate(avg_rating=Avg("rating"))  # ✅ Calcul de la moyenne
        return round(result["avg_rating"], 1) if result["avg_rating"] is not None else 0  # ✅ Arrondi à 1 décimale

    class Meta :
       verbose_name_plural = "Products Listings" 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + ShortUUID().uuid()[:2].lower()
        super().save(*args, **kwargs) 

class ListingsGallery(models.Model):
    listing = models.ForeignKey(ProductListings, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Computer_image', blank=True, null=True, default="Listing.png")
    gallery_id = ShortUUIDField(length=5, max_length=50, prefix="SKU", alphabet="1234567890")

    def __str__(self):
        return f"{self.listing.title} - image" 
    
    class Meta :
       verbose_name_plural = "ListingsImages"

class Specification(models.Model):
    listing = models.ForeignKey(ProductListings, on_delete=models.CASCADE, related_name="specifications")
    key = models.CharField(max_length=255)  # Ex: "Processeur"
    value = models.CharField(max_length=255)  # Ex: "Intel Core i9-13900K"

    def __str__(self):
        return f"{self.key}: {self.value}"
    
    class Meta :
       verbose_name_plural = "Specifications"

class ProductReview(models.Model):
    product = models.ForeignKey(ProductListings, on_delete=models.CASCADE, related_name="reviews")  # ✅ Avis lié à un produit
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="reviews_given")  # ✅ Qui a donné l'avis
    rating = models.IntegerField(choices= RATING, default=1)  # ✅ Note de 1 à 5
    comment = models.TextField(blank=True, null=True)  # ✅ Commentaire facultatif
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Date de l'avis

    class Meta:
        unique_together = ["product", "user"]  # ✅ Un utilisateur ne peut évaluer un produit qu'une seule fois

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.product.title} - {self.rating}/5"
    