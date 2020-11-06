# script that will get the Full article data for all 50 US states
import requests
import json
import urllib.parse
import os

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


ARTICLE_SEARCH_API = "https://article-search-api.herokuapp.com/api/getFullInfo"

folderName = "statesMinReqs/"
statesFilesNames = os.listdir(folderName)
for fName in statesFilesNames:
    print(fName)
    fPath = os.path.join(folderName, fName)
    f = open(fPath, "r")
    stringData = f.read()
    f.close()
    minStateReqs = json.loads(stringData)

    reqLimit = 15

    reqCounter = 0
    countries = []
    batch = []
    articles = []
    reqTotal = 0
    for req in minStateReqs:
        reqCounter += 1
        query = '(seafood OR fishery OR fisheries OR aquaculture) (coronavirus OR \"Covid-19\") ' +  '\"' + req[0] + '\"'
        countryUS = {}
        countryUS["id"] = "US"
        startDate, startTime = getDateTime(req[1])
        endDate, endTime = getDateTime(req[2])

        sendReq = [query, countryUS, startDate, startTime, endDate, endTime]
        print(sendReq)
        batch.append(sendReq)

        if (reqCounter == reqLimit):
            payload = {}
            payload["requestsSent"] = json.dumps(batch)
            resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
            print(resp)
            if resp.status_code == 200:
                responseResults = resp.json()["results"]
                for res in responseResults:
                    articles.extend(res["articles"])
            else:
                print("error occurred")
                

            reqTotal += reqCounter
            print(str(reqTotal) + "out of " + str(len(minStateReqs)))

            batch = []
            reqCounter = 0
    
    if len(batch) > 0:
        payload = {}
        payload["requestsSent"] = json.dumps(batch)
        resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
        print(resp)
    
        if resp.status_code == 200:
            responseResults = resp.json()["results"]
            for res in responseResults:
                articles.extend(res["articles"])

    reqTotal += len(batch)
    print(str(reqTotal) + "out of " + str(len(minStateReqs)))
    
    outFolder = "statesFullArticles/"
    stateName = fName[7:]
    outFile = os.path.join(outFolder, stateName)
    fOut = open(outFile, "w")
    fOut.write(json.dumps(articles))
    fOut.close()
    print(stateName + " DONE")

print("COMPLETELY DONE!!!")    
