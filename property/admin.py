from django.contrib import admin
from .models import Property

# Register your models here.

# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ('id', 'project_Title', 'street', 'x_coordinates', 'y_coordinates', 'propertyType', 'rental_price')
#     list_display_links = ('id', 'project_Title')
#     list_filter = ('propertyType',)
#     search_fields = ('project_Title', 'street','propertyType', 'rental_price')
#     list_per_page = 25

# admin.site.register(Property, PropertyAdmin)