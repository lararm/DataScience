from googleapiclient.discovery import build
import pandas as pd
import pprint
import json

my_api_key = 'AIzaSyBjvKK9stqm7DfV8r_yhD9RzKFxhv-eyFI'
my_cse_id = '016347176537644924962:kmktmzlzila'
my_search_term = 'Data Science Jobs Toronto'


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build('customsearch', 'v1', developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search(

    my_search_term, my_api_key, my_cse_id, num=10)

urls = []
# Getting only the attribute list and inserting into the attr list.
for i in range(0,len(results[2]['pagemap']['listitem'])):
    # print(results['features'][i]['attributes'])
    urls.append(results[2]['pagemap']['listitem'][i]['url'])

for i in urls:
    print(i)






