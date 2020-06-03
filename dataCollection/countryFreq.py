#import pycountry
import requests
import json
import pprint
import matplotlib.pyplot as plt
from changeDateParams import getMonth, incrementMin, incrementHour, incrementDay, incrementMonth, incrementYear

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

COUNTRIES = []

# reads in all GDELT supported Countries
countryFile = open('supportedCountries.txt', 'r')
numCountries = int(countryFile.readline().rstrip('\n'))
for cCount in range(numCountries):
    line = countryFile.readline().rstrip('\n')
    countryData = line.split('\t')
    COUNTRIES.append(countryData)
countryFile.close()

def collectMinutelyNums(inURL, inPayload):
    minuteCount = 0

    startMin = inPayload['STARTDATETIME']
    for i in range(59):
        endMin = incrementMin(startMin, 1)
        inPayload['ENDDATETIME'] = endMin
        minuteResp = requests.get(inURL, inPayload)
        minuteResults = minuteResp.json()
        if (len(minuteResults.keys()) != 0):
            minuteArticles = len(minuteResults['articles'])
            print(f'minute {i}: {minuteArticles}')
            minuteCount += minuteArticles
        
        startMin = endMin
        inPayload['STARTDATETIME'] = startMin
    
    return minuteCount

def collectHourlyNums(inURL, inPayload):

    hourCount = 0

    startHour = inPayload['STARTDATETIME']
    for i in range(23):
        endHour = incrementHour(startHour, 1)
        inPayload['ENDDATETIME'] = endHour
        hourlyResp = requests.get(inURL, inPayload)
        hourResults = hourlyResp.json()
        if (len(hourResults.keys()) != 0):
            hourArticles = len(hourResults['articles'])
            if hourArticles >= MAX_ARTICLES:
                minuteArticles = collectMinutelyNums(inURL, inPayload)
                hourArticles = minuteArticles
            print(f'hour {i}: {hourArticles}')
            hourCount += hourArticles

        startHour = endHour
        inPayload['STARTDATETIME'] = startHour
    
    return hourCount

def collectDailyNums(inURL, inPayload):

    dailyCount = 0
    
    startDay = inPayload['STARTDATETIME']
    month = int(getMonth(startDay))
    for i in range (MONTH_END[month]):
        endDay = incrementDay(startDay, 1)
        inPayload['ENDDATETIME'] = endDay
        dailyResp = requests.get(inURL, inPayload)
        dailyResults = dailyResp.json()

        if (len(dailyResults.keys()) != 0):
            dailyArticles = len(dailyResults['articles'])
            if dailyArticles >= MAX_ARTICLES:
                hourArticles = collectHourlyNums(inURL, inPayload)
                dailyArticles = hourArticles
            print(f'day {i}: {dailyArticles}')
            dailyCount += dailyArticles
        
        startDay = endDay
        inPayload['STARTDATETIME'] = startDay
    

    return dailyCount

def collectMonthNums(inURL, inPayload):

    monthlyCount = 0

    monthlyResp = requests.get(gdeltAPI, params=inPayload)
    monthlyResults = monthlyResp.json()
    if len(monthlyResults.keys()) != 0:
        monthlyArticles = len(monthlyResults['articles'])
        if monthlyArticles >= MAX_ARTICLES:
            dailyArticles = collectDailyNums(inURL, inPayload)
            monthlyArticles = dailyArticles
        print(f'month : {monthlyArticles}')
        monthlyCount += monthlyArticles

    return monthlyCount
        

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

payload = {}
payload['MODE'] = 'ArtList'
payload['FORMAT'] = 'JSON'

# Gets maximum allowed number of articles per request
payload['MAXRECORDS'] = '250'

# Will just check the month of November 2019
# date format YYYYMMDDHHMMSS
dateStart = '20200301000000'
dateEnd = incrementMonth(dateStart, 1)

# Will only search through articles posted through dateStart-dateEnd
payload['STARTDATETIME'] = dateStart
payload['ENDDATETIME'] = dateEnd

# Gets a list of all countries in the world
#countriesList = list(pycountry.countries)
#countryList = ['GH', 'TH', 'NO', 'VM', 'CI']

countryFreq = {}
"""
for country in countryList:
    countryFreq[country] = []
"""
payload['QUERY'] = 'seafood "COVID-19" sourcecountry:US'
numUSA = collectMonthNums(gdeltAPI, payload)
print(numUSA)
"""
# make GDELT requests for each country in our list of countries from Jan 2020 - May 2020
for i in range(5):
    
    for countryIdx in range(len(COUNTRIES))[:5]:
        
        countryCode = COUNTRIES[countryIdx][0]
        countryName = COUNTRIES[countryIdx][1]
        payload['QUERY'] = 'seafood "COVID-19" sourcecountry:' + countryCode
        numSeaCOVID = collectMonthNums(gdeltAPI, payload)

        # if its the first time we are getting data for this country
        if not (countryName in countryFreq.keys()):
            countryFreq[countryName] = {}
            countryFreq[countryName]['seafood&COVID-19'] = []
            countryFreq[countryName]['seafood'] = []
            countryFreq[countryName]['percent'] = []
            
        
        countryFreq[countryName]['seafood&COVID-19'].append(numSeaCOVID)
        
        payload['QUERY'] = 'seafood sourcecountry:' + countryCode
        numSea = collectMonthNums(gdeltAPI, payload)
        
        countryFreq[countryName]['seafood'].append(numSea)

        countryFreq[countryName][percent] = (numSeaCOVID / numSea) * 100
    
    payload['STARTDATETIME'] = payload['ENDDATETIME']
    payload['ENDDATETIME'] = incrementMonth(payload['ENDDATETIME'], 1)
    print(countryFreq)
    print()
"""
"""
monthNames = ['Jan', 'Feb', 'March', 'April', 'May']


countryScatters = []
for country in countryList:
    countryScatters.append(plt.plot(monthNames, countryFreq[country], label=country)) 

plt.legend()

plt.savefig('dataCollection/sample.png')
"""