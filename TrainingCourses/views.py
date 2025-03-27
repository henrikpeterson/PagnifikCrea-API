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
from django.core.paginator import Paginator
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
def List_of_courses(request):
    course = Course.objects.all().order_by("-id") 
    
    page = request.GET.get('page', 1)  # ✅ Récupère le numéro de la page
    limit = request.GET.get('limit', 6)  # ✅ Récupère le nombre de cours par page

    paginator = Paginator(course, limit)  # ✅ Divise les cours en pages
    paginated_courses = paginator.get_page(page)

    course_serializer = CoursesSerializer(paginated_courses, many=True) 

    return Response({
        "results": course_serializer.data,  # ✅ Liste des cours
        "total_pages": paginator.num_pages,  # ✅ Nombre total de pages
        "current_page": page  # ✅ Page actuelle
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def Boosted_courses(request):
    course = Course.objects.filter(boosted=True) 

    course_serializer = CoursesSerializer(course, many=True) 

    return Response(course_serializer.data) 


@api_view(['GET'])
@permission_classes([AllowAny])
def course_details(request, course_id):
    course_details1 = get_object_or_404(Course, id=course_id)

    serializer = CoursesDetailsSerializer(course_details1)

    return Response(serializer.data) 

# ✅ Contenu d’un module (Page Vidéos & Documents)
@api_view(['GET'])
@permission_classes([AllowAny])
def module_content(request, module_id):
    module = get_object_or_404(Modules, id=module_id)

    serializer = ModuleContentSerializer(module)

    return Response(serializer.data)