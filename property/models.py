from django.db import models
from datetime import datetime
from bookmarks.models import Bookmark

# Create your models here.
class Property(models.Model):
    project_Title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    x_coordinates = models.CharField(max_length=20)
    y_coordinates = models.CharField(max_length=20)
    bedrooms = models.CharField(max_length=10)
    sqft = models.CharField(max_length=20)
    leaseDate = models.DateField(default = datetime.now, blank=True)
    propertyType = models.CharField(max_length=200)
    rental_price = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    list_date = models.DateTimeField(default = datetime.now, blank = True)
    bookmark = models.OneToOneField(to=Bookmark, on_delete=models.CASCADE)
    def __str__(self):
        return self.project_Title


