# Importing libraries
import requests
import json
import pandas as pd

# Reading the JSON file from the torontopolice.on.ca
response = requests.get('https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/KSI/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')

data = json.loads(response.text)

# Declaring a list of attributes empty
attr = []

# Getting only the attribute list and inserting into the attr list.
for i in range(0,len(data['features'])):
    # print(data['features'][i]['attributes'])
    attr.append(data['features'][i]['attributes'])

df = pd.DataFrame(attr)

print(df)


