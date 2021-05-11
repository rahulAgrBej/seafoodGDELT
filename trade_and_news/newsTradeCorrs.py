
import math
from scipy.stats.stats import pearsonr
import pandas as pd

def tradeNewsCorr(tradeData, newsData):

    # get all countries
    countries = tradeData['CTY_NAME'].unique()

    tradeNewsCorrelations = {
        'CTY_NAME': [],
        'CORR_0': [],
        'CORR_1': [],
        'CORR_2': [],
        'CORR_0_ABS': [],
        'CORR_1_ABS': [],
        'CORR_2_ABS': []
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
        
        newsShifts = [0,1,2]
        correlations = []
        for newsShift in newsShifts:
            zeros = [0] * newsShift
            newsList = list(countryTradeData['TOTAL'])
            a = zeros + newsList[:(len(newsList) - newsShift)]
            b = list(countryNewsData['TOTAL'])

            tradeNewsCorr, p_value = pearsonr(a, b)
            if math.isnan(tradeNewsCorr):
                tradeNewsCorr = 0
            
            correlations.append(tradeNewsCorr)

        tradeNewsCorrelations['CTY_NAME'].append(country)
        tradeNewsCorrelations['CORR_0'].append(correlations[0])
        tradeNewsCorrelations['CORR_1'].append(correlations[1])
        tradeNewsCorrelations['CORR_2'].append(correlations[2])
        tradeNewsCorrelations['CORR_0_ABS'].append(abs(correlations[0]))
        tradeNewsCorrelations['CORR_1_ABS'].append(abs(correlations[1]))
        tradeNewsCorrelations['CORR_2_ABS'].append(abs(correlations[2]))

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

importCorrOutPath = 'data/analysis/processed/original/importCorrs.csv'
exportCorrOutPath = 'data/analysis/processed/original/exportCorrs.csv'

importCorrF = open(importCorrOutPath, 'w')
importCorrF.write(newsImportCorrs.to_csv(index=False))
importCorrF.close()

exportCorrF = open(exportCorrOutPath, 'w')
exportCorrF.write(newsExportCorrs.to_csv(index=False))
exportCorrF.close()
