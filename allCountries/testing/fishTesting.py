import requests
import json
import time

GDELT_URL = 'https://api.gdeltproject.org/api/v2/doc/doc'
MAX_ARTICLES = 250

query1 = 'United States fish sourcecountry:US'
query2 = 'United States (fish OR catfish) sourcecountry:US'

# builds payload for GDELT request
payload1 = {}
payload1['QUERY'] = query1
payload1['MODE'] = 'TimelineVolRaw'
payload1['FORMAT'] = 'JSON'
payload1['MAXRECORDS'] = MAX_ARTICLES
payload1['STARTDATETIME'] = '20170101000000'
payload1['ENDDATETIME'] = '20180101000000'

resp1 = requests.get(GDELT_URL, params=payload1)
data1 = resp1.json()

results1 = data1['timeline'][0]['data']
sum1 = 0


for result in results1:
    sum1 += result['value']

# to satisfy GDELT requirements
time.sleep(5)

payload2 = {}
payload2['QUERY'] = query2
payload2['MODE'] = 'TimelineVolRaw'
payload2['FORMAT'] = 'JSON'
payload2['MAXRECORDS'] = MAX_ARTICLES
payload2['STARTDATETIME'] = '20170101000000'
payload2['ENDDATETIME'] = '20180101000000'

resp2 = requests.get(GDELT_URL, params=payload2)
data2 = resp2.json()
results2 = data2['timeline'][0]['data']
sum2 = 0

for res in results2:
    sum2 += res['value']

print(f'Query w/ just FISH: {sum1}')
print(f'Query w/ FISH or CATFISH {sum2}')

if sum1 == sum2:
    print('results ARE the same')
else:
    print('results are NOT the same')