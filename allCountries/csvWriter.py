import os
import json

inputFolder = 'tmpDataStorage/'
inputFiles = os.listdir(inputFolder)

# collecting all raw data
completeData = []

for inFile in inputFiles:
    fullFilePath = os.path.join(inputFolder, inFile)
    f = open(fullFilePath, 'r')
    fileData = json.loads(f.read())
    f.close()

    completeData.extend(fileData)

# get dictionary of name to code
countryCodeFile = open('countryLookUp.txt', 'r')
countries = countryCodeFile.readlines()
countryCodeFile.close()

countryCodes = {}

for country in countries:
    country = country.rstrip('\n')
    countryInfo = country.split('\t')
    countryCodes[countryInfo[1]] = countryInfo[0]

# writing to csv file
testFile = 'testing/testTable.csv'
outF = open(testFile, 'w')

freqHeader = 'country1,country2,sourceCountry,date,value,norm\n'
outF.write(freqHeader)

for entry in completeData:

    if len(entry['timeline']) > 0:
    
        quoteIdx = []
        for chIdx in range(len(entry['query_details']['title'])):
            if entry['query_details']['title'][chIdx] == '\"':
                quoteIdx.append(chIdx)
        
        countryName1 = entry['query_details']['title'][quoteIdx[0] + 1:quoteIdx[1]]
        countryName2 = entry['query_details']['title'][quoteIdx[2] + 1:quoteIdx[3]]

        countryCode1 = countryCodes[countryName1]
        countryCode2 = countryCodes[countryName2]
        sourceCountryCode = entry['query_details']['title'][-2:]

        entries = entry['timeline'][0]['data']
        for dt in entries:
            value = dt['value']
            norm = dt['norm']
            date = dt['date'][:8]

            dataEntry = f'{countryCode1},{countryCode2},{sourceCountryCode},{date},{value},{norm}\n'
            outF.write(dataEntry)

outF.close()
print("Done writing to csv file")
