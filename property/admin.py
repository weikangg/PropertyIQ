from django.contrib import admin
from .models import Property

# Register your models here.

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'street', 'project', 'x_coordinates', 'y_coordinates', 'propertyType', 'rental_price')
    list_display_links = ('id', 'title')
    list_filter = ('propertyType',)
    search_fields = ('title', 'street','propertyType', 'rental_price')
    list_per_page = 25

admin.site.register(Property, PropertyAdmin)