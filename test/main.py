import os

from dotenv import load_dotenv
from ura_api import ura_api
import json

load_dotenv()

URA_API_KEY = os.getenv('URA_API_KEY')

ura = ura_api.ura_api(URA_API_KEY)
data = ura.private_residential_properties_rental_contract('23q1')
# print(data) # will print out the whole data.
print(type(data))  # type list
print()
print(len(data)) # 1886 rows in 2023 q1
print()
print(data[0]) # first element
print()
print(data[0]['rental'][0]['rent']) # get rent of first element

# store it into json file for now , not database yet
with open("./test/propertyData.json", "w") as outfile:
    json.dump(data[:5], outfile, indent = 4)