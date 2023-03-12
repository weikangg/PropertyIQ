import os

from dotenv import load_dotenv
from ura_api import ura_api
import json
import sys
from property import models

load_dotenv()

URA_API_KEY = os.getenv('URA_API_KEY')

ura = ura_api.ura_api(URA_API_KEY)
data = ura.private_residential_properties_rental_contract('23q1')
# print(data) # will print out the whole data.
print(type(data[0]))  # type list
print()
print(len(data)) # 1886 rows in 2023 q1
print()
print(data[0]) # first element
print()

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
    property_item['street'] = project['street']
    property_item['x'] = project.get('x')
    property_item['y'] = project.get('y')
    property_item['project'] = project['project']
    
    for property in project['rental']:
        property_item['leaseDate'] = property['leaseDate']
        property_item['propertyType'] = property['propertyType']
        property_item['district'] = property['district']
        property_item['areaSqft'] = property['areaSqft']
        property_item['noOfBedRoom'] = property['noOfBedRoom']
        property_item['rent'] = property['rent']
        property_list.append(property_item)
        property = models.Property(street=property_item['street'],x_coordinates=property_item.get('x'),
                            y_coordinates = property_item.get('y'),bedrooms=property_item['noOfBedRoom'], sqft = property_item['areaSqft'],
                            leaseDate = property_item['leaseDate'], propertyType = property_item['propertyType'], rent = property_item['rent'])
        property.save()


# store it into json file for now , not database yet
with open("./test/propertyData.json", "w") as outfile:
    json.dump(data[:5], outfile, indent = 4)