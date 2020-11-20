import requests
import json
import time

GDELT_URL = 'https://api.gdeltproject.org/api/v2/doc/doc'
MAX_ARTICLES = 250


query1 = 'seafood sourcecountry:US'


# builds payload for GDELT request
payload1 = {}
payload1['QUERY'] = query1
payload1['MODE'] = 'TimelineVolRaw'
payload1['FORMAT'] = 'JSON'
payload1['MAXRECORDS'] = MAX_ARTICLES
payload1['STARTDATETIME'] = '20170101000000'
payload1['ENDDATETIME'] = '20170102000000'

resp1 = requests.get(GDELT_URL, params=payload1)
print(resp1.text)
data1 = resp1.json()['timeline'][0]['data']

count = 0
for d in data1:
    count += d['value']

print(count)