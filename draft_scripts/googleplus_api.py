from __future__ import print_function
import apiclient.discovery
from apiclient import discovery

TMPL = '''
    User: %s
    Date: %s
    Post: %s
'''

API_KEY = 'AIzaSyBjvKK9stqm7DfV8r_yhD9RzKFxhv-eyFI'

GPLUS = discovery.build('plus', 'v1', developerKey=API_KEY)

items = GPLUS.activities().search(query='python').execute().get('items', [])
for data in items:
    post = ' '.join(data['title'].strip().split())
    if post:
        print(TMPL % (data['actor']['displayName'],
                      data['published'], post))
