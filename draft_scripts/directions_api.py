import urllib.request
import json

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'CtmTYiHN8W6sefMsCkADJGXG'
origin = input('Where are you?: ').replace('','+')
destination = input('Where do you want to go?: ').replace('','+')

nav_request = 'origin=()&destination={}&Key={}'.format(origin,destination,api_key)

request = endpoint + nav_request
response = urllib.request.urlopen(request).read()
directions = json.loads(response)
print(directions)
