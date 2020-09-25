import requests
import json
import urllib.parse
from itertools import permutations

FREQ_API_URL = "https://article-search-api.herokuapp.com/api/searchTrends"

countries = [
    ["NO", "Norway", "Norwegian"],
    ["CI", "Chile", "Chilean"],
    ["RS", "Russia", "Russian"],
    ["CH", "China", "Chinese"],
    ["CA", "Canada", "Canadian"],
    ["SW", "Sweden", "Swedish"],
    ["JA", "Japan", "Japanese"],
    ["US", "United States", "American"]
    ]

countryCombos = permutations(countries, 2)

for combo in countryCombos:
    sourceCountry = combo[0]
    targetCountry = combo[1]

    query = "(" + targetCountry[1] + " OR " + targetCountry[2] + ")"
    query += " salmon (export OR exports OR import OR imports OR trade)"
    print(query)

"""
urllib.parse.urlencode(currStr)

query = "Japan salmon trade"

countries = []
countryUS = {}
countryUS["id"] = "US"
countries.append(countryUS)

payload = {}
payload['q'] = json.dumps(finalQuery)
payload['startDate'] = json.dumps("01/01/2020")
payload['startTime'] = json.dumps("00:00:00")
payload['endDate'] = json.dumps("09/01/2020")
payload['endTime'] = json.dumps("00:00:00")
payload['countries'] = json.dumps(countries)
"""