import json
import requests
import urllib.parse
from itertools import permutations, combinations

FREQ_API_URL = 'https://article-search-api.herokuapp.com/api/searchTrends'

MAIN_IDS = [
    {'id': 'US'},
    {'id': 'CH'},
    {'id': 'CA'}
    ]

MAIN_COUNTRIES = ['US', 'CH', 'CA']

# reads in all source countries into a dictionary with country id : country name
def readCountries():

    sourceCountries = {}

    f = open('countryLookUp.txt', 'r')
    data = f.readlines()
    f.close()

    for country in data:
        country = country.rstrip('\n')
        country = country.split('\t')
        sourceCountries[country[0]] = ' '.join(country[1:])

    return sourceCountries

# returns all possible combos of sourceCountries
def allCombos():
    combos = []

    sourceCountries = readCountries()
    ids = sourceCountries.keys()
    combos = combinations(ids, 2)

    return combos

def getArticleCounts(inQuery, startDate, startTime, endDate, endTime):

    combos = allCombos()
    
    for combo in combos:
        query = f'{combo[0][1]} {combo[1][1]} ' + inQuery
        payload = {}

        reportingCountries = []
        reportingCountries.extend(MAIN_IDS)

        if not (combo[0][0] in MAIN_COUNTRIES):
            reportingCountries.append({'id': combo[0][0]})
        
        if not (combo[1][0] in MAIN_COUNTRIES):
            reportingCountries.append({'id': combo[1][0]})
        
        payload['countries'] = json.dumps(reportingCountries)
        payload['q'] = json.dumps(query)
        payload['startDate'] = json.dumps(startDate)
        payload['startTime'] = json.dumps(startTime)
        payload['endDate'] = json.dumps(endDate)
        payload['endTime'] = json.dumps(endTime)

        encodedPayload = urllib.parse.urlencode(payload)
        finalURL = FREQ_API_URL + "?" + encodedPayload

        resp = requests.get(finalURL)
        data = resp.json()["results"]

    return data