
def readCountries():

    sourceCountries = {}

    f = open('countryLookUp.txt', 'r')
    data = f.readlines()
    f.close()

    for country in data:
        country = country.rstrip('\n')
        country = country.split('\t')
        sourceCountries[country[0]] = ' '.join(country[1:])

    return sourceCountries


print(readCountries())