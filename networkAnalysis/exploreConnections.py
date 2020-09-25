import requests
import json
import urllib.parse
from itertools import permutations

FREQ_API_URL = "https://article-search-api.herokuapp.com/api/searchTrends"

countries = [
    {"id": "NO", "name": "Norway", "descriptor": "Norwegian"},
    {"id": "CI", "name": "Chile", "descriptor": "Chilean"},
    {"id": "RS", "name": "Russia", "descriptor": "Russian"},
    {"id": "CH", "name": "China", "descriptor": "Chinese"},
    {"id": "CA", "name": "Canada", "descriptor": "Canadian"},
    {"id": "SW", "name": "Sweden", "descriptor": "Swedish"},
    {"id": "JA", "name": "Japan", "descriptor": "Japanese"},
    {"id": "US", "name": "United States", "descriptor": "American"}
    ]

for idx in range(len(countries)):

    targetCountry = countries[idx]
    sourceCountries = []
    
    if ((idx > 0) and (idx < (len(countries) - 1))):
        sourceCountries = countries[0:idx]
        sourceCountries.extend(countries[(idx + 1):])
    elif idx == 0:
        sourceCountries = countries[1:]
    else:
        sourceCountries = countries[:-1]

    print(sourceCountries)
    print()

    query = "(" + targetCountry["name"] + " OR " + targetCountry["descriptor"] + ")  salmon (import OR imports OR export OR exports OR trade)"
    
    payload = {}
    payload["countries"] = json.dumps(sourceCountries)
    payload['q'] = json.dumps(query)
    payload['startDate'] = json.dumps("01/01/2017")
    payload['startTime'] = json.dumps("00:00:00")
    payload['endDate'] = json.dumps("01/01/2018")
    payload['endTime'] = json.dumps("00:00:00")

    print(payload)

    encodedPayload = urllib.parse.urlencode(payload)
    finalURL = FREQ_API_URL + "?" + encodedPayload
    resp = requests.get(finalURL)
    print(resp.status_code)
    data = resp.json()["results"]
    print(len(data))
    for source in data:
        fName = targetCountry["name"] + " salmon trade source:" + source["query_details"]["title"][-2:]
        fPath = "freqResults/" + fName
        f = open(fPath, "w")
        f.write(json.dumps(source["timeline"][0]["data"]))
        f.close()
