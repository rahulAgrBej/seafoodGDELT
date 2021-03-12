
source('residualsAnalysis.R')
source('helpers.R')

# aggregate data exports and imports
aggregateTrade <- function(countryInfo) {
  countryInfo <- getInfo(country)
  
  importsInfo <- countryInfo %>% filter(
    str_detect(TYPE, 'IMPORTS')
  )
  exportsInfo <- countryInfo %>% filter(
    str_detect(TYPE, 'EXPORTS')
  )
  
  countryInfo$TOTAL_TRADE <- importsInfo$COUNTS + exportsInfo$COUNTS
  trade <- data.frame(countryInfo$CTY_NAME, countryInfo$MONTH, countryInfo$YEAR, countryInfo$MONTH_IDX, countryInfo$TOTAL_TRADE)
  trade <- unique(trade)
  colnames(trade) <- c('CTY_NAME', 'MONTH', 'YEAR', 'MONTH_IDX', 'COUNTS')
  trade$TYPE <- rep('TOTAL_TRADE', 48)
  
  trade$COUNTS <- as.numeric(trade$COUNTS)
  
  return(trade)
}

# COUNT_PLOT is residuals for imports and exports and is the frequency of articles for news

# calculates baseline correlation

relevantCountries <- read_csv('data/relevantCountries.csv')

country <- relevantCountries[1,]
countryInfo <- getInfo(country)
trade <- aggregateTrade(countryInfo)

# calculate residuals for aggregate trade
tradeResiduals <- getResiduals(trade)


for (idx in 1:) {
  country <- relevantCountries[idx,]
  countryInfo <- getInfo(country)
  
  newsInfo <- countryInfo %>% filter(
    str_detect(TYPE, 'NEWS')
  )
  importsInfo <- countryInfo %>% filter(
    str_detect(TYPE, 'IMPORTS')
  )
  exportsInfo <- countryInfo %>% filter(
    str_detect(TYPE, 'EXPORTS')
  )
  print(countryInfo$CTY_NAME)
  print('news exports')
  print(cor(newsInfo$COUNT_PLOT, exportsInfo$COUNT_PLOT))
  print('news imports')
  print(cor(newsInfo$COUNT_PLOT, importsInfo$COUNT_PLOT))
}