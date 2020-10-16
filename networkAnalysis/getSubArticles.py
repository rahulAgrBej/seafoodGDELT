import os
import urllib.parse
import requests
import json

ARTICLE_SEARCH_API = "https://article-search-api.herokuapp.com/api/getFullInfo"

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

f = open("sub250.txt", "r")
fileNames = f.readlines()
f.close()

reqLimit = 15
batch = []

startDate = "01/01/2017"
startTime = "00:00:00"
endDate = "01/01/2018"
endTime = "00:00:00"

folderOut = 'fullArticleInfo/'

for fName in fileNames:
    countryCode1 = fName[:2]
    countryCode2 = fName[2:4]
    sourceCountryCode = fName[4:6]

    query = "(" + countryRef[countryCode1][0] + " OR " + countryRef[countryCode1][1] + ") (" + countryRef[countryCode2][0] + " OR " + countryRef[countryCode2][1] + ") salmon (import OR imports OR export OR exports OR trade)"


    sendReq = [query, {"id": sourceCountryCode}, startDate, startTime, endDate, endTime]
    batch.append(sendReq)

    if len(batch) == reqLimit:
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

                csvContent = 'country1,country2,sourceCountry,year,month,day,domain,title,url,social_image,language\n'
                
                if 'articles' in res:
                    for articleHit in res['articles']:
                        csvContent = csvContent + \
                                        firstCountryCode + ',' + \
                                        secondCountryCode + ',' + \
                                        sourceCountryCode + ',' + \
                                        articleHit['seendate'][:4] + ',' + \
                                        str(int(articleHit['seendate'][4:6])) + ',' + \
                                        str(int(articleHit['seendate'][6:8])) + ',' + \
                                        articleHit['domain'] + ',' + \
                                        articleHit['title'] + ',' + \
                                        articleHit['url'] + ',' + \
                                        articleHit['socialimage'] + ',' +\
                                        articleHit['language'] + '\n'

                    fOutName = firstCountryCode + '_' + secondCountryCode + '_' + sourceCountryCode + '.csv'
                    fullOutPath = os.path.join(folderOut, fOutName)
                    fOut = open(fullOutPath, 'w')
                    fOut.write(csvContent)
                    fOut.close()
                else:
                    print(res)

            batch = []

