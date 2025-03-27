from django.contrib import admin
from .models import SellerProfile, Certificat
# Register your models here.
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'is_trainer', 'total_courses_completed', 'total_product', 'average_seller_rating']
    search_fields = ['user__username', 'location']

class CertificatAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'issued_at']

admin.site.register(SellerProfile, SellerProfileAdmin)
admin.site.register(Certificat, CertificatAdmin) 

