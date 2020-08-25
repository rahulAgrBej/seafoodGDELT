# script that will get the Full article data for all 50 US states
import requests
import json
import urllib.parse

def getDateTime(inDate):
    
    newDateStr = ""
    year = inDate[0:4]
    month = inDate[4:6]
    day = inDate[6:8]
    newDateStr = month + "/" + day + "/" + year


    newTimeStr = ""
    hour = inDate[10:12]
    minute = inDate[12:14]
    seconds = inDate[14:16]
    newTimeStr = hour + ":" + minute + ":" + seconds
    return newDateStr, newTimeStr


ARTICLE_SEARCH_API = "https://article-search-api.herokuapp.com/api/getFullInfo"

# get timeframes for each state
f = open("stateReqs.txt", "r")
dataStr = f.read()
f.close()
stateTimeframes = json.loads(dataStr)

reqLimit = 15

reqCounter = 0
countries = []
batch = []
articles = []
reqTotal = 0
for req in stateTimeframes:
    reqCounter += 1
    query = 'seafood (coronavirus OR ' + '\"' + "COVID-19" + '\") ' +  '\"' + req[0] + '\"'
    countryUS = {}
    countryUS["id"] = "US"
    startDate, startTime = getDateTime(req[1])
    endDate, endTime = getDateTime(req[2])

    sendReq = [query, country, startDate, startTime, endDate, endTime]
    batch.append(sendReq)

    if (reqCounter == reqLimit):
        payload = {}
        payload["requestsSent"] = json.dumps(batch)
        resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
        print(resp)
        if resp.status_code == 200:
            articles.extend(resp.json()["results"][0]["articles"])

        reqTotal += reqCounter
        print(str(reqTotal) "out of " str(len(stateTimeframes)))

        batch = []
        reqCounter = 0

if len(batch) > 0:
    payload = {}
    payload["requestsSent"] = json.dumps(batch)
    resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
    print(resp)
    if resp.status_code == 200:
        articles.extend(resp.json()["results"][0]["articles"])

    reqTotal += len(batch)
    print(str(reqTotal) "out of " str(len(stateTimeframes)))

print("writing results to file")
fResults = open("fullArticleData.txt", 'w')
fResults.write(json.dumps(articles))
fResults.close()
print("DONE!!!!!!!!!!")
