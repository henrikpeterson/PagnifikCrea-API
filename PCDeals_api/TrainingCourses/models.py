from django.db import models
from authentication import models as user_models
from django.utils.html import mark_safe
# Create your models here.

# Create your models here.
Level= (
    ("Debutant", "Debutant"),
    ("Intermediare", "Intermediare"),
    ("Avancee", "Avancee")
)

Type=(
    ("Premium", "Premium"),
    ("Gratuit", "Gratuit")
)

class Course(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Training_Image', blank=True, null=True, default="product.png")

    trainer = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True, related_name="courses_taught")
    students = models.ManyToManyField(user_models.User, related_name="courses_followed", blank=True)

    duration = models.CharField(max_length=20, default="0 min")
    
    boosted = models.BooleanField(blank=True, null=True, default=False)
    
    status = models.CharField(choices=Level, max_length=25, default="Debutant")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 0.00 si gratuit

    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_students(self):
        return self.students.count()  # ✅ Permet de compter les inscrits
    
    def get_progress(self, user):
        """ ✅ Calculer la progression de l'utilisateur pour ce cours """
        total_modules = self.modules.count()  # ✅ Nombre total de modules
        completed_modules = self.modules.filter(completed_by=user).count()  # ✅ Modules complétés par l'utilisateur

        if total_modules == 0:
            return "0%"  # ✅ Éviter la division par zéro

        progress = (completed_modules / total_modules) * 100  # ✅ Calcul du %
        return f"{round(progress)}%" 

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    @property
    def number_of_module(self):
        return self.modules.count()
    
    def course_image(self):
        """ Afficher l'image dans Django Admin """
        if self.image:
           return mark_safe(f'<img src="{self.image.url}" width="75" height="50"/>')  # ✅ Utilise f-string
        return "Pas d'image"

    def __str__(self):
        return self.title
    

class Modules(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)

    video = models.FileField(upload_to="videos/")
    duration = models.CharField(max_length=20, default="0 min")
    description = models.TextField(default="Bienvenue dans ce module")  

    document = models.FileField(upload_to="lessons/", blank=True, null=True)  # ✅ PDF ou autre fichier
    status = models.CharField(choices=Type, max_length=25, default="Gratuit")
    order = models.PositiveIntegerField()  # ✅ Ordre d'affichage
    completed_by = models.ManyToManyField(user_models.User, related_name="completed_modules", blank=True)

    def __str__(self):
        return self.title

    class Meta :
       verbose_name_plural = "Modules"

class SkillsLearn(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="skills")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta :
       verbose_name_plural = "SkillsLearn"
