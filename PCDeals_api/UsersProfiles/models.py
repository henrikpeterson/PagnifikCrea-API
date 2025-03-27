from django.db import models
from authentication import models as user_models
from Marketplace.models import ProductListings 
from TrainingCourses.models import Course  # ✅ Import du modèle Course

# Create your models here.
RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"), 
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"), 
)

class SellerProfile(models.Model):
    user = models.OneToOneField(user_models.User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="profiles/", default="profiles/utilisateur.png")
    location = models.CharField(max_length=255, blank=True, null=True)
    is_trainer = models.BooleanField(default=False)  # ✅ Indique si l'utilisateur est une formatrice
    joined_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_courses_completed(self):
        return self.user.courses_followed.count()  # ✅ Nombre total de formations suivies
    
    @property
    def Certifications(self):
        return self.user.certifications.count()  
    
    @property
    def total_product(self):
        return self.user.product_owned.count() 
    
    @property
    def average_seller_rating(self):
        reviews = self.user.product_owned.all().values_list("reviews__rating", flat=True)  # ✅ Récupère les notes des produits
        valid_reviews = [rating for rating in reviews if rating is not None]
        return round(sum(valid_reviews) / len(valid_reviews), 1) if valid_reviews else 0  # ✅ Moyenne arrondie à 1 décimale

    def __str__(self):
        return self.user.username

class Certificat(models.Model):
    students = models.ManyToManyField(user_models.User, related_name="certifications")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="certifications")  # ✅ Lien avec une formation
    title = models.CharField(max_length=255)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to="certificates/", blank=True, null=True)  # ✅ PDF du certificat
    
    def number_of_certificate(self):
        return self.students.count()

    def __str__(self):
        return f"{self.title} - {self.course.title}"  # ✅ Affiche le titre de la formation
