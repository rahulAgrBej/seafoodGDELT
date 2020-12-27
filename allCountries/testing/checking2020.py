import os
import pprint

folder2020 = '2020/'
folderArticles = '../articleResults/'

inconsistentLines = []

# First collect all 2020 articles from 2017 - 2019
articleFiles = os.listdir(folderArticles)
for fileName in articleFiles:
    if fileName[-3:] == 'csv':
        fullPath = os.path.join(folderArticles, fileName)
        f = open(fullPath, 'r')
        fileLines = f.read()
        f.close()

        fileLines = fileLines.split('\n')
        for line in fileLines[1:]:
            if len(line) > 0:
                line = line.rstrip('\n')
                data = line.split(',')
                if data[3] == '2020':
                    inconsistentLines.append(line)

# pp = pprint.PrettyPrinter(indent=3)
# pp.pprint(inconsistentLines)
# print(len(inconsistentLines))

articlesCollected = []

officialArticles2020 = os.listdir(folder2020)
for officialFileName in officialArticles2020:
    officialPath = os.path.join(folder2020, officialFileName)
    f = open(officialPath, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    for dataIdx in range(len(data))[1:]:
        newLine = data[dataIdx].rstrip('\n')
        newData = newLine.split(',')
        data[dataIdx] = newData
    articlesCollected.extend(data)



print('looping to find articles within 2020 dataset')

notFound = []
found = False
for inconsistentLine in inconsistentLines:
    for ln in articlesCollected:
        if ln[8] == inconsistentLine[8]:
            found = True
            print('found!')
            break
    
    if not found:
        print('NOT found!')
        notFound.append(inconsistentLine)
    
    found = False

print('finished!')