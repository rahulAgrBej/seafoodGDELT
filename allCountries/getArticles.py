import os
import json
import requests
import pprint
import urllib.parse
import setup


ARTICLE_SEARCH_API = "https://article-search-api.herokuapp.com/api/getFullInfo"

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
    newQuery = query[:-17]
    
    startDate, startTime = getDateTime(startDate)
    endDate, endTime = getDateTime(endDate)

    req = [newQuery, {'id': sourceCountry}, startDate, startTime, endDate, endTime]

    return req

def sendBatch(batch):

    payload = {}
    payload['requestsSent'] = json.dumps(batch)
    resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))

    if resp.status_code == 200:
        print('STATUS CODE 200')
        responseData = resp.json()['results']
    else:
        responseData = []
        print(resp.text)
        print("ERROR OCCURED RESP")
    
    return responseData

COUNTRIES = setup.country2Id()

def findChar(text, character):
    indices = []

    for i in range(len(text)):
        if text[i] == character:
            indices.append(i)

    return indices

def processResponse(data):

    for result in data:
        query = result['query_details']['title']
        sourceCountryCode = query[-2:]
        
        # finds quotation marks
        indices = findChar(query, '\"')

        if len(indices) != 4:
            print("ERROR OCCURED FINDING QUOTATIONS")
        
        startQuote = indices[0] + 1
        endQuote = indices[1]
        country1 = query[startQuote:endQuote]
        
        startQuote = indices[2] + 1
        endQuote = indices[3]
        country2 = query[startQuote:endQuote]

        firstCountryCode = COUNTRIES[country1]
        secondCountryCode = COUNTRIES[country2]

        csvContent = ''

        if 'articles' in result:
            for articleHit in result['articles']:
                # replace all commas in titles
                articleHit['title'].replace(',', '', )
                csvContent = csvContent + \
                    firstCountryCode + ',' + \
                    secondCountryCode + ',' + \
                    sourceCountryCode + ',' + \
                    articleHit['seendate'][:4] + ',' + \
                    str(int(articleHit['seendate'][4:6])) + ',' + \
                    str(int(articleHit['seendate'][6:8])) + ',' + \
                    articleHit['domain'] + ',' + \
                    articleHit['title'].replace(',', '') + ',' + \
                    articleHit['url'] + ',' + \
                    articleHit['socialimage'] + ',' +\
                    articleHit['language'] + ',' +\
                    query[:-17] + '\n'
    
    return csvContent

tmpDataFolder = 'tmpDataStorage2017/'
dataFileNames = os.listdir(tmpDataFolder)[:1]

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
                endDate = getCurrDate(date)[:-6] + '235959'
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
                    endDate = prevDate[:-6] + '235959'
                    count = 0
                    reqs.append(makeReq(query, startDate, endDate))

                    # set new startDate
                    startDate = getCurrDate(date)

                else:
                    count += date['value']
            
            prevDate = getCurrDate(date)
        
        if count > 0:
            # do the last req
            endDate = getCurrDate(entry['timeline'][0]['data'][-1])
            reqs.append(makeReq(query, startDate, endDate))
            count = 0
        
        startDate = ''
        prevDate = ''
    
#printer = pprint.PrettyPrinter()
#print(len(reqs))
#printer.pprint(reqs)

API_REQ_LIMIT = 10

batch = []

csvContent = 'country1,country2,sourceCountry,year,month,day,domain,title,url,social_image,language,query\n'

for req in reqs:

    batch.append(req)

    if len(batch) == API_REQ_LIMIT:
        # send batch over to API
        responseData = sendBatch(batch)
        if len(responseData) > 0:
            csvContent += processResponse(responseData)
        batch = []


# edge case if there are any reqs left to be sent
if len(batch) > 0:
    # send batch
    leftoverResponseData = sendBatch(batch)
    if len(leftoverResponseData) > 0:
        csvContent += processResponse(leftoverResponseData)

f = open('articleResults/2017_part0.csv', 'w')
f.write(csvContent)
f.close()