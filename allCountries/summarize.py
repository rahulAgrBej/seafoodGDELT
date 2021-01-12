import os
import json
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument('-y', '--year', type=str)
argParser.add_argument('-m', '--month', type=str)
argParser.add_argument('-d', '--day', type=str)
argParser.add_argument('-s', '--sourceCountry', type=str)
argParser.add_argument('-c', '--country', type=str)
argParser.add_argument('-c1', '--country1', type=str)
argParser.add_argument('-c2', '--country2', type=str)
argParser.add_argument('-o', '--outputFile', type=str)
args = argParser.parse_args()
print(args)

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

    if year == 2020:
        print(f'{year} {month} {day}')

    return date

def makeDateNum(date):
    return int(date[0:4]), int(date[4:6]), int(date[6:8])

def getFullData():
    return None

summaryData = ''

for fileName in resultsFiles:
    if fileName == '.DS_Store':
        continue
    fullPath = os.path.join(resultsFolder, fileName)
    print(fullPath)
    f = open(fullPath, 'r')
    rows = f.readlines()
    f.close()
    # make sure to skip the header
    for row in rows[1:]:
        possRow = row.rstrip('\n')
        row = row.rstrip('\n')
        cells = row.split(',')

        if args.sourceCountry != None:
            if cells[2] != args.sourceCountry:
                continue

        if args.country1 != None:
            if cells[0] != args.country1 or cells[1] != args.country2:
                continue

        if args.country != None:
            if cells[0] != args.country and cells[1] != args.country:
                continue

        if args.year != None:
            if cells[3] != args.year:
                continue
        
        if args.month != None:
            if cells[4] != args.month:
                continue

        if args.day != None:
            if cells[5] != args.day:
                continue
        
        # this avoids including rows where the social image url has commas in it
        insertRow = ''
        for i in range(9):
            insertRow += cells[i] + ','
        insertRow = insertRow.rstrip(',')
        summaryData += insertRow + '\n'

summaryTable = 'country1,country2,sourceCountry,year,month,day,domain,title,url\n'
#summaryTable = 'country1,country2,sourceCountry,year,month,day,domain,title,url,social_image,language,query\n'
summaryTable += summaryData


if args.outputFile != None:
    outFile = args.outputFile
else:
    outFile = 'summary_table.csv'
fOut = open(outFile, 'w')
fOut.write(summaryTable)
fOut.close()
