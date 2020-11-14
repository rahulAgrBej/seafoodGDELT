import os
import json
import setup

startDate = '01/01/2017'
startTime = '00:00:00'

endDate = '01/01/2018'
endTime = '00:00:00'

query = '(seafood OR fish OR crab OR shrimp)'

combos = list(setup.allCombos())

for comboIdx in range(len(combos)):
    
    if (comboIdx > 0) and (comboIdx % 10 == 0):
        reqs = setup.buildArticleCountsReqs(query, combos[comboIdx - 10:comboIdx], startDate, startTime, endDate, endTime)
        reqLimit = 15
        data = setup.sendCountReqs(reqs, reqLimit)
        print("THIS IS THE DATA")
        print(data)
        outFolder = 'tmpDataStorage/'
        outF = f'{str(comboIdx-10)}_{str(comboIdx)}.txt'
        f = open(os.path.join(outFolder, outF), 'w')
        f.write(json.dumps(data))
        f.close()
