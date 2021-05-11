
import numpy as np
import pandas as pd

def tradeNewsShockAlignment(tradeData, newsData):
    newsShocks = (newsData['shock.event'] == 1)
    newsShocks = newsData[newsShocks]

    tradeShocks = (tradeData['shock.event'] == 1)
    tradeShocks = tradeData[tradeShocks]

    tradeShockCountries = tradeShocks['CTY_NAME'].unique()

    tradeNewsAlignment = {
        'CTY_NAME': [],
        'TRADE_SHOCK_MONTH': [],
        'PREV_NEWS_SHOCKS': []
    }

    # checking to see if news shocks come before import shocks
    for country in tradeShockCountries:
        countryTradeShocks = (tradeShocks['CTY_NAME'] == country)
        countryTradeShocks = tradeShocks[countryTradeShocks]
        countryTradeShockMonths = countryTradeShocks['MONTH_IDX']

        # get all shocks for a given country in news
        countryNewsShocks = (newsShocks['CTY_NAME'] == country)
        countryNewsShocks = newsShocks[countryNewsShocks]

        # check if news shocks existed on that given month or up to two months before
        for monthIdx in countryTradeShockMonths:

            checkMonths = [monthIdx]
            if ((monthIdx - 1) > 0):
                checkMonths.append(monthIdx - 1)
            
            if ((monthIdx - 2) > 0):
                checkMonths.append(monthIdx - 2)

            newsMonths = list(countryNewsShocks['MONTH_IDX'])
            numShocksAligned = 0

            for checkMonth in checkMonths:
                for newsMonth in newsMonths:
                    if checkMonth == newsMonth:
                        numShocksAligned += 1
            
            tradeNewsAlignment['CTY_NAME'].append(country)
            tradeNewsAlignment['TRADE_SHOCK_MONTH'].append(monthIdx)
            tradeNewsAlignment['PREV_NEWS_SHOCKS'].append(numShocksAligned)
        
    tradeNewsAlignmentDF = pd.DataFrame(data=tradeNewsAlignment)

    return tradeNewsAlignmentDF

# Get news shock data
newsShockPath = 'data/news/processed/original/newsShocks.csv'
newsShockData = pd.read_csv(newsShockPath)

# Get trade shock data
importShocksPath = 'data/trade/processed/original/importShocks.csv'
importShockData = pd.read_csv(importShocksPath)

exportShocksPath = 'data/trade/processed/original/exportShocks.csv'
exportShockData = pd.read_csv(exportShocksPath)

importNewsAlignment = tradeNewsShockAlignment(importShockData, newsShockData)
exportNewsAlignment = tradeNewsShockAlignment(exportShockData, newsShockData)

importOutPath = 'data/analysis/processed/original/importNewsAlignment.csv'
importOutF = open(importOutPath, 'w')
importOutF.write(importNewsAlignment.to_csv(index=False))
importOutF.close()

exportOutPath = 'data/analysis/processed/original/exportNewsAlignment.csv'
exportOutF = open(exportOutPath,'w')
exportOutF.write(exportNewsAlignment.to_csv(index=False))
exportOutF.close()