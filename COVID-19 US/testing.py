import requests
import urllib.parse
import json
import pprint



f = open("statesCountsExtendedQuery/Alaska Counts.txt", 'r')
dataCounts = json.loads(f.read())
f.close()

dataTotal = 0
for d in dataCounts:
    dataTotal += d["value"]

fCheck = open("statesFullArticles/Mississippi.txt", "r")
fullData = json.loads(fCheck.read())
fCheck.close()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(fullData)



"""

GDELT_URL = 'https://api.gdeltproject.org/api/v2/doc/doc'
TEST_URL = 'http://127.0.0.1:5000/api/getFullInfo'

MAX_ARTICLES = 250

payload = {}
payload['QUERY'] = "(seafood OR aquaculture OR aquacultures OR fishery OR fisheries) (coronavirus OR " + '\"Covid-19\") \"Alaska\"' + " sourcecountry:US"
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'
payload['MAXRECORDS'] = MAX_ARTICLES
payload['STARTDATETIME'] = "20200101000000"
payload['ENDDATETIME'] = "20200901000000"

query = "(seafood OR aquaculture OR aquacultures OR fishery OR fisheries) (coronavirus OR " + '\"Covid-19\") \"Alaska\"'
countryUS = {}
countryUS["id"] = "US"
startDate = "01/01/2020"
startTime = "00:00:00"
endDate = "09/01/2020"
endTime = "00:00:00"

sendReq = [[query, countryUS, startDate, startTime, endDate, endTime]]

parameters = {}
parameters["requestsSent"] = json.dumps(sendReq)


resp = requests.get(TEST_URL + "?" + urllib.parse.urlencode(parameters))

pp = pprint.PrettyPrinter(indent=2)
print(resp)
print(pp.pprint(resp.json()))
"""