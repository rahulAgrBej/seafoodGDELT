import pycountry
import requests
import json
import pprint
import matplotlib.pyplot as plt
from changeDateParams import incrementDay, incrementMonth, incrementYear

MAX_ARTICLES = 250
MONTH_END = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

def collectMonthNums(inURL, inPayload):

    resp = requests.get(gdeltAPI, params=inPayload)
    results = resp.json()

    numArticles = 0

    if len(results.keys()) != 0:
        
        # if we got the MAX number of article results
        if results['articles'] >= MAX_ARTICLES:
            
            # Do a more granular search (day by day search)
            startDay = inPayload['STARTDATETIME']
            for i in range (MONTH_END[month]):
                
                endDay = incrementDay(startDay, 1)
                inPayload['ENDDATETIME'] = endDay
                dailyResp = requests.get(inURL, inPayload)
                
                if (len(results.keys()) != 0):
                    print(results['articles'])
                    numArticles += results['articles']
                
                startDay = endDay

    return numArticles
        

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'

# Gets maximum allowed number of articles per request
payload['MAXRECORDS'] = '250'

# Will just check the month of November 2019
# date format YYYYMMDDHHMMSS
dateStart = '20200101000000'
dateEnd = incrementMonth(dateStart, 1)

# Will only search through articles posted through dateStart-dateEnd
payload['STARTDATETIME'] = dateStart
payload['ENDDATETIME'] = dateEnd

# Gets a list of all countries in the world
# countriesList = list(pycountry.countries)
countryList = ['GH', 'TH', 'NO', 'VM', 'CI']

countryFreq = {}
for country in countryList:
    countryFreq[country] = []

# make GDELT request for articles for spain mentioning seafood AND "COVID-19" during NOV 2019
for i in range(5):

    for country in countryList:
        payload['QUERY'] = 'seafood "COVID-19" sourcecountry:' + country
        resp = requests.get(gdeltAPI, params=payload)
        results = resp.json()
    
        if len(results.keys()) != 0:
            countryFreq[country].append(len(results['articles']))
        else:
            countryFreq[country].append(0)
    
    payload['STARTDATETIME'] = payload['ENDDATETIME']
    payload['ENDDATETIME'] = incrementMonth(payload['ENDDATETIME'], 1)


monthNames = ['Jan', 'Feb', 'March', 'April', 'May']

countryScatters = []
for country in countryList:
    countryScatters.append(plt.plot(monthNames, countryFreq[country], label=country)) 

plt.legend()

plt.savefig('dataCollection/sample.png')