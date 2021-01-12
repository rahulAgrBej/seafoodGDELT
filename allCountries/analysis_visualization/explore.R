library(tidyverse)
library(ggplot2)
library(lubridate)

articles <- read_csv("../summary_US_CH.csv")
articles <- articles %>%
  mutate(date = make_date(year, month, day)) %>%
  mutate(week = strftime(date, format = "%V"))

articles$week <- as.numeric(articles$week)

grouped_by_week <- articles %>% group_by(week) %>% tally()
grouped_by_week


g <- ggplot(articles %>% group_by(week) %>% tally(), aes(x = week,y = n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("figs", "Summary_US_CH_2017.jpeg"), 
     height = 3, width = 4, units ="in", res = 400)
print(g)
dev.off()

