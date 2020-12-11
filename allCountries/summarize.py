import os
import json

resultsFolder = 'articleResults/'
resultsFiles = os.listdir(resultsFolder)

def makeDateStr(year, month, day):
    date = str(year)
    
    if month < 10:
        date += str(0)
    
    date += str(month)

    if day < 10:
        date += str(0)
    
    date += str(day)

    return date

def makeDateNum(date):
    return int(date[0:4]), int(date[4:6]), int(date[6:8])

summaryData = {}

for fileName in resultsFiles:
    fullPath = os.path.join(resultsFolder, fileName)
    f = open(fullPath, 'r')
    rows = f.readlines()
    f.close()

    # create a conditonal here if only looking for articles from a specific country or other criteria

    # make sure to skip the header
    for row in rows[1:]:
        row = row.rstrip('\n')
        cells = row.split(',')
        year = int(cells[3])
        month = int(cells[4])
        day = int(cells[5])

        date = makeDateStr(year, month, day)

        if not (date in summaryData):
            summaryData[date] = 0
        
        summaryData[date] += 1

summaryTable = 'year,month,day,freq\n'

for entry in summaryData:

    year, month, day = makeDateNum(entry)
    freq = summaryData[entry]
    rowEntry = str(year) + ',' + str(month) + ',' + str(day) + ',' + str(freq) + '\n'
    summaryTable += rowEntry

outFile = 'analysis_visualization/summaryTable.csv'
fOut = open(outFile, 'w')
fOut.write(summaryTable)
fOut.close()
