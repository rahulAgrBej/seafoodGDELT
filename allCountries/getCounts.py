import os
import json
import setup

startDate = '01/01/2017'
startTime = '00:00:00'

endDate = '02/01/2017'
endTime = '00:00:00'

query = '(seafood OR fish OR crab OR shrimp)'

combos = list(setup.allCombos())[:1000]
print(len(combos))

reqs = setup.buildArticleCountsReqs(query, combos, startDate, startTime, endDate, endTime)
print(reqs)

reqLimit = 15
data = setup.sendCountReqs(reqs, reqLimit)
print("THIS IS THE DATA")
print(data)

outFolder = 'tmpDataStorage/'
outF = '0_10.txt'
f = open(os.path.join(outFolder, outF), 'w')
f.write(json.dumps(data))
f.close()
