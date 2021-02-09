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

chileExports <- records.getFullCountryExports('CHILE')
p <- ggplot(chileExports, aes(x=MONTH, y=ALL_VAL_MO)) +
  geom_line() +
  scale_x_continuous(breaks=seq(1,48,by=1)) +
  labs(x='Months', y='Export Counts') +
  facet_wrap(~YEAR)
plot(p)
