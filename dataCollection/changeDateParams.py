
def incrementYear(inDate, numYears):
    
    # increments year
    year = int(inDate[:4])
    year += numYears

    # puts year back into string
    inDate = str(year) + inDate[4:]
    return inDate

test = '20200101000000'
print(test)
print(incrementYear(test, 5))