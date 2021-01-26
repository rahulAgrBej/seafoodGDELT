import pprint

pp = pprint.PrettyPrinter(indent=3)


# Read in all countries and provide them an index
countriesFilePath = 'countryLookUp.csv'
countryF = open(countriesFilePath, 'r')
countries = countryF.readlines()
countryF.close()

countries = countries[1:] # eliminates header row

# creates country matrix filled with 0's
numCountries = len(countries)
countryMtrx = []
for idx in range(numCountries):
    countryMtrx.append([0] * numCountries)

# creates country lookup dictionary
countryIdx = {}
lineIdx = 0
for line in countries:
    line = line.rstrip('\n')
    vals = line.split(',')
    country = vals[0] # uses/get country code
    countryIdx[country] = lineIdx
    lineIdx += 1

# Build a n x n matrix where n = number of all countries being considered
# all values inside the matrix should be 0 by default
# matrix will be symmetrical

dataFilePath = 'summary_table.csv'
dataF = open(dataFilePath, 'r')
dataCountries = dataF.readlines()
dataF.close()

dataCountries = dataCountries[1:] # eliminates header row
for row in dataCountries:
    row = row.rstrip('\n')
    cells = row.split(',')
    
    # gets which countries are involved in this row
    countryA = cells[0]
    countryB = cells[1]
    idxA = countryIdx[countryA]
    idxB = countryIdx[countryB]

    # adds to counter for each part of the matrix b/c it is symmetrical
    countryMtrx[idxA][idxB] += 1
    countryMtrx[idxB][idxA] += 1

# writes matrix into CSV file
matrixCSV = ''
for counterRow in countryMtrx:
    for count in counterRow[:-1]:
        matrixCSV += str(count) + ','
    matrixCSV += str(counterRow[-1])
    matrixCSV += '\n'

outFilePath = 'matrix.csv'
outF = open(outFilePath, 'w')
outF.write(matrixCSV)
outF.close()