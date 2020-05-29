
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