import os
from ura_api import ura_api
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render
from .models import Property
from .models import Property
# Create your views here.

def savePropertyToDatabase():
    URA_API_KEY = os.getenv('URA_API_KEY')

    ura = ura_api.ura_api(URA_API_KEY)
    data = ura.private_residential_properties_rental_contract('23q1')

    property_list = []

    property_item = {
        "street": None,
        "x": None,
        "y": None,
        "project": None,
        "areaSqm": None,
        "leaseDate": None,
        "propertyType": None,
        "district": None,
        "areaSqFt": None,
        "noOfBedRoom": None,
        "rent": None 
    }


    for project in data:
        property_item['project_Title'] = project.get('project')
        property_item['street'] = project.get('street')
        property_item['x'] = project.get('x')
        property_item['y'] = project.get('y')
        property_item['project'] = project.get('project')
        
        for property in project['rental']:
            property_item['leaseDate'] = property.get('leaseDate')
            property_item['propertyType'] = property.get('propertyType')
            property_item['district'] = property.get('district')
            property_item['areaSqft'] = property.get('areaSqft')
            property_item['noOfBedRoom'] = property.get('noOfBedRoom')
            property_item['rent'] = property.get('rent')
            property_list.append(property_item)
            # property = Property(project_Title = property_item.get('project_Title'),street=property_item.get('street'),x_coordinates=property_item.get('x'),
            #                     y_coordinates = property_item.get('y'),bedrooms=property_item.get('noOfBedRoom'), sqft = property_item.get('areaSqft'),
            #                     leaseDate = property_item.get('leaseDate'), propertyType = property_item.get('propertyType'), rent = property_item.get('rent'))
            # property.save()


def index(request):
    pass

def property(request):
    pass

savePropertyToDatabase()