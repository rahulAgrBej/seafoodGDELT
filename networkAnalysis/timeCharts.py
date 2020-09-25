import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

folderPath = "freqResults/"
fileNames = os.listdir(folderPath)

for fName in fileNames:
    fullPath = os.path.join(folderPath, fName)
    f = open(fullPath, 'r')
    stringFormat = f.read()
    f.close()

    data = json.loads(stringFormat)
    dates = []
    values = []
    for entry in data:
        inYear = int(entry["date"][0:4])
        inMonth = int(entry["date"][4:6])
        inDay = int(entry["date"][6:8])
        dates.append(datetime(year=inYear, month=inMonth, day=inDay))
        values.append(entry["value"])
    
    plt.scatter(dates, values)
    plt.plot(dates, values, '-o')

    figureName = "timeGraphs/" + fName
    
    plt.savefig(figureName)
    plt.close()