from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    project_Title = models.CharField(max_length=200,blank=True, null=True)
    street = models.CharField(max_length=200, blank = True, null = True)
    latitude = models.DecimalField(max_digits=20,decimal_places=15, null = True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places = 15,null = True, blank=True)
    bedrooms = models.CharField(max_length=10, null=True, blank= True, default = 0)
    sqft = models.CharField(max_length=20, null=True,blank=True)
    leaseDate = models.DateField(auto_now=True)
    propertyType = models.CharField(max_length=200, blank=True, null=True)
    rent = models.IntegerField(blank=True)
    photo_main = models.CharField(max_length=200, blank=True)
    photo_1 = models.CharField(max_length=200, blank=True)
    photo_2 = models.CharField(max_length=200, blank=True)
    photo_3 = models.CharField(max_length=200, blank=True)
    # Every user that adds a property to their bookmarks, that individual property has a bookmarks field where the individual ID resides
    # we can look for all the properties where the USER ID is.
    bookmarks = models.ManyToManyField(User, related_name='bookmark', default = None, blank = True)
    def __str__(self):
        return self.project_Title

class UserProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Project Title: {self.property.project_Title} User: {self.user.username}"

    class Meta:
        unique_together = ('user', 'property',)
