
import math
from scipy.stats.stats import pearsonr
import pandas as pd

def tradeNewsCorr(tradeData, newsData):

    # get all countries
    countries = tradeData['CTY_NAME'].unique()

    tradeNewsCorrelations = {
        'CTY_NAME': [],
        'CORR': []
    }

    for country in countries:
        print(country)

        # Get country trade records and sort by month idx
        countryTradeData = (tradeData['CTY_NAME'] == country)
        countryTradeData = tradeData[countryTradeData]
        countryTradeData = countryTradeData.sort_values(by=['MONTH_IDX'])

        # Get news trade records and sort by month idx
        countryNewsData = (newsData['CTY_NAME'] == country)
        countryNewsData = newsData[countryNewsData]
        countryNewsData = countryNewsData.sort_values(by=['MONTH_IDX'])
        
        a = list(countryTradeData['TOTAL'])
        b = list(countryNewsData['TOTAL'])
        tradeNewsCorr, p_value = pearsonr(a, b)
        if math.isnan(tradeNewsCorr):
            tradeNewsCorr = 0
        print(tradeNewsCorr)

        tradeNewsCorrelations['CTY_NAME'].append(country)
        tradeNewsCorrelations['CORR'].append(tradeNewsCorr)

    tradeNewsCorrelationsDF = pd.DataFrame(data=tradeNewsCorrelations)
    
    return tradeNewsCorrelationsDF

# Get News COUNTS data
newsCountsPath = 'data/news/processed/original/newsCounts.csv'
newsCounts = pd.read_csv(newsCountsPath)


# Get trade shock data
importDataPath = 'data/trade/processed/original/imports.csv'
importData = pd.read_csv(importDataPath)

exportDataPath = 'data/trade/processed/original/exports.csv'
exportData = pd.read_csv(exportDataPath)

newsImportCorrs = tradeNewsCorr(importData, newsCounts)
newsExportCorrs = tradeNewsCorr(exportData, newsCounts)

importCorrOutPath = 'data/trade/processed/original/importCorrs.csv'
exportCorrOutPath = 'data/trade/processed/original/exportCorrs.csv'

importCorrF = open(importCorrOutPath, 'w')
importCorrF.write(newsImportCorrs.to_csv(index=False))
importCorrF.close()

exportCorrF = open(exportCorrOutPath, 'w')
exportCorrF.write(newsExportCorrs.to_csv(index=False))
exportCorrF.close()
