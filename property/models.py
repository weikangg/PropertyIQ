from django.db import models

# Create your models here.
class Property(models.Model):
    project_Title = models.CharField(max_length=200,blank=True, null=True)
    street = models.CharField(max_length=200, blank = True, null = True)
    x_coordinates = models.CharField(max_length=20, null = True, blank=True)
    y_coordinates = models.CharField(max_length=20, null = True, blank=True)
    bedrooms = models.CharField(max_length=10, null=True, blank= True, default = 0)
    sqft = models.CharField(max_length=20, null=True,blank=True)
    leaseDate = models.CharField(max_length=20, blank=True,null=True)
    propertyType = models.CharField(max_length=200, blank=True, null=True)
    rent = models.IntegerField(blank=True)
    photo_main = models.CharField(max_length=200, blank=True)
    photo_1 = models.CharField(max_length=200, blank=True)
    photo_2 = models.CharField(max_length=200, blank=True)
    photo_3 = models.CharField(max_length=200, blank=True)
    photo_4 = models.CharField(max_length=200, blank=True)
    photo_5 = models.CharField(max_length=200, blank=True)
    photo_6 = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.project_Title

class PropertyIQUser(models.Model):
    username = models.CharField(max_length=200)
    bookmarks = models.ForeignKey('Property', on_delete=models.DO_NOTHING)
