import os
import json
import pprint


folderName = "statesDateCounts/"
fileNames = os.listdir(folderName)

f = open("fullArticleData.txt", "r")
data = json.loads(f.read())
f.close()
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(data)

# This takes fullArticleData and turns it to a CSV format


# This was to turn all files in statesInfo to a more understandable format and deposit them into statesDatesCounts
"""
for fName in fileNames:
    print(fName)
    fpath = os.path.join("statesInfo/", fName)
    f = open(fpath, 'r')
    strFormat = f.read()
    f.close()
    if len(strFormat) > 0:
        countData = json.loads(strFormat)
    
        countData = countData["results"][0]["timeline"][0]["data"]
        wpath = os.path.join("statesDateCounts/", fName)
        
        wf = open(wpath, 'w')
        wf.write(json.dumps(countData))
        wf.close()

print("done writing files")
"""

