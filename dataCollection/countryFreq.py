#import pycountry
import requests
import json
import pprint
import matplotlib.pyplot as plt
import threading
from changeDateParams import getMonth, incrementMin, incrementHour, incrementDay, incrementMonth, incrementYear
import concurrent.futures
import copy


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
COUNTRIES_LOCK = threading.Lock()

COUNTRIES_LOCK.acquire()
# reads in all GDELT supported Countries
countryFile = open('supportedCountries.txt', 'r')
numCountries = int(countryFile.readline().rstrip('\n'))
for cCount in range(numCountries):
    line = countryFile.readline().rstrip('\n')
    countryData = line.split('\t')
    COUNTRIES.append(countryData)
countryFile.close()

COUNTRIES = [['CA', 'Canada']]
COUNTRIES_LOCK.release()

def collectMinutelyNums(inURL, inPayload):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    minuteCount = 0

    startMin = inPayload['STARTDATETIME']
    for i in range(59):
        endMin = incrementMin(startMin, 1)
        inPayload['ENDDATETIME'] = endMin
        minuteResp = requests.get(inURL, inPayload)
        try:
            minuteResults = minuteResp.json()
        except:
            printMulti(minuteResp)
            printMulti(f'minute {minuteResp.content} {inPayload["STARTDATETIME"]} {inPayload["ENDDATETIME"]}')
            return 0
        
        if (len(minuteResults.keys()) != 0):
            minuteArticles = len(minuteResults['articles'])
            minuteCount += minuteArticles
        
        startMin = endMin
        inPayload['STARTDATETIME'] = startMin
    
    return minuteCount

def collectHourlyNums(inURL, inPayload):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    hourCount = 0

    startHour = inPayload['STARTDATETIME']
    for i in range(23):
        endHour = incrementHour(startHour, 1)
        inPayload['ENDDATETIME'] = endHour
        hourlyResp = requests.get(inURL, inPayload)
        try:
            hourResults = hourlyResp.json()
        except:
            printMulti(hourlyResp)
            printMulti(f'hour {hourlyResp.content} {inPayload["STARTDATETIME"]} {inPayload["ENDDATETIME"]}')
            return 0
        
        if (len(hourResults.keys()) != 0):
            hourArticles = len(hourResults['articles'])
            if hourArticles >= MAX_ARTICLES:
                minuteArticles = collectMinutelyNums(inURL, inPayload)
                hourArticles = minuteArticles
            hourCount += hourArticles

        startHour = endHour
        inPayload['STARTDATETIME'] = startHour
    
    return hourCount

def collectDailyNums(inURL, inPayload):
    
    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    dailyCount = 0
    
    startDay = inPayload['STARTDATETIME']
    month = int(getMonth(startDay))
    for i in range (MONTH_END[month]):
        endDay = incrementDay(startDay, 1)
        inPayload['ENDDATETIME'] = endDay
        dailyResp = requests.get(inURL, inPayload)
        try:
            dailyResults = dailyResp.json()
        except:
            printMulti(dailyResp)
            printMulti(f'day {dailyResp.content} {inPayload["STARTDATETIME"]} {inPayload["ENDDATETIME"]}')
            return 0

        if (len(dailyResults.keys()) != 0):
            dailyArticles = len(dailyResults['articles'])
            if dailyArticles >= MAX_ARTICLES:
                hourArticles = collectHourlyNums(inURL, inPayload)
                dailyArticles = hourArticles
            dailyCount += dailyArticles
        
        startDay = endDay
        inPayload['STARTDATETIME'] = startDay
    

    return dailyCount

def collectMonthNums(inURL, inPayload):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    monthlyCount = 0

    monthlyResp = requests.get(inURL, params=inPayload)
    try:
        monthlyResults = monthlyResp.json()
    except:
        printMulti(monthlyResp)
        printMulti(f'month {monthlyResp.content} {inPayload["STARTDATETIME"]} {inPayload["ENDDATETIME"]}')
        return 0

    if len(monthlyResults.keys()) != 0:
        monthlyArticles = len(monthlyResults['articles'])
        if monthlyArticles >= MAX_ARTICLES:
            dailyArticles = collectDailyNums(inURL, inPayload)
            monthlyArticles = dailyArticles
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

COUNTRY_COUNTER_LOCK = threading.Lock()
COUNTRY_COUNTER = 0

COUNTRY_FREQ_LOCK = threading.Lock()
COUNTRY_FREQ = {}

PRINT_LOCK = threading.Lock()

def printMulti(strText):
    PRINT_LOCK.acquire()
    print(strText)
    PRINT_LOCK.release()
    return None

def gdeltRequester():
    
    gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

    global COUNTRY_COUNTER
    global COUNTRY_FREQ_LOCK
    global COUNTRY_COUNTER_LOCK
    global COUNTRY_FREQ
    global COUNTRIES

    COUNTRY_COUNTER_LOCK.acquire()
    while (COUNTRY_COUNTER < 1):

        countryIdx = COUNTRY_COUNTER
        COUNTRY_COUNTER += 1
        COUNTRY_COUNTER_LOCK.release()

        COUNTRIES_LOCK.acquire()
        countryCode = COUNTRIES[countryIdx][0]
        countryName = COUNTRIES[countryIdx][1]
        COUNTRIES_LOCK.release()
        printMulti(f'country code: {countryCode}')

        COUNTRY_FREQ_LOCK.acquire()
        COUNTRY_FREQ[countryCode] = {}
        COUNTRY_FREQ[countryCode]['seafoodCOVID'] = []
        COUNTRY_FREQ[countryCode]['seafood'] = []
        COUNTRY_FREQ_LOCK.release()

        payload = {}
        payload['MODE'] = 'ArtList'
        payload['FORMAT'] = 'JSON'

        # Gets maximum allowed number of articles per request
        payload['MAXRECORDS'] = '250'

        # start date Jan 1 2020
        # date format YYYYMMDDHHMMSS
        dateStart = '20200101000000'
        dateEnd = incrementMonth(dateStart, 1)

        # Will only search through articles posted through dateStart-dateEnd
        payload['STARTDATETIME'] = dateStart
        payload['ENDDATETIME'] = dateEnd

        # for JAN 2020 - MAY 2020 (inclusive)
        for i in range(5):

            # runs search for query with seafood and COVID-19 in it for this particular country
            printMulti(f"before seaCOVID {payload['STARTDATETIME']} {payload['ENDDATETIME']}")
            payload['QUERY'] = 'seafood "COVID-19" sourcecountry:' + countryCode
            numSeaCOVID = collectMonthNums(gdeltAPI, payload)
            
            # updates COUNTRY_FREQ dictionary with number of article hits
            COUNTRY_FREQ_LOCK.acquire()
            COUNTRY_FREQ[countryCode]['seafoodCOVID'].append(numSeaCOVID)
            COUNTRY_FREQ_LOCK.release()

            # runs search for query with seafood in it for this particular country
            payload['QUERY'] = 'seafood sourcecountry:' + countryCode
            printMulti(f"before SEA {payload['STARTDATETIME']} {payload['ENDDATETIME']}")
            numSea = collectMonthNums(gdeltAPI, payload)

            # updates COUNTRY_FREQ dictionary with number of article hits
            COUNTRY_FREQ_LOCK.acquire()
            COUNTRY_FREQ[countryCode]['seafood'].append(numSea)
            COUNTRY_FREQ_LOCK.release()

            # update start and end times
            dateStart = dateEnd
            dateEnd = incrementMonth(dateStart, 1)

            payload['STARTDATETIME'] = dateStart
            payload['ENDDATETIME'] = dateEnd

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
        
        fileName = 'freqData/' + countryCode + '.txt'
        recordFile = open(fileName, 'w')
        recordFile.write(countryName)
        recordFile.write('\n')
        recordFile.write('seafood AND COVID-19: ' + seaCOVIDHits)
        recordFile.write('\n')
        recordFile.write('seafood: ' +seaHits)
        recordFile.write('\n')
        recordFile.close()

        printMulti(f'{countryName} DONE')
        
        COUNTRY_COUNTER_LOCK.acquire()

    COUNTRY_COUNTER_LOCK.release()
    return None


threads = []

for i in range(10):
    threads.append(threading.Thread(target=gdeltRequester, args=()))
    threads[i].start()

for i in range(10):
    threads[i].join()