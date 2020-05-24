import requests
import json
import pprint

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['QUERY'] = 'seafood "COVID-19" thai'
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'

# testing GDELT DOC API request for November 2019
resp = requests.get(gdeltAPI, params=payload)
results = resp.json()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(results)
