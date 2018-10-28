from googleapiclient.discovery import build
import pandas as pd
import pprint
import json

my_api_key = 'your api key'
my_cse_id = 'your cse id '
my_search_term = 'Data Science Jobs Toronto'


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build('customsearch', 'v1', developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search(

    my_search_term, my_api_key, my_cse_id, num=10)

urls = []
# Getting only the attribute list and inserting into the url list.
for i in range(0,len(results[2]['pagemap']['listitem'])):
    # print(results['features'][i]['attributes'])
    urls.append(results[2]['pagemap']['listitem'][i]['url'])

# for i in urls:
#     print(i)

urls





