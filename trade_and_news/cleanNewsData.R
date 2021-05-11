
library(tidyverse)

# Get news articles

newsArticleFiles <- data.frame(
  filePath = c(
    'data/news/summary_table_2017.csv',
    'data/news/summary_table_2018.csv',
    'data/news/summary_table_2019.csv',
    'data/news/summary_table_2020.csv'
  )
)

print(nrow(newsArticleFiles))

newsArticles <- data.frame(
  country1=character(),
  country2=character(),
  sourceCountry=character(),
  year=numeric(),
  month=numeric(),
  day=numeric(),
  domain=character(),
  title=character(),
  url=character()
)

for (newsFileIdx in 1:nrow(newsArticleFiles)) {
  currNewsPath <- newsArticleFiles[newsFileIdx, ]
  print(currNewsPath)
  currNewsFile <- read_csv(currNewsPath)
  newsArticles <- newsArticles %>%
    rbind(currNewsFile)
}

# cleaning and counting news

# filtering news to only include connections with the US
newsArticles <- newsArticles %>%
  filter(str_detect(country1, 'US') | str_detect(country2, 'US'))

newsC1 <- newsArticles %>%
  filter(str_detect(country1, 'US')) %>%
  select(-c(country1)) %>%
  rename(CTY_NAME=country2, YEAR=year, MONTH=month, DAY=day)

newsC2 <- newsArticles %>%
  filter(str_detect(country2, 'US')) %>%
  select(-c(country2)) %>%
  rename(CTY_NAME=country1, YEAR=year, MONTH=month, DAY=day)

news <- newsC1 %>%
  rbind(newsC2)

newsPath <- 'data/news/processed/original/completeNews.csv'
write_csv(news, newsPath)

countryCodeNameLookupPath <- 'data/relevantCountries.csv'
countryCodeNameLookup <- read_csv(countryCodeNameLookupPath) %>%
  rename(CTY_NAME=name)

countryFillerPath <- 'data/countryFiller.csv'
countryFiller <- read_csv(countryFillerPath)

newsCounts <- news %>%
  group_by(CTY_NAME, YEAR, MONTH) %>%
  summarize(TOTAL = n()) %>%
  rename(code=CTY_NAME) %>%
  left_join(countryCodeNameLookup) %>%
  ungroup() %>%
  select(-c(code)) %>%
  right_join(countryFiller) %>%
  mutate(TOTAL = replace_na(TOTAL, 0)) %>%
  arrange(CTY_NAME, YEAR) %>%
  cbind(data.frame(
    'MONTH_IDX'=rep(seq(1,48), nrow(countryCodeNameLookup))))

newsCountsPath <- 'data/news/processed/original/newsCounts.csv'
write_csv(newsCounts, newsCountsPath)

