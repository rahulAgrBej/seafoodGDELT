
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
