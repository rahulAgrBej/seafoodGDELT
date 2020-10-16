import os
import json

folderPath = 'stage0/'
fileNames = os.listdir(folderPath)

csvContent = "country1,country2,sourceCountry,year,month,day\n"

for fName in fileNames:
    # open the file
    fullPath = os.path.join(folderPath,fName)
    f = open(fullPath, 'r')
    fileContent = json.loads(f.read())
    f.close()

    country1 = fName[:2]
    country2 = fName[2:4]
    sourceCountry = fName[4:6]

    for row in fileContent:
        year = int(row['date'][:4])
        month = int(row['date'][4:6])
        day = int(row['date'][6:8])
        
        outRow = country1 + ',' + country2 + ',' + sourceCountry + ',' + str(year) + ',' + str(month) + ',' + str(day) + '\n'
        csvContent = csvContent + outRow
    print("done with file: " + fName)

outFile = "resultsTable.csv"
fOut = open(outFile, 'w')
fOut.write(csvContent)
fOut.close()

print("DONE!")