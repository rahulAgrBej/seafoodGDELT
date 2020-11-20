import os
import json
import requests

GDELT_REQ_LIMIT = 250

def getDateTime(date):

    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    mins = date[10:12]
    sec = date[12:]

    newDate = f'{month}/{day}/{year}'
    newTime = f'{hour}:{mins}:{sec}'

    return newDate, newTime

def getCurrDate(date):
    return date['date'][:8] + date['date'][9:-1]


def makeReq(query, startDate, endDate):
    
    sourceCountry = query[-2:]
    newQuery = query[-17:]
    
    startDate, startTime = getDateTime(startDate)
    endDate, endTime = getDateTime(endDate)

    req = [newQuery, {'id': sourceCountry}, startDate, startTime, endDate, endTime]

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
startDate = ''
prevDate = ''

for entry in completeFreqData:

    # check if empty
    if len(entry['timeline']) > 0:

        query = entry['query_details']['title']

        for date in entry['timeline'][0]['data']:

            if startDate == '':
                startDate = getCurrDate(date)
            
            # check if date has more than 250
            if date['value'] > GDELT_REQ_LIMIT:
                endDate = prevDate
                reqs.append(makeReq(query, startDate, endDate))


                startDate = getCurrDate(date)
                endDate = getCurrDate[-4:] + '235959'
                reqs.append(makeReq(query, startDate, endDate))
                count = 0
            else:
                
                if (count + date['value']) == GDELT_REQ_LIMIT:
                    # make request
                    endDate = getCurrDate(date)
                    reqs.append(makeReq(query, startDate, endDate))
                    count = 0
                    
                    # restart startDate
                    startDate = ''

                elif (count + date['value']) > GDELT_REQ_LIMIT:
                    # make new request
                    endDate = prevDate[:-4] + '235959'
                    count = 0
                    reqs.append(makeReq(query, startDate, endDate))

                    # set new startDate
                    startDate = getCurrDate(date)

                else:
                    count += date['value']
            
            prevDate = getCurrDate(date)
        
        if count > 0:
            # do the last req
            endDate = getCurrDate(entry['timeline'][0]['data'][-1]['date'])
            reqs.append(makeReq(query, startDate, endDate))
            count = 0


API_REQ_LIMIT = 15

# request API requesters

# write to CSV