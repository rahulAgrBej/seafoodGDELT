import os
import json
import requests
import urllib.parse

def getDateStr(inDate):
    
    newDateStr = ""
    year = inDate[0:4]
    month = inDate[4:6]
    day = inDate[6:8]
    newDateStr = month + "/" + day + "/" + year
    return newDateStr

def getTimeframes(state, filePath):

    API_URL = "https://article-search-api.herokuapp.com/api/searchTrends?"

    f = open(filePath, 'r')
    stateCountDataStr = f.read()
    f.close()

    timeFrames = []

    if (len(stateCountDataStr) > 0):

        stateCountData = json.loads(stateCountDataStr)
        stateTimeData = stateCountData["results"][0]["timeline"][0]["data"]

        countLimit = 250
        startDate = stateTimeData[0]["date"]
        endDate = stateTimeData[0]["date"]
        
        count = 0

        for tf in stateTimeData:

            # if there are more articles on a particular day than limit
            if tf["value"] > countLimit:

                # save the dates you have collected up to this point as a timeframe
                # and reset all values again
                newEndDate = endDate[0:9] + "235959Z"
                endDate = newEndDate
                timeFrames.append([state, startDate, endDate])
                startDate = tf["date"]
                endDate = tf["date"]
                count = 0

                # make another time request for the day in order to determine new minimum
                countries = []
                countryUS = {}
                countryUS["id"] = "US"
                countries.append(countryUS)

                query = stateCountData["results"][0]["query_details"]["title"]

                payload = {}
                payload['q'] = json.dumps(query)
                payload['startDate'] = json.dumps(getDateStr(startDate))
                payload['startTime'] = json.dumps("00:00:00")
                payload['endDate'] = json.dumps(getDateStr(tf["date"]))
                payload['endTime'] = json.dumps("23:59:59")
                payload['countries'] = json.dumps(countries)

                finalURL = API_URL + urllib.parse.urlencode(payload)

                resp = requests.get(finalURL)
                print(resp)
                if resp.status_code == 200:
                    excessData = resp.json()
                    excessDates = excessData["results"][0]["timeline"][0]["data"]

                    for ed in excessDates:

                        if (count + ed["value"] > countLimit):
                            timeFrames.append([state, startDate, endDate])
                            startDate = ed["date"]
                            count = ed["value"]
                        else:
                            count += ed["value"]
                        
                        endDate = ed["date"]

            else:

                # check to see if result limit would be exceeded
                if ((count + tf["value"]) > countLimit):
                    newEndDate = endDate[0:9] + "235959Z"
                    endDate = newEndDate
                    timeFrames.append([state, startDate, endDate])
                    startDate = tf["date"]
                    count = tf["value"]
                else:
                    count += tf["value"]
                
                endDate = tf["date"]
        
        # append last time frame incase it already hasn't been appended
        if len(timeFrames) > 0:
            lastStart = timeFrames[-1][0]
            lastEnd = timeFrames[-1][1]

            if not ((startDate == lastStart) and (endDate == lastEnd)):
                timeFrames.append([state, startDate, endDate])
        else:
            timeFrames.append([state, startDate, endDate])

    return timeFrames

stateInfoPath = "statesInfo/"
stateCountFiles = os.listdir(stateInfoPath)

reqs = []
reqTotal = 0

for stateFile in stateCountFiles:
    print(stateFile)
    stateFileName = stateInfoPath + stateFile
    fileName = stateFile.split(" ")
    state = ""

    for i in range(len(fileName) - 1):
        state += fileName[i]
        if (i < (len(fileName) - 2)):
            state += " "


    reqs.extend(getTimeframes(state, stateFileName))

print(reqs)
print(len(reqs))

f = open("stateReqs.txt", "w")
f.write(json.dumps(reqs))
f.close()
