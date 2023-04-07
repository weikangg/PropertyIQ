import os
from ura_api import ura_api
from dotenv import load_dotenv
load_dotenv()
from django.apps import apps
from random import randint
from pyproj import Proj
import pyproj
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class Observer:
    def update(self, subject):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class PropertyListings(Subject):
    def __init__(self):
        super().__init__()

    def update_listings(self, request):
        # Put your existing savePropertyToDatabase function code here
        URA_API_KEY = os.getenv('URA_API_KEY')
        ura = ura_api.ura_api(URA_API_KEY)

        # Clear all the previous listings first
        apps.get_model('property', 'Property').objects.all().delete()
        quarters = ['23q1']
        # quarters = ['18q1', '18q2', '18q3', '18q4', '19q1', '19q2', '19q3', '19q4', '20q1', '20q2', '20q3', '20q4', '21q1', '21q2', '21q3', '21q4', '22q1', '22q2', '22q3', '22q4', '23q1']
        startTime = datetime.now()
        for quarter in quarters:
            raw_data = ura.private_residential_properties_rental_contract(quarter)
            data = raw_data[:200]
            print(len(data))
            property_item = {
                "project title" : None,
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

                svy21 = Proj("+proj=tmerc +lat_0=1.366666666666667 +lon_0=103.8333333333333 +k=1 +x_0=28001.642 +y_0=38744.572 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
                lat_long = Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

                if project.get('x') is None or project.get('y') is None:

                    # x,y = transformer.transform(project.get('x'), project.get('y'))
                    x,y = pyproj.transform(svy21, lat_long, data[0].get('x'), data[0].get('y'))
                else:
                    # x,y = transformer.transform(project.get('x'), project.get('y'))
                    x, y = pyproj.transform(svy21, lat_long, project.get('x'), project.get('y'))
                    # x,y = pyproj.Transformer.from_crs(svy21, lat_long, always_xy=True).transform(project.get('x'), project.get('y'))

                property_item['x'] = x
                property_item['y'] = y
                property_item['project'] = project.get('project')
                
                for property_i in project['rental']:
                    property_item['leaseDate'] = property_i.get('leaseDate')
                    year = '20' + property_item['leaseDate'][2:]
                    month = int(property_item['leaseDate'][:2])
                    if month in [1, 2, 3]:
                        quarter_start_month = 1
                    elif month in [4, 5, 6]:
                        quarter_start_month = 4
                    elif month in [7, 8, 9]:
                        quarter_start_month = 7
                    else:
                        quarter_start_month = 10
                    lease_Date = f"{year}-{quarter_start_month:02}-01"
                    print(lease_Date)
                    property_item['propertyType'] = property_i.get('propertyType')
                    property_item['district'] = property_i.get('district')
                    areaSqft = property_i.get('areaSqft')
                    # Case 1: '<=' is in the string. e.g. '<=1000'
                    if '<=' in areaSqft:
                        areaSqft = areaSqft.replace('<','').replace('=','').strip()
                        property_item['areaSqft'] = int(areaSqft)
                    # Case 2: '>' is in the string. e.g. '>5000'
                    elif '>' in areaSqft:
                        areaSqft = areaSqft.replace('>','').strip()
                        property_item['areaSqft'] = int(areaSqft)
                    # Case 3: No arrows. means it's given in a range. e.g. '5000-6000'
                    else:
                        areaSqftList = areaSqft.split('-')
                        property_item['areaSqft'] = int(areaSqftList[0]) + int(areaSqftList[1]) // 2
                        
                    if property_i.get('noOfBedRoom') is not None:
                        property_item['noOfBedRoom'] = property_i.get('noOfBedRoom')
                    # Give it a default of 3
                    else:
                        property_item['noOfBedRoom'] = 3
                    if property_item['noOfBedRoom'] == 'NA':
                        property_item['noOfBedRoom'] = str(randint(1,5))
                    property_item['rent'] = property_i.get('rent')

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
                            
                    property = apps.get_model('property', 'Property')(project_Title = property_item.get('project_Title'),street=property_item.get('street'),latitude=property_item.get('y'),
                                        longitude = property_item.get('x'),bedrooms=property_item.get('noOfBedRoom'), sqft = property_item.get('areaSqft'),
                                        leaseDate = lease_Date, propertyType = property_item.get('propertyType'), rent = property_item.get('rent'), photo_main = photo_link,
                                        photo_1 = inner_photo_link1,photo_2 = inner_photo_link2, photo_3 = inner_photo_link3)
                    property.save()
                    print(f"Saving {property}....")
        
        # Notify the observers after saving the properties
        self.notify()   
          
        endTime = datetime.now()
        timeTaken = endTime-startTime
        timeTakenFormatted = divmod(timeTaken.total_seconds(), 60)
        num_rows = apps.get_model('property', 'Property').objects.count()

        print("You might see the same project title being saved multiple times. This is perfectly fine as a project can have multiple rental flats. \nThe details of each rental flat will be different although their project title are the same.\n")
        print(f"Properties saved: {num_rows}")
        print(f"Time taken: {int(timeTakenFormatted[0])} minutes {int(timeTakenFormatted[1])} seconds")

