import json
import requests
import urllib.parse
import os

def getQuery(fileName):

    country1 = fileName[:2]
    country2 = fileName[2:4]
    sourceCountry = fileName[4:6]

    query = "(" + code2name[country1] + " OR " + code2descriptor[country1] + ") (" + code2name[country2] + " OR " + code2descriptor[country2] + ") salmon (import OR imports OR export OR exports OR trade)"
    return query, {'id': sourceCountry}

def getDateTime(inDate):
    
    newDateStr = ""
    year = inDate[0:4]
    month = inDate[4:6]
    day = inDate[6:8]
    newDateStr = month + "/" + day + "/" + year


    newTimeStr = ""
    hour = inDate[9:11]
    minute = inDate[11:13]
    seconds = inDate[13:15]
    newTimeStr = hour + ":" + minute + ":" + seconds
    return newDateStr, newTimeStr

code2name = {
    'US': '\"United States\"',
    'NO': 'Norway',
    'CI': 'Chile',
    'RS': 'Russia',
    'CH': 'China',
    'CA': 'Canada',
    'SW': 'Sweden',
    'JA': 'Japan'
}

code2descriptor = {
    'US': 'American',
    'NO': 'Norwegian',
    'CI': 'Chilean',
    'RS': 'Russian',
    'CH': 'Chinese',
    'CA': 'Canadian',
    'SW': 'Swedish',
    'JA': 'Japanese'
}


ARTICLE_SEARCH_API = "https://article-search-api.herokuapp.com/api/getFullInfo"
#ARTICLE_SEARCH_API = "http://127.0.0.1:5000/api/getFullInfo"

query = "(Canada OR Canadian) (China OR Chinese) salmon (import OR imports OR export OR exports OR trade)"

startDate = "01/01/2017"
startTime = "00:00:00"
endDate = "01/01/2018"
endTime = "00:00:00"
batch = []
sendReq = [query, {"id": "CH"}, startDate, startTime, endDate, endTime]
batch.append(sendReq)

payload = {}
payload["requestsSent"] = json.dumps(batch)
resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
print(resp)
print(resp.json())
"""

FREQ_API_URL = "https://article-search-api.herokuapp.com/api/searchTrends"


payload = {}
payload["countries"] = json.dumps([{"id":"US"}])
payload['q'] = json.dumps(query)
payload['startDate'] = json.dumps("10/05/2017")
payload['startTime'] = json.dumps("23:00:00")
payload['endDate'] = json.dumps("10/05/2017")
payload['endTime'] = json.dumps("23:59:59")

print(payload)

encodedPayload = urllib.parse.urlencode(payload)
finalURL = FREQ_API_URL + "?" + encodedPayload
resp = requests.get(finalURL)
print(resp.status_code)
data = resp.json()['results'][0]['timeline'][0]['data']
total = 0
for r in data:
    total += r['value']
    if r['value'] > 250:
        print("hey")
        print(r['value'])
        print(r['date'])
    print(r['value'])

print("total results:")
print(total)


overPath = 'over250.txt'
overF = open(overPath, 'r')
overFiles = overF.readlines()
overF.close()



print(payload)

encodedPayload = urllib.parse.urlencode(payload)
finalURL = FREQ_API_URL + "?" + encodedPayload


overPath = 'over250.txt'
overF = open(overPath, 'r')
overFiles = overF.readlines()
overF.close()

for fName in overFiles:
    fName = fName.rstrip('\n')
    f = open(os.path.join('stage0/', fName), 'r')
    data = json.loads(f.read())
    for d in data:
        if d['value'] > 250:
            print("print day value exceeded")
            testQuery, sourceC = getQuery(fName)
            sDate, sTime = getDateTime(d['date'])
            payload = {}
            payload["countries"] = json.dumps([sourceC])
            payload['q'] = json.dumps(testQuery)
            payload['startDate'] = json.dumps(sDate)
            payload['startTime'] = json.dumps("00:00:00")
            payload['endDate'] = json.dumps(sDate)
            payload['endTime'] = json.dumps("23:59:59")
            encodedPayload = urllib.parse.urlencode(payload)
            finalURL = FREQ_API_URL + "?" + encodedPayload

            resp = requests.get(finalURL)
            print(resp.status_code)
            dataDay = resp.json()['results'][0]['timeline'][0]['data']
            for dD in dataDay:
                if dD['value'] > 250:
                    print("HOUR EXCEEDED")
"""
