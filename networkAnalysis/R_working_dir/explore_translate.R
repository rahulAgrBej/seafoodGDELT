library(tidyverse)
library(ggplot2)
library(lubridate)

translatedArticles <- read_csv('translatedFullArticleData.csv')

# lower case all titles
translatedArticles$title = tolower(translatedArticles$title)
translate

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
  filter(
    str_detect(title, "import") |
      str_detect(title, "export") |
      str_detect(title, "trade") |
      str_detect(title, "seafood") |
      str_detect(title, "salmon") |
      str_detect(title, "fish") |
      str_detect(title, "sale") |
      str_detect(title, "chile") |
      str_detect(title, "norw") |
      str_detect(title, "chin") |
      str_detect(title, "japan") |
      str_detect(title, "russia") |
      str_detect(title, "canad") |
      str_detect(title, "american")) %>%
  mutate(smallTitle = substr(title, start = 1, stop = 30)) %>%
  select(date, week, title) %>%
  distinct()

translatedArticles$week <- as.numeric(translatedArticles$week)

g <- ggplot(translatedArticles %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("figs", "Translated_Summary.jpeg"), 
     height = 3, width = 4, units ="in", res = 400)
print(g)
dev.off()

week40 <- translatedArticles %>%
  filter(week == 40)

week43 <- translatedArticles %>%
  filter(week == 43)

week44 <- translatedArticles %>%
  filter(week == 44)

week45 <- translatedArticles %>%
  filter(week == 45)
