import os
import json
import requests
import urllib.parse

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

countryRef = {
    "NO": ["Norway", "Norwegian"],
    "CI": ["Chile", "Chilean"],
    "RS": ["Russia", "Russian"],
    "CH": ["China", "Chinese"],
    "CA": ["Canada", "Canadian"],
    "SW": ["Sweden", "Swedish"],
    "JA": ["Japan", "Japanese"],
    "US": ["\"United States\"", "American"]
}

countryCodes = {
    "Norway": "NO",
    "Chile": "CI",
    "Russia": "RS",
    "China": "CH",
    "Canada": "CA",
    "Sweden": "SW",
    "Japan": "JA",
    "\"United": "US"
}

ARTICLE_SEARCH_API = "https://article-search-api.herokuapp.com/api/getFullInfo"


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

def getQuery(fileName):

    country1 = fileName[:2]
    country2 = fileName[2:4]
    sourceCountry = fileName[4:6]

    query = "(" + code2name[country1] + " OR " + code2descriptor[country1] + ") (" + code2name[country2] + " OR " + code2descriptor[country2] + ") salmon (import OR imports OR export OR exports OR trade)"
    return query, {'id': sourceCountry}

def createReq(overFile, inStartDate, inEndDate):
    outStartDate, outStartTime = getDateTime(inStartDate)
    outEndDate, outEndTime = getDateTime(inEndDate)
    if outStartDate == outEndDate:
        outEndTime = '23:59:59'
    query, sourceCountry = getQuery(overFile)
    sendReq = [query, sourceCountry, outStartDate, outStartTime, outEndDate, outEndTime]
    
    return sendReq

def hourlyReqs(overFile, inDate):

    dt, tm = getDateTime(inDate)
    query, sourceCountry = getQuery(overFile)
    hrReqs = []

    for i in range(24):

        if i == 23:
            st = str(i) + ':00:00'
            et = str(i) + ':59:59'
        elif i >= 10:
            st = str(i) + ':00:00'
            et = str(i + 1) + ':00:00'
        elif i == 9:
            st = '0' + str(i) + ':00:00'
            et = '10:00:00'
        else:
            st = '0' + str(i) + ':00:00'
            et = '0' + str(i + 1) + ':00:00'  
        
        sendReq = [query, sourceCountry, dt, st, dt, et]
        hrReqs.append(sendReq)
    
    return hrReqs
        

inFile = 'over250.txt'
f = open(inFile, 'r')
overFiles = f.readlines()
f.close()

resultLimit = 250
reqs = []

for overFile in overFiles:
    overFile = overFile.rstrip('\n')
    newF = open(os.path.join('stage0/', overFile), 'r')
    data = json.loads(newF.read())
    newF.close()

    total = 0

    inStartDate = data[0]['date']
    inEndDate = data[0]['date']

    reset = False
    
    for d in data:

        if reset:
            inStartDate = d['date']
            inEndDate = d['date']
            total = 0
            reset = False

        if d['value'] > 250:
            
            reqs.append(createReq(overFile, inStartDate, inEndDate))
            reqs.extend(hourlyReqs(overFile, d['date']))
            reset = True
        else:
            if (total + d['value']) > resultLimit:
                reqs.append(createReq(overFile, inStartDate, inEndDate))
                inStartDate = d['date']
                inEndDate = d['date']
                total = d['value']

            elif (total + d['value']) == resultLimit:
                inEndDate = d['date']
                reqs.append(createReq(overFile, inStartDate, inEndDate))
                reset = True
            else:
                total += d['value']
                inEndDate = d['date']


print("STARTING BATCHING")
print(len(reqs))
batch = []
csvContent = 'country1,country2,sourceCountry,year,month,day,domain,title,url,social_image,language\n'
for r in reqs:

    batch.append(r)

    if len(batch) == 15:
        payload = {}
        payload["requestsSent"] = json.dumps(batch)
        resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
        print(resp)

        if resp.status_code == 200:
            # get info and put into CSV format
            responseData = resp.json()['results']
            print(len(responseData))
            for res in responseData:
                inQuery = res['query_details']['title']
                sourceCountry = inQuery[-2:]
                spaceSplit = inQuery.split(' ')

                firstCountry = spaceSplit[0][1:]
                secondCountry = ''

                firstCountryCode = ''
                secondCountryCode = ''

                if firstCountry == '\"United':
                    secondCountry = spaceSplit[4][1:]
                else:
                    secondCountry = spaceSplit[3][1:]
                
                firstCountryCode = countryCodes[firstCountry]
                secondCountryCode = countryCodes[secondCountry]
                
                if 'articles' in res:
                    for articleHit in res['articles']:
                        articleHit['title'].replace(',', '', )
                        csvContent = csvContent + \
                                        firstCountryCode + ',' + \
                                        secondCountryCode + ',' + \
                                        sourceCountry + ',' + \
                                        articleHit['seendate'][:4] + ',' + \
                                        str(int(articleHit['seendate'][4:6])) + ',' + \
                                        str(int(articleHit['seendate'][6:8])) + ',' + \
                                        articleHit['domain'] + ',' + \
                                        articleHit['title'].replace(',', '') + ',' + \
                                        articleHit['url'] + ',' + \
                                        articleHit['socialimage'] + ',' +\
                                        articleHit['language'] + '\n'
        else:
            print(batch)
            print("ERROR HAPPENED")
            print(resp.content)
        batch = []

if len(batch) > 0:
    payload = {}
    payload["requestsSent"] = json.dumps(batch)
    resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
    print(resp)

    if resp.status_code == 200:
        # get info and put into CSV format
        responseData = resp.json()['results']
        print(len(responseData))
        for res in responseData:
            inQuery = res['query_details']['title']
            sourceCountry = inQuery[-2:]
            spaceSplit = inQuery.split(' ')

            firstCountry = spaceSplit[0][1:]
            secondCountry = ''

            firstCountryCode = ''
            secondCountryCode = ''

            if firstCountry == '\"United':
                secondCountry = spaceSplit[4][1:]
            else:
                secondCountry = spaceSplit[3][1:]
            
            firstCountryCode = countryCodes[firstCountry]
            secondCountryCode = countryCodes[secondCountry]
            
            if 'articles' in res:
                for articleHit in res['articles']:
                    articleHit['title'].replace(',', '', )
                    csvContent = csvContent + \
                                    firstCountryCode + ',' + \
                                    secondCountryCode + ',' + \
                                    sourceCountry + ',' + \
                                    articleHit['seendate'][:4] + ',' + \
                                    str(int(articleHit['seendate'][4:6])) + ',' + \
                                    str(int(articleHit['seendate'][6:8])) + ',' + \
                                    articleHit['domain'] + ',' + \
                                    articleHit['title'].replace(',', '') + ',' + \
                                    articleHit['url'] + ',' + \
                                    articleHit['socialimage'] + ',' +\
                                    articleHit['language'] + '\n'
    else:
        print(batch)
        print("ERROR HAPPENED")
        print(resp.content)
    

fOut = open('over250FullArticles.csv', 'w')
fOut.write(csvContent)
fOut.close()
print("DONE!!!")