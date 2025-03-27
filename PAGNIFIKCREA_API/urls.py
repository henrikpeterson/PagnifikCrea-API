"""
URL configuration for PCDeals_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from PAGNIFIKCREA_API import settings # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),

    path('apiv1/', include('TrainingCourses.urls')), 
    path('apiv2/', include('Marketplace.urls')),
    path('apiv3/', include('UsersProfiles.urls')),

    path('api/auth/', include('djoser.urls')),  # Ajoute les endpoints d'authentification
    path('api/auth/', include('djoser.urls.jwt')),  # Active l'authentification JWT
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)