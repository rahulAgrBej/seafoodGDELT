# Gets count data for all 50 states for the query seafood AND (coronavirus OR covid-19)

import requests
import json
import urllib.parse
import time

def urlPrep(currStr):
    return urllib.parse.urlencode(currStr)

API_URL = "https://article-search-api.herokuapp.com/api/searchTrends"

stateNames = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
payload = {}
queryStr = 'seafood ("COVID-19" OR coronavirus) '

followUp = []
for state in stateNames:
    finalQuery = queryStr + '\"' + state + '\"'
    countries = []
    countryUS = {}
    countryUS["id"] = "US"
    countries.append(countryUS)

    payload = {}
    payload['q'] = json.dumps(finalQuery)
    payload['startDate'] = json.dumps("01/01/2020")
    payload['startTime'] = json.dumps("00:00:00")
    payload['endDate'] = json.dumps("08/01/2020")
    payload['endTime'] = json.dumps("00:00:00")
    payload['countries'] = json.dumps(countries)

    resp = requests.get(API_URL + "?" + urlPrep(payload))

    print(state)
    print(resp)

    if (resp.status_code == 200):
        f = open("statesInfo/" + state + " Counts.txt", 'w')
        f.write(json.dumps(resp.json()))
        f.close()
    else:
        followUp.append(state)
    
    #time.sleep(5)
print("followup")
print(followUp)
