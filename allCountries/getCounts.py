import os
import json
import setup

startDate = '01/01/2020'
startTime = '00:00:00'

endDate = '01/01/2021'
endTime = '00:00:00'

query = '(toothfish OR swordfish OR shellfish)'

combos = list(setup.combosUS())
combos = [['US', 'CH']]
sendCombos = []

for comboIdx in range(len(combos)):

    sendCombos.append(combos[comboIdx])

    if (len(sendCombos) % 1000 == 0):
        reqs = setup.buildArticleCountsReqs(query, sendCombos, startDate, startTime, endDate, endTime)
        reqLimit = 15
        data = setup.sendCountReqs(reqs, reqLimit)
        outFolder = 'CHINA/'
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
    outFolder = 'CHINA/'
    outF = f'{str(len(combos)-(len(combos) % 1000))}_{str(len(combos))}.txt'
    f = open(os.path.join(outFolder, outF), 'w')
    f.write(json.dumps(data))
    f.close()
    print(f'{comboIdx} combinations searched for')
