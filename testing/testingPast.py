import requests
import json
import pprint

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['QUERY'] = 'seafood outbreak'
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'
payload['STARTDATETIME'] = '20170101000000'
payload['ENDDATETIME'] = '20180101000000'

# testing GDELT DOC API request for November 2019
resp = requests.get(gdeltAPI, params=payload)
results = resp.json()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(results)
