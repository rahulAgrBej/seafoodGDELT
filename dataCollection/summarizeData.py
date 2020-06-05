import os
import matplotlib.pyplot as plt

def plotPercents(folderName):

    countryPercents = {}

    # get list of files from directory
    dataFileNames = os.listdir(folderName)

    for fileName in dataFileNames:

        filePath = os.path.join(folderName, fileName)
        file = open(filePath, 'r')
        countryName = file.readline().rstrip('\n')
        countryPercents[countryName] = []

        # getting results from seafood AND COVID-19 query
        line = file.readline()
        line = line[22:]
        seafoodCOVID = line.split(' ')
        seafoodCOVID = [int(num) for num in seafoodCOVID]
        
        # getting results from seafood query
        line = file.readline().rstrip('\n')
        
        file.close()
        
        line = line[9:]
        seafood = line.split(' ')
        seafood = [int(num) for num in seafoodCOVID]

        for i in range(len(seafoodCOVID)):

            if seafood[i] != 0:
                countryPercents[countryName].append(float(seafoodCOVID[i] / seafood[i]))
            else:
                countryPercents[countryName].append(0)
    
    return countryPercents


"""
monthNames = ['Jan', 'Feb', 'March', 'April', 'May']


countryScatters = []
for country in countryList:
    countryScatters.append(plt.plot(monthNames, countryFreq[country], label=country)) 

plt.legend()

plt.savefig('dataCollection/sample.png')
"""

percentData = plotPercents('freqData')
monthNames = ['Jan', 'Feb', 'March', 'April', 'May']
countryScatters = []

for country in percentData.keys():
    countryScatters.append(plt.plot(monthNames, percentData[country], label=country))

plt.legend()
plt.savefig('sampleWHOLE.png')
