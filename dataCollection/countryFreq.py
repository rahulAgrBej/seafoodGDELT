import pycountry
import requests
import json
import pprint
import matplotlib.pyplot as plt
from changeDateParams import incrementMonth, incrementYear

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['QUERY'] = 'seafood "COVID-19" sourcecountry:GH'
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'

# Gets maximum allowed number of articles per request
payload['MAXRECORDS'] = '250'

# Will just check the month of November 2019
# date format YYYYMMDDHHMMSS
dateStart = '20200101000000'
dateEnd = incrementMonth(dateStart, 1)

# Will only search through articles posted through dateStart-dateEnd
payload['STARTDATETIME'] = dateStart
payload['ENDDATETIME'] = dateEnd

# Gets a list of all countries in the world
countriesList = list(pycountry.countries)

countryFreq = {}
countryFreq['Ghana'] = []
# make GDELT request for articles for spain mentioning seafood AND "COVID-19" during NOV 2019
for i in range(5):
    
    resp = requests.get(gdeltAPI, params=payload)
    print(f'response code: {resp.status_code}')
    results = resp.json()
    
    if len(results.keys()) != 0:
        countryFreq['Ghana'].append(len(results['articles']))
    else:
        countryFreq['Ghana'].append(0)
    
    print(countryFreq['Ghana'])
    
    payload['STARTDATETIME'] = payload['ENDDATETIME']
    payload['ENDDATETIME'] = incrementMonth(payload['ENDDATETIME'], 1)

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(results)

plt.scatter([1, 2, 3, 4, 5], countryFreq['Ghana'])
plt.plot([1, 2, 3, 4, 5], countryFreq['Ghana'])
plt.show()