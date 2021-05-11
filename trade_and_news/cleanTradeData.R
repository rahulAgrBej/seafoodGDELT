
library(tidyverse)

countryCodeNameLookupPath <- 'data/relevantCountries.csv'
countryCodeNameLookup <- read_csv(countryCodeNameLookupPath) %>%
  rename(CTY_NAME=name)

# constructing filler table with all countries, all months and all years
completeCountries <- read_csv('data/relevantCountries.csv') %>%
  select(name) %>%
  rename(CTY_NAME = name)


yearStart <- 2017
fullMonths <- data.frame(
  'MONTH' = seq(1, 12),
  'YEAR' = rep(yearStart)
)

for (yearIdx in 1:3) {
  fullMonths <- fullMonths %>%
    rbind(data.frame(
      'MONTH' = seq(1,12),
      'YEAR' = rep(yearStart + yearIdx, 12)
    ))
}

completeCountries <- completeCountries %>%
  crossing(fullMonths)

completeCountriesRefPath <- 'data/countryFiller.csv'
write_csv(completeCountries, completeCountriesRefPath)


# input files for imports and exports
importsFilePath <- "data/trade/level_hs_10/imports.csv"
exportsFilePath <- "data/trade/level_hs_10/exports.csv"

# IMPORTS=========================================================================
# cleaning import data
importData <- read_csv(importsFilePath)
importData <- importData %>%
  select(CTY_CODE, CTY_NAME, CON_QY1_MO, MONTH, SUMMARY_LVL, I_COMMODITY, YEAR) %>%
  filter(str_detect(SUMMARY_LVL, 'DET')) %>%
  filter(!str_detect(CTY_CODE, '-')) %>%
  select(CTY_CODE, CTY_NAME, CON_QY1_MO, MONTH, I_COMMODITY, YEAR) %>%
  rename(QUANTITY = CON_QY1_MO, HS_CODE = I_COMMODITY) %>%
  mutate(MONTH = as.numeric(MONTH))

# make sure to have an entry for every country, every month, every year
importData <- importData %>%
  right_join(completeCountries)

# aggregate all trade fro all codes into one total value per month per country
importData <- importData %>%
  group_by(CTY_NAME, MONTH, YEAR) %>%
  summarize(TOTAL = sum(QUANTITY)) %>%
  mutate(TOTAL = replace_na(TOTAL, 0)) %>%
  arrange(CTY_NAME, YEAR) %>%
  cbind(data.frame(
    'MONTH_IDX'=rep(seq(1,48), nrow(countryCodeNameLookup))))

# EXPORTS=========================================================================
exportData <- read_csv(exportsFilePath)
exportData <- exportData %>%
  select(CTY_CODE, CTY_NAME, QTY_1_MO, DF, MONTH, SUMMARY_LVL, E_COMMODITY, YEAR) %>%
  filter(str_detect(SUMMARY_LVL, 'DET')) %>%
  filter(!str_detect(CTY_CODE, '-')) %>%
  filter(str_detect(DF, '-')) %>%
  select(CTY_CODE, CTY_NAME, QTY_1_MO, MONTH, E_COMMODITY, YEAR) %>%
  rename(QUANTITY = QTY_1_MO, HS_CODE = E_COMMODITY) %>%
  mutate(MONTH = as.numeric(MONTH))

# make sure to have an entry for every country, month and year
exportData <- exportData %>%
  right_join(completeCountries)

# aggregate all trade for all codes into one total value per month per country
exportData <- exportData %>%
  group_by(CTY_NAME, MONTH, YEAR) %>%
  summarize(TOTAL = sum(QUANTITY)) %>%
  mutate(TOTAL = replace_na(TOTAL, 0)) %>%
  arrange(CTY_NAME, YEAR) %>%
  cbind(data.frame(
    'MONTH_IDX'=rep(seq(1,48), nrow(countryCodeNameLookup))))

# WRITES INFO TO SEPARATE FILES FOR REFERENCE LATER
importsOutPath <- 'data/trade/processed/original/imports.csv'
exportsOutPath <- 'data/trade/processed/original/exports.csv'

write_csv(importData, importsOutPath)
write_csv(exportData, exportsOutPath)