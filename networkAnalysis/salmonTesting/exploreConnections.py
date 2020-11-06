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

mainCountries = [
    {"id": "US", "name": "United States"},
    {"id": "CA", "name": "Canada"},
    {"id": "CH", "name": "China"}
    ]

perms = permutations(countries, 2)

csvFileText = "country1,country2,sourceCountry,frequency,norm,year,month,day"

for entry in perms:
    sourceCountry = entry[0]
    targetCountry = entry[1]

    query = "(" + targetCountry["name"] + " OR " + targetCountry["descriptor"] + ") (" + sourceCountry["name"] + " OR " + sourceCountry["descriptor"] + ") salmon (import OR imports OR export OR exports OR trade)"
    
    payload = {}

    searchCountries = []
    addCountry = True
    for i in range(len(mainCountries)):
        if sourceCountry["id"] != mainCountries[i]["id"]:
            searchCountries.append(mainCountries[i])
        else:
            addCountry = False
    
    if addCountry:
        searchCountries.append(sourceCountry)
    
    payload["countries"] = json.dumps(searchCountries)
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
    #print(data)

    for source in data:
        if len(source["timeline"]) > 0:
            fName = targetCountry["id"] + sourceCountry["id"] + source["query_details"]["title"][-2:]+".txt"
            fPath = "stage0/" + fName
            f = open(fPath, "w")
            f.write(json.dumps(source["timeline"][0]["data"]))
            f.close()
    