from django.contrib import admin

from .models import Course, Modules, SkillsLearn
# Register your models here.

class SkillsInlines(admin.TabularInline):
    model = SkillsLearn
    extra = 1

class LessonInlines(admin.TabularInline):
    model = Modules
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [SkillsInlines, LessonInlines]
    
    list_display = ['title', 'course_image', 'price', 'duration', 'students_count', 'module_count']

    def module_count(self, obj):
        return obj.number_of_module
    module_count.short_description = "Nombre de chapitre"

    def students_count(self, obj):
        return obj.total_students()
    students_count.short_description = "Nombre d'eleve"


admin.site.register(Course, CourseAdmin)
admin.site.register(Modules)
admin.site.register(SkillsLearn)
