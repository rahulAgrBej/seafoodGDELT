import requests
import json
import pprint

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['QUERY'] = 'seafood "COVID-19"'
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'
payload['STARTDATETIME'] = '20190101000000'
payload['ENDDATETIME'] = '20200601000000'
payload['MAXRECORDS'] = '250'

# testing GDELT DOC API request for 2019 - 2020
resp = requests.get(gdeltAPI, params=payload)
results = resp.json()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(results)
