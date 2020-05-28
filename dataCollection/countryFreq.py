import pycountry
import requests
import json
import pprint

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['QUERY'] = 'seafood "COVID-19"'
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'

# Gets maximum allowed number of articles per request
payload['MAXRECORDS'] = '250'

# Will just check the month of November 2019
# date format YYYYMMDDHHMMSS
dateStart = '20191101000000'
dateEnd = '20191130235959'

# Will only search through articles posted through dateStart-dateEnd
payload['STARTDATETIME'] = dateStart
payload['ENDDATETIME'] = dateEnd

# Gets a list of all countries in the world
countriesList = list(pycountry.countries)

# EXAMPLE: will only get articles from Spain
payload['SourceCountry'] = 'Spain'

# testing GDELT DOC API request for 2019 - 2020
resp = requests.get(gdeltAPI, params=payload)
print(f'response code: {resp.status_code}')
results = resp.json()
print(results.keys())