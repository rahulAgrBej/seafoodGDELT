import os
import json

def getTimeframes(filePath):
    print(filePath)
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
            currCount = count + tf["value"]
            
            if (currCount > countLimit):
                timeFrames.append([startDate, endDate])
                startDate = tf["date"]
                endDate = tf["date"]
                count = tf["value"]
            else:
                count = currCount
                endDate = tf["date"]

    return timeFrames

stateInfoPath = "statesInfo/"
stateCountFiles = os.listdir(stateInfoPath)

reqs = {}
reqTotal = 0

for stateFile in stateCountFiles:
    stateFileName = stateInfoPath + stateFile
    fileName = stateFile.split(" ")
    state = ""

    for i in range(len(fileName) - 1):
        state += fileName[i]
        if (i < (len(fileName) - 2)):
            state += " "


    reqs[state] = getTimeframes(stateFileName)
    reqTotal += len(reqs[state])

print(reqs)
print(reqTotal)

f = open("stateReqs.txt", "w")
f.write(json.dumps(reqs))
f.close()
