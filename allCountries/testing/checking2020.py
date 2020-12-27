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

pp = pprint.PrettyPrinter(indent=3)
pp.pprint(inconsistentLines)
print(len(inconsistentLines))

