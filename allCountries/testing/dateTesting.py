import requests
import json
import time

def sumResults(data):
    count = 0
    for d in data:
        count += d['value']
    return count

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

count1 = sumResults(data1)

print(count1)

# to satisfy GDELT requirements
time.sleep(5)

payload2 = {}
payload2['QUERY'] = query1
payload2['MODE'] = 'TimelineVolRaw'
payload2['FORMAT'] = 'JSON'
payload2['MAXRECORDS'] = MAX_ARTICLES
payload2['STARTDATETIME'] = '20170101000000'
payload2['ENDDATETIME'] = '20170101235959'

resp2 = requests.get(GDELT_URL, params=payload2)
print(resp2.text)
data2 = resp2.json()['timeline'][0]['data']

count2 = sumResults(data2)
print(count2)