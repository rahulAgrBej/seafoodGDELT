library(tidyverse)
library(ggplot2)
library(lubridate)
library(ngram)

translatedArticles <- read_csv('translatedFullArticleData.csv')
translatedArticles <- translatedArticles %>%
  mutate(date = make_date(year, month, day)) %>%
  mutate(week = strftime(date, format = "%V")) %>%
  filter(
    !(str_detect(domain, "iheart.com$")) &
      !(str_detect(domain, "floridastar.com$")) &
      !(str_detect(domain, "jewishtimes.com$")) &
      !(str_detect(domain, "oyetimes.com$"))) %>% # remove irrelevant sources with high number of hits
  filter(
    lengths(strsplit(title, " ")) > 1) %>%
  mutate(smallTitle = substr(title, start = 1, stop = 30)) %>%
  select(date, week, title, domain) %>%
  distinct()
