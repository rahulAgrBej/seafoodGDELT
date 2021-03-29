
import os
import json
import pprint

# writes results for trade type into csv table
def writeResults(outCSV, content):

    for year in content:
        for countryName in content[year]['countries']:
            countryTotal = content[year]['countries'][countryName]['total']
            countryMonths = content[year]['countries'][countryName]['months']
            outCSV += f'{countryName},{str(countryTotal)},{str(countryMonths)},{str(year)}\n'
    
    return outCSV

# returns the yearly trade total
def getTradeTotals(tradeRows):
    # header for trade records
    headerRow = tradeRows[0]

    # gets total seafood trade for year
    tradeRows = tradeRows[1:]
    totalRows = tradeRows[0:12]

    totalTrade = 0
    for record in totalRows:
        record = record.rstrip('\n')
        cells = record.split(',')
        monthTotal = int(cells[2])
        totalTrade += monthTotal
    
    return totalTrade

def processTrade(dirPath, tradeYears, tradeType, outFileName):

    countryTotals = {}

    for year in tradeYears:
        countryTotals[year] = {}
        fileName = tradeType + str(year) + '.csv'
        filePath = os.path.join(dirPath, fileName)

        tradeContent = open(filePath, 'r')
        tradeRows = tradeContent.readlines()
        totalYearTrade = getTradeTotals(tradeRows)
        countryTotals[year]['total'] = totalYearTrade
        countryTotals[year]['countries'] = {}
        countryTotals[year]['countries']['ALL_COUNTRIES'] = {}
        countryTotals[year]['countries']['ALL_COUNTRIES']['total'] = totalYearTrade
        countryTotals[year]['countries']['ALL_COUNTRIES']['months'] = 12

        tradeRows = tradeRows[13:]
        for record in tradeRows:
            record = record.rstrip('\n')
            cells = record.split(',')
            countryName = cells[1]
            
            if not (countryName in countryTotals[year]['countries']):
                countryTotals[year]['countries'][countryName] = {}
                countryTotals[year]['countries'][countryName]['total'] = 0
                countryTotals[year]['countries'][countryName]['months'] = 0

            monthTradeCount = int(cells[2])
            countryTotals[year]['countries'][countryName]['total'] += monthTradeCount
            if monthTradeCount > 0:
                countryTotals[year]['countries'][countryName]['months'] += 1
    
    outCSV = 'COUNTRY,TOTAl,MONTHS,YEAR\n'
    outCSV = writeResults(outCSV, countryTotals)
    f = open(outFileName, 'w')
    f.write(outCSV)
    f.close()
    
    return None

dirPath = 'data/trades/countries/'

tradeYears = [2017,2018,2019,2020]
exportType = 'exportCountries'
importType = 'importCountries'

processTrade(dirPath, tradeYears, exportType, 'exportsBaseline.csv')
processTrade(dirPath, tradeYears, importType, 'importsBaseline.csv')
