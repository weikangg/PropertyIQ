import os
from ura_api import ura_api
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render
from .models import Property
from random import randint
from pyproj import Transformer
from latLongConverter import SVY21

# Create your views here.

def savePropertyToDatabase():
    URA_API_KEY = os.getenv('URA_API_KEY')
    cv = SVY21()
    ura = ura_api.ura_api(URA_API_KEY)
    year = '23'
    quarter = '1'
    string = year + 'q' + quarter
    data = ura.private_residential_properties_rental_contract(string)

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

        # Temporary Fix
        if project.get('x') is None or project.get('y') is None:
            x,y = float(data[0].get('x')), float(data[0].get('y'))
        else:
            x,y = float(project.get('x')),float(project.get('y'))   
        
        lat, lon = cv.computeLatLon(x, y)
        property_item['x'] = lat
        property_item['y'] = lon
        property_item['project'] = project.get('project')
        
        for property in project['rental']:
            property_item['leaseDate'] = property.get('leaseDate')
            year = '20' + property_item['leaseDate'][2:]
            if property_item['leaseDate'][:2] == '01':
                month = '01'
            elif property_item['leaseDate'][:2] == '02':
                month = '04'
            elif property_item['leaseDate'][:2] == '03':
                month = '07'
            else:
                month = '10'
            day = '01'
            lease_Date = f"{year}-{month}-{day}"
            property_item['propertyType'] = property.get('propertyType')
            property_item['district'] = property.get('district')
            property_item['areaSqft'] = property.get('areaSqft')
            property_item['noOfBedRoom'] = property.get('noOfBedRoom')
            if property_item['noOfBedRoom'] == 'NA':
                property_item['noOfBedRoom'] = str(randint(1,5))
            property_item['rent'] = property.get('rent')
            property_list.append(property_item)
            random_index = randint(1,6)
            photo_link = 'img/home-' + str(random_index) + '.jpg'
            for i in range(3):
                random_index = randint(1,6)
                if i == 0:
                    inner_photo_link1 = 'img/home-inside' + str(random_index) + '.jpg'
                elif i == 1:
                    inner_photo_link2 = 'img/home-inside' + str(random_index) + '.jpg'
                else:
                    inner_photo_link3 = 'img/home-inside' + str(random_index) + '.jpg'
                    
            property = Property(project_Title = property_item.get('project_Title'),street=property_item.get('street'),latitude=property_item.get('x'),
                                longitude = property_item.get('y'),bedrooms=property_item.get('noOfBedRoom'), sqft = property_item.get('areaSqft'),
                                leaseDate = lease_Date, propertyType = property_item.get('propertyType'), rent = property_item.get('rent'), photo_main = photo_link,
                                photo_1 = inner_photo_link1,photo_2 = inner_photo_link2, photo_3 = inner_photo_link3)
            property.save()


def index(request):
    if request.user.is_superuser:
        savePropertyToDatabase()
    return render(request,'pages/index.html')

def property(request):
    pass
