#import pycountry
import requests
import json
import pprint
import matplotlib.pyplot as plt
import threading
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

"""
monthNames = ['Jan', 'Feb', 'March', 'April', 'May']


countryScatters = []
for country in countryList:
    countryScatters.append(plt.plot(monthNames, countryFreq[country], label=country)) 

plt.legend()

plt.savefig('dataCollection/sample.png')
"""

COUNTRY_LIST_LOCK = threading.Lock()
COUNTRY_LIST_COUNTER = 0

COUNTRY_FREQ_LOCK = threading.Lock()
COUNTRY_FREQ = {}

PRINT_LOCK = threading.Lock()

def gdeltRequester():
    
    gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

    COUNTRY_LIST_LOCK.acquire()
    global COUNTRY_LIST_COUNTER
    countryIdx = COUNTRY_LIST_COUNTER
    COUNTRY_LIST_COUNTER += 1
    COUNTRY_LIST_LOCK.release()

    countryCode = COUNTRIES[countryIdx][0]
    countryName = COUNTRIES[countryIdx][1]

    COUNTRY_FREQ_LOCK.acquire()
    COUNTRY_FREQ[countryCode] = {}
    COUNTRY_FREQ[countryCode]['seafood&COVID-19'] = []
    COUNTRY_FREQ[countryCode]['seafood'] = []
    COUNTRY_FREQ_LOCK.release()

    payload = {}
    payload['MODE'] = 'ArtList'
    payload['FORMAT'] = 'JSON'

    # Gets maximum allowed number of articles per request
    payload['MAXRECORDS'] = '250'

    # Will just check the month of November 2019
    # date format YYYYMMDDHHMMSS
    dateStart = '20200401000000'
    dateEnd = incrementMonth(dateStart, 1)

    # Will only search through articles posted through dateStart-dateEnd
    payload['STARTDATETIME'] = dateStart
    payload['ENDDATETIME'] = dateEnd

    # for JAN 2020 - MAY 2020 (inclusive)
    for i in range(4):

        # runs search for query with seafood and COVID-19 in it for this particular country
        payload['QUERY'] = 'seafood "COVID-19" sourcecountry:' + countryCode
        numSeaCOVID = collectMonthNums(gdeltAPI, payload)
        
        # updates COUNTRY_FREQ dictionary with number of article hits
        COUNTRY_FREQ_LOCK.acquire()
        COUNTRY_FREQ[countryCode]['seafoodCOVID'].append(numSeaCOVID)
        COUNTRY_FREQ_LOCK.release()

        # runs search for query with seafood in it for this particular country
        payload['QUERY'] = 'seafood sourcecountry:' + countryCode
        numSea = collectMonthNums(gdeltAPI, payload)

        # updates COUNTRY_FREQ dictionary with number of article hits
        COUNTRY_FREQ_LOCK.acquire()
        COUNTRY_FREQ[countryCode]['seafood'].append(numSea)
        COUNTRY_FREQ_LOCK.release()

        dateStart = dateEnd
        dateEnd = incrementMonth(dateStart, 1)

    # writing results to file
    janHits = COUNTRY_FREQ[countryCode]["seafoodCOVID"][0]
    febHits = COUNTRY_FREQ[countryCode]["seafoodCOVID"][1]
    marchHits = COUNTRY_FREQ[countryCode]["seafoodCOVID"][2]
    aprilHits = COUNTRY_FREQ[countryCode]["seafoodCOVID"][3]
    mayHits = COUNTRY_FREQ[countryCode]["seafoodCOVID"][4]
    seaCOVIDHits = f'{janHits} {febHits} {marchHits} {aprilHits} {mayHits}'

    janHitSea = COUNTRY_FREQ[countryCode]["seafood"][0]
    febHitSea = COUNTRY_FREQ[countryCode]["seafood"][1]
    marchHitSea = COUNTRY_FREQ[countryCode]["seafood"][2]
    aprilHitSea = COUNTRY_FREQ[countryCode]["seafood"][3]
    mayHitSea = COUNTRY_FREQ[countryCode]["seafood"][4]
    seaHits = f'{janHitSea} {febHitSea} {marchHitSea} {aprilHitSea} {mayHitSea}'
    
    fileName = 'record' + countryCode
    recordFile = open('fileName', 'w')
    recordFile.write(countryName)
    recordFile.write('\n')
    recordFile.write('seafood AND COVID-19: ' + seaCOVIDHits)
    recordFile.write('\n')
    recordFile.write('seafood: ' +seaHits)
    recordFile.write('\n')
    recordFile.close()

    PRINT_LOCK.acquire()
    print(f'{countryName} DONE')
    PRINT_LOCK.release

    return None


