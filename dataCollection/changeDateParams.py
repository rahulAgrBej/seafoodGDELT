
monthDays = {
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

    # increments year if necessary
    if (month + numMonths > 12):
        inDate = incrementYear(inDate, 1)
    
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

    # increments month if necessary
    if (day + numDays > monthDays[month]):
        newDate = incrementMonth(inDate, 1)
    
    # increment day
    day = (day + numDays) % monthDays[month]
    if (day == 0):
        day = monthDays[month]
    
    # accounts for single digit ints
    if (day < 10):
        day = '0' + str(day)
    
    inDate = inDate[:6] + day + inDate[8:]

    return inDate
    