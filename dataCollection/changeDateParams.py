import math

monthEnd = {
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

def getMonth(inDate):
    return inDate[4:6]

def incrementYear(inDate, numYears):
    
    # increments year
    year = int(inDate[:4])
    year += numYears

    # puts year back into string
    inDate = str(year) + inDate[4:]
    return inDate

def incrementMonth(inDate, numMonths):

    # gets month
    month = int(inDate[4:6])

    totalMonths = month + numMonths

    # increments year if necessary
    if (totalMonths > 12):

        # get number of years to increment by
        numYears = math.floor(totalMonths / 12)

        # get number of years to increment
        inDate = incrementYear(inDate, numYears)
    
    # increment month
    month = (month + numMonths) % 12
    if (month == 0):
        month = 12
    
    # accounting for single digit ints
    if (month < 10):
        month = '0' + str(month)
    
    inDate = inDate[:4] + str(month) + inDate[6:]

    return inDate

def incrementDay(inDate, numDays):

    # gets day
    day = int(inDate[6:8])

    # gets month
    month = int(inDate[4:6])

    totalDays = day + numDays

    numMonths = 0

    # increments month if necessary
    while (totalDays > monthEnd[month]):
        totalDays = totalDays - monthEnd[month]
        month = (month + 1) % 12
        if month == 0:
            month = 12
        numMonths += 1
    
    if (totalDays == 0):
        totalDays = 1

    inDate = incrementMonth(inDate, numMonths)

    # increment day
    totalDays = totalDays % monthEnd[month]
    if (totalDays == 0):
        totalDays = monthEnd[month]

    if totalDays > 31:
        raise Exception('WRONG NUM DAYS')
    
    # accounts for single digit ints
    if (totalDays < 10):
        totalDays = '0' + str(day)
    
    inDate = inDate[:6] + str(totalDays) + inDate[8:]

    return inDate
    
"""
#### TESTING ####
testDate = '20200101000000'
print(incrementYear(testDate, 5))
print(incrementMonth(testDate, 14))
print(incrementDay(testDate,40))
"""