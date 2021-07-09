import os
import json
import setup

startDate = '01/01/2017'
startTime = '00:00:00'

endDate = '01/01/2018'
endTime = '00:00:00'

query = '(seafood OR fish OR crab OR shrimp OR salmon OR lobster OR tuna)'

combos = list(setup.combosUS())
#combos = [['US', 'CH']]
sendCombos = []

for comboIdx in range(len(combos)):

    sendCombos.append(combos[comboIdx])

    if (len(sendCombos) % 15 == 0):
        print('BUILDING REQS')
        reqs = setup.buildArticleCountsReqs(query, sendCombos, startDate, startTime, endDate, endTime)
        print(reqs)
        reqLimit = 15
        print('SENDING REQS')
        data = setup.sendCountReqs(reqs, reqLimit)
        outFolder = 'tmpData/2017_1/'
        outF = f'{str(comboIdx-1000)}_{str(comboIdx)}.txt'
        f = open(os.path.join(outFolder, outF), 'w')
        f.write(json.dumps(data))
        f.close()
        print(f'{comboIdx} combinations searched for')
        sendCombos = []

if (len(sendCombos) > 0):
    reqs = setup.buildArticleCountsReqs(query, sendCombos, startDate, startTime, endDate, endTime)
    reqLimit = 15
    data = setup.sendCountReqs(reqs, reqLimit)
    outFolder = 'tmpData/2017_1/'
    outF = f'{str(len(combos)-(len(combos) % 1000))}_{str(len(combos))}.txt'
    f = open(os.path.join(outFolder, outF), 'w')
    f.write(json.dumps(data))
    f.close()
    print(f'{comboIdx} combinations searched for')
