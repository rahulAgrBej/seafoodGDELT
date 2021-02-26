library(tidyverse)
library(ggplot2)
library(dplyr)

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

# Clean trade data to a specific country's exports
records.getCountryExports <- function(fp, country) {
  
  countryTrades <- read_csv(fp)
  countryTrades <- countryTrades %>%
    filter(
      str_detect(CTY_NAME, country)
    )
  
  countryTrades$MONTH <- as.numeric(countryTrades$MONTH)
  countryTrades$YEAR <- as.numeric(countryTrades$YEAR)
  countryTrades$ALL_VAL_MO <- as.numeric(countryTrades$ALL_VAL_MO)
  countryTrades <- subset(countryTrades, select=-c(CTY_CODE, SUMMARY_LVL, COMM_LVL, E_COMMODITY))
  
  return(countryTrades)
}

# Clean trade data to a specific country's exports
records.getCountryImports <- function(fp, country) {
  
  countryTrades <- read_csv(fp)
  countryTrades <- countryTrades %>%
    filter(
      str_detect(CTY_NAME, country)
    )
  
  countryTrades$MONTH <- as.numeric(countryTrades$MONTH)
  countryTrades$YEAR <- as.numeric(countryTrades$YEAR)
  countryTrades$GEN_VAL_MO <- as.numeric(countryTrades$GEN_VAL_MO)
  countryTrades <- subset(countryTrades, select=-c(CTY_CODE, SUMMARY_LVL, COMM_LVL, I_COMMODITY))
  
  return(countryTrades)
}

# Get all export records for a specific country
records.getFullCountryExports <- function(country) {
  fp17 <- 'data/trades/countries/exportCountries2017.csv'
  fp18 <- 'data/trades/countries/exportCountries2018.csv'
  fp19 <- 'data/trades/countries/exportCountries2019.csv'
  fp20 <- 'data/trades/countries/exportCountries2020.csv'
  countryExport17 <- records.getCountryExports(fp17, country)
  countryExport18 <- records.getCountryExports(fp18, country)
  countryExport19 <- records.getCountryExports(fp19, country)
  countryExport20 <- records.getCountryExports(fp20, country)
  countryExportTotal <- rbind(countryExport17, countryExport18, countryExport19, countryExport20)
  
  colnames(countryExportTotal) <- c('CTY_NAME', 'COUNTS', 'MONTH', 'YEAR')
  
  return(countryExportTotal)
}

# Get all export records for a specific country
records.getFullCountryImports <- function(country) {
  fp17 <- 'data/trades/countries/importCountries2017.csv'
  fp18 <- 'data/trades/countries/importCountries2018.csv'
  fp19 <- 'data/trades/countries/importCountries2019.csv'
  fp20 <- 'data/trades/countries/importCountries2020.csv'
  countryImport17 <- records.getCountryImports(fp17, country)
  countryImport18 <- records.getCountryImports(fp18, country)
  countryImport19 <- records.getCountryImports(fp19, country)
  countryImport20 <- records.getCountryImports(fp20, country)
  countryImportTotal <- rbind(countryImport17, countryImport18, countryImport19, countryImport20)
  
  colnames(countryImportTotal) <- c('CTY_NAME', 'COUNTS', 'MONTH', 'YEAR')
  
  return(countryImportTotal)
}

# Get all news article records for a specific country fo a specific year
records.getCountryNewsCounts <- function(fp, country, year) {
  countryArticles <- read_csv(fp)
  countryArticles <- countryArticles %>%
    filter(
      (str_detect(country1, 'US') & str_detect(country2, country)) |
        (str_detect(country1, country) & str_detect(country2, 'US'))
    ) %>% group_by(month) %>% tally()
  
  monthCounts <- data.frame()
  
  for (row in 1:12) {
    
    monthCounts <- rbind(monthCounts, c(row, 0, year))
  }
  
  colnames(monthCounts) <- c('MONTH', 'COUNTS', 'YEAR')
  
  for (newRow in 1:nrow(countryArticles)) {
    idx <- as.integer(countryArticles[newRow, 'month'])
    freq <- as.integer(countryArticles[newRow, 'n'])
    monthCounts[idx, 2] <- freq
  }
  
  return(monthCounts)
}

# Gets news article records for 2017-2020 for a specific country
records.getFullCountryNewsCounts <- function(country) {
  fp17 <- 'data/summary_table_2017.csv'
  fp18 <- 'data/summary_table_2018.csv'
  fp19 <- 'data/summary_table_2019.csv'
  fp20 <- 'data/summary_table_2020.csv'
  countryNewsCounts17 <- records.getCountryNewsCounts(fp17, country, 2017)
  countryNewsCounts18 <- records.getCountryNewsCounts(fp18, country, 2018)
  countryNewsCounts19 <- records.getCountryNewsCounts(fp19, country, 2019)
  countryNewsCounts20 <- records.getCountryNewsCounts(fp20, country, 2020)
  countryNewsCounts <- rbind(countryNewsCounts17, countryNewsCounts18, countryNewsCounts19, countryNewsCounts20)
  
  return(countryNewsCounts)
}

completeData <- function(data, kind) {
  tradeRows <- nrow(data)
  tradeKindCol <- rep(c(kind), times=tradeRows)
  tradeKindDF <- data.frame(tradeKindCol)
  colnames(tradeKindDF) <- c('KIND')
  data <- cbind(data, tradeKindDF)
  shocks <- shock.id(data$COUNT)
  shocks <- data.frame(shocks$shock.event)
  colnames(shocks) <- c('SHOCK')
  data <- cbind(data, shocks)
  data$MONTH <- seq(1,48)
  data <- subset(data, select=c('MONTH', 'COUNTS', 'KIND', 'SHOCK'))
  
  return(data)
}

tradeNewsPlots <- function(countryName, countryCode) {
  # Example with data
  dataExport <- records.getFullCountryExports(countryName)
  dataExport <- completeData(dataExport, 'EXPORTS')
  
  # Example with data
  dataImport <- records.getFullCountryImports(countryName)
  dataImport <- completeData(dataImport, 'IMPORTS')
  
  dataNews <- records.getFullCountryNewsCounts(countryCode)
  dataNews <- completeData(dataNews, 'NEWS')
  
  dataComplete <- rbind(dataNews, dataImport, dataExport)
  
  exportShocks = which(subset(dataComplete, KIND=='EXPORTS')$SHOCK == 1)
  importShocks = which(subset(dataComplete, KIND=='IMPORTS')$SHOCK == 1)
  newsShocks = which(subset(dataComplete, KIND=='NEWS')$SHOCK == 1)
  
  p <- ggplot() +
    ggtitle(countryName) +
    facet_grid(rows=vars(KIND), scales='free_y') +
    scale_x_continuous(breaks=seq(1,48,by=1)) +
    geom_line(data=subset(dataComplete, KIND='NEWS'), aes(MONTH, COUNTS), color='red') +
    geom_line(data=subset(dataComplete, KIND='EXPORTS'), aes(MONTH, COUNTS), color='blue') +
    geom_line(data=subset(dataComplete, KIND='IMPORTS'), aes(MONTH, COUNTS), color='black') +
    geom_vline(xintercept=newsShocks, color='blue') +
    geom_vline(xintercept=exportShocks, color='green') +
    geom_vline(xintercept=importShocks, color='red', linetype='dotted')
    
  return(p)
}

shocksImports <- function(countryName) {
  imports <- records.getFullCountryImports(countryName)
  shocks <- shock.id(imports$COUNTS)
  monthIdx <- seq(1,48)
  final <- cbind(monthIdx, imports$COUNTS, shocks$shock.event)
  colnames(final) <- c('MONTH', 'COUNT', 'SHOCK')
  final <- data.frame(final)
  return(final)
}

shocksExports <- function(countryName) {
  exports <- records.getFullCountryExports(countryName)
  shocks <- shock.id(exports$COUNTS)
  monthIdx <- seq(1,48)
  final <- cbind(monthIdx, exports$COUNTS, shocks$shock.event)
  colnames(final) <- c('MONTH', 'COUNT', 'SHOCK')
  final <- data.frame(final)
  return(final)
}

shockPlots <- function(data, title) {
  p <- ggplot() +
    ggtitle(title) +
    geom_line(data=data, aes(MONTH, COUNT)) +
    geom_vline(xintercept=which(data$SHOCK == 1), color='red')
  
  return(p)
}
