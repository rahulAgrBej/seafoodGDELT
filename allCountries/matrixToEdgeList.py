import pprint

# pp = pprint.PrettyPrinter(indent=3)

iFilePath = 'analysis_visualization/data/matrix2017.csv'

inFile = open(iFilePath, 'r')
lines = inFile.readlines()
inFile.close()

# build idx to country code dictionary
countries = lines[0]
countries = countries.rstrip('\n')
countryCodes = countries.split(',')

idxToCode = {}
idxCounter = 0
for code in countryCodes:
    idxToCode[idxCounter] = code
    idxCounter += 1

# rebuilding the matrix from the file
mtrx = []
for line in lines[1:]:
    line = line.rstrip('\n')
    cells = line.split(',')
    row = []
    for cell in cells:
        row.append(int(cell))
    mtrx.append(row)

nextIdx = 0
numCountries = len(mtrx)
edgesCSV = 'from,to,weight\n'
for rowIdx in range(len(mtrx)):
    for colIdx in range(len(mtrx[rowIdx:])):
        country1 = idxToCode[rowIdx]
        country2 = idxToCode[colIdx + nextIdx]
        value = mtrx[rowIdx][colIdx + nextIdx]
        print(f'rowidx {rowIdx} colIdx {colIdx + nextIdx}')
        #print(f'country1: {country1} country2: {country2} value: {value}')
        edgeLine = f'{country1},{country2},{value}\n'
        edgesCSV += edgeLine
    nextIdx += 1

outFilePath = 'analysis_visualization/data/edges2017.csv'
outFile = open(outFilePath, 'w')
outFile.write(edgesCSV)
outFile.close()