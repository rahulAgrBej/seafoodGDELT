
source('residualsAnalysis.R')
source('helpers.R')

# aggregate data exports and imports
aggregateTrade <- function(countryInfo, importsInfo, exportsInfo) {

  countryInfo$TOTAL_TRADE <- importsInfo$COUNTS + exportsInfo$COUNTS
  trade <- data.frame(countryInfo$CTY_NAME, countryInfo$MONTH, countryInfo$YEAR, countryInfo$MONTH_IDX, countryInfo$TOTAL_TRADE)
  trade <- unique(trade)
  colnames(trade) <- c('CTY_NAME', 'MONTH', 'YEAR', 'MONTH_IDX', 'COUNTS')
  trade$TYPE <- rep('TOTAL_TRADE', 48)
  
  trade$COUNTS <- as.numeric(trade$COUNTS)
  
  return(trade)
}

calculateCorr <- function(cty_name, newsBase, trade, tradeType) {
  
  baseCorr <- cor(newsBase, trade)
  
  # correlation news predicts trade patterns (move news up by 1 to 3 months with NAs)
  add1 <- prepend(newsBase, rep(NA,1))[1:48]
  add2 <- prepend(newsBase, rep(NA,2))[1:48]
  add3 <- prepend(newsBase, rep(NA,3))[1:48]
  
  add1Corr <- cor(add1, trade, use='complete.obs')
  add2Corr <- cor(add2, trade, use='complete.obs')
  add3Corr <- cor(add3, trade, use='complete.obs')
  
  # correlation TRADE predicts news (move news down by 1 to 3 months with NAs)
  sub1 <- append(newsBase, rep(NA,1))[2:49]
  sub2 <- append(newsBase, rep(NA,2))[3:50]
  sub3 <- append(newsBase, rep(NA,3))[4:51]
  
  sub1Corr <- cor(sub1, trade, use='complete.obs')
  sub2Corr <- cor(sub2, trade, use='complete.obs')
  sub3Corr <- cor(sub3, trade, use='complete.obs')
  
  results <- data.frame(cty_name, baseCorr, add1Corr, add2Corr, add3Corr, sub1Corr, sub2Corr, sub3Corr)
  colnames(results) <- c('CTY_NAME', 'baseCorr', 'add1Corr', 'add2Corr', 'add3Corr', 'sub1Corr', 'sub2Corr', 'sub3Corr')
  results$TYPE <- tradeType
  
  return(results)
}

relevantCountries <- read_csv('data/relevantCountries.csv')

countryCorrs <- data.frame(CTY_NAME=character(),
                           baseCorr=numeric(),
                           add1Corr=numeric(),
                           add2Corr=numeric(),
                           add3Corr=numeric(),
                           sub1Corr=numeric(),
                           sub2Corr=numeric(),
                           sub3Corr=numeric(),
                           TYPE=character())

colnames(countryCorrs) <- c('CTY_NAME', 'baseCorr', 'add1Corr', 'add2Corr', 'add3Corr', 'sub1Corr', 'sub2Corr', 'sub3Corr', 'TYPE')

for (idx in 1:nrow(relevantCountries)) {
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
  
  trade <- aggregateTrade(countryInfo, importsInfo, exportsInfo)
  
  # calculate residuals for aggregate trade
  trade <- getResiduals(trade)
  
  tradeCorrs <- calculateCorr(unique(countryInfo$CTY_NAME), newsInfo$COUNTS, trade$residual, 'TRADE')
  exportCorrs <- calculateCorr(unique(countryInfo$CTY_NAME), newsInfo$COUNTS, exportsInfo$residual, 'EXPORTS')
  importCorrs <- calculateCorr(unique(countryInfo$CTY_NAME), newsInfo$COUNTS, importsInfo$residual, 'IMPORTS')
  
  countryCorrs <- rbind(countryCorrs, tradeCorrs,exportCorrs,importCorrs)

}