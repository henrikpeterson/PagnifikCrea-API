from rest_framework import serializers
from .models import Course, Modules, SkillsLearn
from authentication import models as user_models

class CoursesSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "price", "duration", "short_description", "image", "status"]

    def get_short_description(self, obj):
        return obj.description[:100] + "..." if obj.description else "" 

class ModuleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ["id", "title","status", "description"] 

class SkillsLearnSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsLearn
        fields = ["title"] 

class CoursesDetailsSerializer(serializers.ModelSerializer):
    modules = ModuleSerializers(many=True)

    skills = SkillsLearnSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__' 

    def get_modules(self, obj):
        return Modules.objects.filter(course=obj).values("id", "title", "status","duration", "description")

    def get_skills(self, obj):
        return SkillsLearn.objects.filter(course=obj).values("id", "title")
    
# Serializer pour afficher les vidéos et documents d’un module
class ModuleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ["id", "title", "video", "document"] 
