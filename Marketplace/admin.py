from django.contrib import admin
from .models import ProductListings, ListingsGallery, Specification, ProductReview
# Register your models here.

class GalleryInline(admin.TabularInline):
    model = ListingsGallery

class SpecificationInlines(admin.TabularInline):
    model = Specification

class ProductReviewInline(admin.TabularInline):
    model = ProductReview

class ListingsAdmin(admin.ModelAdmin):
    inlines = [GalleryInline,SpecificationInlines,ProductReviewInline]
    
    list_display = ['title', 'price', 'listing_image','status']

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['listing', 'key', 'value']

admin.site.register(ProductListings, ListingsAdmin)
admin.site.register(Specification, SpecificationAdmin)  


