# Data exploration

# Load packages
library(rjson)
library(tidyverse)
library(ggplot2)

# Load US-wide data
US <- fromJSON(file = "COVID-19 US/fullArticleData.txt")

US <- data.frame(matrix(unlist(US), nrow=length(US), byrow=T))
colnames(US) <- c("domain", "language", "seendate", "socialimage", "sourcecountry", "title", "url", "url_mobile")
US <- US %>%
  separate(col = seendate, into = c("date", "time"), sep = "T") %>%
  mutate(date = as.Date(date, format = "%Y%m%d")) %>%
  select(date, title) %>%
  distinct() 

ggplot(US %>% group_by(date) %>% tally(), aes(x = date, y = n)) +
  geom_line()

# Load states data (need to )
states <- fromJSON(file = "COVID-19 US/statesDateCounts/Alaska Counts.txt")
states <- data.frame(matrix(unlist(states), nrow=length(states), byrow=T))
colnames(states) <- c("date", "norm", "value")
states <- states %>%
  separate(col = date, into = c("date", "time"), sep = "T") %>%
  mutate(date = as.Date(date, format = "%Y%m%d"))
