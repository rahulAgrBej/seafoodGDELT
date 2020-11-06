import os
import json

folderName = 'stage0/'
fileNames = os.listdir(folderName)

sub250 = ''
over250 = ''


for fName in fileNames:
    fullPath = os.path.join(folderName, fName)
    f = open(fullPath, 'r')
    content = json.loads(f.read())
    f.close()

    total = 0

    for row in content:
        total += row['value']

    if total > 250:
        over250 += fName + '\n'
    else:
        sub250 += fName + '\n'

fSub = open('sub250.txt', 'w')
fSub.write(sub250)
fSub.close()

fOver = open('over250.txt', 'w')
fOver.write(over250)
fOver.close()

print("done!")