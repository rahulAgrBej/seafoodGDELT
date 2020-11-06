from itertools import permutations, combinations


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

def allCombos():
    combos = []

    sourceCountries = readCountries()
    ids = sourceCountries.keys()
    combos = permutations(ids, 2)

    return combos

print([i for i in allCombos()])