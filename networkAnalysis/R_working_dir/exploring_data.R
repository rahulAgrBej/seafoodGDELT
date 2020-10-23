library(tidyverse)
library(ggplot2)
library(lubridate)

TotalFullArticleData <- read_csv("TotalFullArticleData.csv")
TotalFullArticleData <- TotalFullArticleData %>%
  mutate(date = make_date(year, month, day)) %>%
  mutate(week = strftime(date, format = "%V")) %>%
  filter(!(str_detect(domain, "iheart.com$"))) # remove irrelevant sources with high number of hits

TotalFullArticleData$week <- as.numeric(TotalFullArticleData$week)

# plot everything on a weekly basis
g <- ggplot(TotalFullArticleData %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = "Complete_Summary.jpeg", height = 3, width = 4, units ="in", res = 400)
print(g)
dev.off()


US_CH <- TotalFullArticleData %>%
  filter((str_detect(country1, "US") & str_detect(country2, "CH")))

g1 <- ggplot(US_CH %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = "US_CH.jpeg", height = 3, width = 4, units ="in", res = 400)
print(g1)
dev.off()

CA_CH <- TotalFullArticleData %>%
  filter((str_detect(country1, "CA") & str_detect(country2, "CH")))

g2 <- ggplot(CA_CH %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = "CA_CH.jpeg", height = 3, width = 4, units ="in", res = 400)
print(g2)
dev.off()

NO_CA <- TotalFullArticleData %>%
  filter((str_detect(country1, "NO") & str_detect(country2, "CA")))

g2 <- ggplot(NO_CA %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = "NO_CA.jpeg", height = 3, width = 4, units ="in", res = 400)
print(g2)
dev.off()

NO_CI <- TotalFullArticleData %>%
  filter((str_detect(country1, "NO") & str_detect(country2, "CI")))

g2 <- ggplot(NO_CI %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = "NO_CI.jpeg", height = 3, width = 4, units ="in", res = 400)
print(g2)
dev.off()
