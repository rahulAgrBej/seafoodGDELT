library(tidyverse)
library(ggplot2)
library(lubridate)

articles <- read_csv("summaryTable.csv")
articles <- articles %>%
  mutate(date = make_date(year, month, day)) %>%
  mutate(week = strftime(date, format = "%V"))

articles$week <- as.numeric(articles$week)

g <- ggplot(articles %>% group_by(week) %>% summarise(freq = sum(freq)), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("figs", "summary.jpeg"), 
     height = 3, width = 4, units ="in", res = 400)
print(g)
dev.off()