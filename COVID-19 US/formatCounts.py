import os
import json

fileNames = os.listdir("statesInfo/")

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