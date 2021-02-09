library(tidyverse)
library(ggplot2)

# Analyzing trades with the US

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
  
  return(countryExportTotal)
}

# Get all news article records for a specific country
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
  
  colnames(monthCounts) <- c('Month', 'Counts', 'Year')
  
  for (newRow in 1:nrow(countryArticles)) {
    idx <- as.integer(countryArticles[newRow, 'month'])
    freq <- as.integer(countryArticles[newRow, 'n'])
    monthCounts[idx, 2] <- freq
  }
  
  return(monthCounts)
}

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


chileNewsCounts <- records.getFullCountryNewsCounts('TH')
pNews <- ggplot(chileNewsCounts, aes(x=Month, y=Counts)) +
  geom_line() +
  scale_x_continuous(breaks=seq(1,48,by=1)) +
  labs(x="Months", y="Article Frequency") +
  facet_wrap(~Year)
plot(pNews)

# chileExports <- records.getFullCountryExports('CHILE')
# p <- ggplot(chileExports, aes(x=MONTH, y=ALL_VAL_MO)) +
#   geom_line() +
#   scale_x_continuous(breaks=seq(1,48,by=1)) +
#   labs(x='Months', y='Export Counts') +
#   facet_wrap(~YEAR)
# plot(p)
