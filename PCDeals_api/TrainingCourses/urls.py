from django.urls import path
from .views import List_of_courses, course_details, module_content, Boosted_courses
urlpatterns = [
   path('Lists_of_course/', List_of_courses, name="courses_list"),
   path('Boosted_course/', Boosted_courses, name="courses_list"),
   path('Courses_Details/<int:course_id>/', course_details, name="courses_details"),
   path('Module_Contents/<int:module_id>/', module_content, name="chapters"),
]

#Fabrication de sac a main en Batik
#maitriser l'art du batik et la fabrication d'accessoire a base de batik 