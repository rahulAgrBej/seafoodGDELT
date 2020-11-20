import os
import json
import requests

def makeReq(query, date):
    
    sourceCountry = query[-2:]
    newQuery = query[-17:]
    
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    mins = date[10:12]
    sec = date[12:]

    newDate = f'{month}/{day}/{year}'
    startTime = '00:00:00'
    endTime = '23:59:59'

    req = [newQuery, {'id': sourceCountry}, newDate, startTime, newDate, endTime]

    return req

tmpDataFolder = 'tmpDataStorage/'
dataFileNames = os.listdir(tmpDataFolder)

completeFreqData = []

for fName in dataFileNames:
    fPath = os.path.join(tmpDataFolder,fName)
    f = open(fPath, 'r')
    currData = json.loads(f.read())
    f.close()

    completeFreqData.extend(currData)

reqs = []
count = 0

for entry in completeFreqData:

    # check if empty
    if len(entry['timeline']) > 0:
        for date in entry['timeline'][0]['data']:
            # check if date has more than 250
            if date['value'] > 250:
                query = entry['query_details']['title']
                excessDate = date['date'][:8] + date['date'][9:-1]
                excessReq.append([query, excessDate])
            else:
                
                if (count + date['value']) >= 250:
                    # make request

                    pass
                else:
                    count += date['value']
