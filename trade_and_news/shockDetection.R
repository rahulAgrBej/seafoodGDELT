
# Shock Detection Function
shock.id <- function(dat, thresh=0.25){
  # dat is your time series data and threshold is the threshold you want for Cook's D (defaulted to 0.35)
  outt <- array(dim=c(length(dat), 3))
  x <- 1:length(dat)
  ll <- lowess(x, dat, f=(2/3)) # Fits lowess curve (can specify other options for how the curve is estimated and can change the span)
  rr <- as.numeric(dat[order(x)]-ll$y) #residuals off lowess
  rrp1 <- rr[2:length(rr)] # Residuals at time t
  rrm1 <- rr[1:(length(rr)-1)] # Residuals at time t-1
  ll2 <- lm(rrp1~rrm1) # Linear fit of the residuals
  cd <- cooks.distance(ll2) # Calculate the Cook's D
  outt[2:length(rr),1] <- as.numeric(cd) # Output the Cook's D
  outt[,2] <- rr # Output the residuals
  outt[2:length(rr),3] <- ifelse(as.numeric(cd) >= thresh,1,0) # Logical of whether point is a shock
  outt <- as.data.frame(outt)
  colnames(outt) <- c("cooks.d", "residual", "shock.event")
  return(outt)
}

# finds shocks for trade data
findShocks <- function(tradeData, countryName) {

  countryData <- tradeData %>%
    filter(str_detect(CTY_NAME, countryName)) %>%
    filter(str_length(CTY_NAME) == str_length(countryName)) %>%
    arrange(YEAR, MONTH)
  
  if (nrow(countryData) > 0) {
    # if records exist for this country
    tradeShocks <- shock.id(countryData$TOTAL) %>%
      mutate(cooks.d = replace_na(cooks.d, 0)) %>%
      mutate(shock.event = replace_na(shock.event, 0))
  } else {
    # edge case there are no records for this country
    tradeShocks <- data.frame(
      cooks.d=rep(0, 48),
      residual=rep(0,48),
      shock.event=rep(0,48)
    )
  }
  
  monthIndices <- data.frame(
    'MONTH_IDX'=seq(1,48)
  )
  
  tradeShocks <- tradeShocks %>%
    cbind(monthIndices)
  
  return(tradeShocks)
}

# Trade data file paths and retrieval (PROCESSED VERSION)
importFilePath <- 'data/trade/processed/original/imports.csv'
exportFilePath <- 'data/trade/processed/original/exports.csv'
newsFilePath <- 'data/news/processed/original/newsCounts.csv'

importData <- read_csv(importFilePath)
exportData <- read_csv(exportFilePath)
newsData <- read_csv(newsFilePath)

countryListPath <- 'data/relevantCountries.csv'
countryList <- read_csv(countryListPath)

importShocks <- data.frame(
  CTY_NAME=character(),
  cooks.d=numeric(),
  residual=numeric(),
  shock.event=numeric()
)

exportShocks <- data.frame(
  CTY_NAME=character(),
  cooks.d=numeric(),
  residual=numeric(),
  shock.event=numeric()
)

newsShocks <- data.frame(
  CTY_NAME=character(),
  cooks.d=numeric(),
  residual=numeric(),
  shock.event=numeric()
)

for (countryIdx in 1:nrow(countryList)) {
  countryTradeName <- countryList[countryIdx, ]$name
  countryNewsCode <- countryList[countryIdx, ]$code
  
  print(countryTradeName)
  
  # detecting and recording shocks in imports
  countryImportShocks <- findShocks(importData, countryTradeName) %>%
    cbind(data.frame(
      'CTY_NAME'=rep(countryTradeName, 48)
    ))
  
  importShocks <- importShocks %>%
    rbind(countryImportShocks)
  
  # detecting and recording shocks in exports
  countryExportShocks <- findShocks(exportData, countryTradeName) %>%
    cbind(data.frame(
      'CTY_NAME'=rep(countryTradeName, 48)
    ))
  
  exportShocks <- exportShocks %>%
    rbind(countryExportShocks)
  
  # detecting and recording shocks in news
  countryNewsShocks <- findShocks(newsData, countryTradeName) %>%
    cbind(data.frame(
      'CTY_NAME'=rep(countryTradeName, 48)
    ))
  
  newsShocks <- newsShocks %>%
    rbind(countryNewsShocks)
}

# write all trade shock data to output files
importShockPath <- 'data/trade/processed/original/importShocks.csv'
exportShockPath <- 'data/trade/processed/original/exportShocks.csv'
newsShockPath <- 'data/news/processed/original/newsShocks.csv'

write_csv(importShocks, importShockPath)
write_csv(exportShocks, exportShockPath)
write_csv(newsShocks, newsShockPath)

