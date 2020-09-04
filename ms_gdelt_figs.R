# MS GDELT Figs

# Load packages
library(rjson)
library(tidyverse)
library(ggplot2)
library(lubridate)
library(usmap)
library(geom_map)

# Set map theme
theme_map <- function(...) {
  theme_minimal() +
    theme(
      text = element_text(color = "#22211d"),
      axis.line = element_blank(),
      axis.text.x = element_blank(),
      axis.text.y = element_blank(),
      axis.ticks = element_blank(),
      axis.title.x = element_blank(),
      axis.title.y = element_blank(),
      # panel.grid.minor = element_line(color = "#ebebe5", size = 0.2),
      panel.grid.major = element_line(color = "#ebebe5", size = 0.2),
      panel.grid.minor = element_blank(),
      plot.background = element_rect(fill = "#f5f5f2", color = NA), 
      panel.background = element_rect(fill = "#f5f5f2", color = NA), 
      legend.background = element_rect(fill = "#f5f5f2", color = NA),
      panel.border = element_blank(),
      ...
    )
}

# Load data for all states
state_files <- list.files("COVID-19 US/statesFullArticles")

states <- fromJSON(file = file.path("COVID-19 US", "statesFullArticles", state_files[1]))
states <- data.frame(matrix(unlist(states), nrow=length(states), byrow=T))
colnames(states) <- c("domain", "language", "seendate", "socialimage", "sourcecountry", "title", "url", "url_mobile")
states <- states %>%
  separate(col = seendate, into = c("date", "time"), sep = "T") %>%
  mutate(date = as.Date(date, format = "%Y%m%d"))
states$state <- substr(state_files[1], 1, nchar(state_files[1])-4)

for(i in 2:length(state_files)){
  states_temp <- fromJSON(file = file.path("COVID-19 US", "statesFullArticles", state_files[i]))
  states_temp <- data.frame(matrix(unlist(states_temp), nrow=length(states_temp), byrow=T))
  colnames(states_temp) <- c("domain", "language", "seendate", "socialimage", "sourcecountry", "title", "url", "url_mobile")
  states_temp <- states_temp %>%
    separate(col = seendate, into = c("date", "time"), sep = "T") %>%
    mutate(date = as.Date(date, format = "%Y%m%d"))
  states_temp$state <- substr(state_files[i], 1, nchar(state_files[i])-4)
  
  states <- states %>%
    bind_rows(states_temp)
}

# Convert date/time to date format and select unique titles for each state
states <- states %>%
  mutate(week = strftime(date, format = "%V")) %>%
  filter(!(str_detect(domain, "iheart.com$"))) %>% # remove irrelevant sources with high number of hits
  mutate(title = substr(title, start = 1, stop = 30)) %>%
  select(state, date, week, title) %>%
  distinct() 
states$week <- as.numeric(states$week)

# Map of total articles by state
g <- plot_usmap(data = states %>% group_by(state) %>% tally(), values = "n") + 
  scale_fill_continuous(name = paste("No. articles Jan-Aug")) + 
  theme_map()

jpeg(filename = file.path("COVID-19 US", "figs", "states_total.jpeg"), 
     height = 3, width = 4, units = "in", res = 400)
print(g)
dev.off()

# Summarize counts by month
states$month <- month(states$date)

states_month <- states %>%
  group_by(month, state) %>% 
  filter(month < 9) %>%
  tally()


# Plot monthly state article counts (duplicates of articles cannot be removed)
months <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug")

# Add in zeros for missing states
state_month_list <- c(unique(states$state), "Ohio", "Iowa", "Utah")
state_month_list <- expand_grid(state_month_list, 1:8)
colnames(state_month_list) <- c("state", "month")

states_month <- states_month %>%
  full_join(state_month_list, by = c("month", "state"))
states_month$n[is.na(states_month$n)] <- 0

states_month <- states_month %>% 
  mutate(month = case_when(
    month == 1 ~ "Jan",
    month == 2 ~ "Feb",
    month == 3 ~ "Mar",
    month == 4 ~ "Apr",
    month == 5 ~ "May",
    month == 6 ~ "Jun",
    month == 7 ~ "Jul",
    month == 8 ~ "Aug",
  ))
states_month$month <- factor(states_month$month, levels = months)
g <- plot_usmap(data = states_month, values = "n") + 
  scale_fill_continuous(limits = c(0,800), name = "No. of articles") + 
  theme_map() +
  facet_wrap(~month, ncol = 3) 

jpeg(filename = file.path("COVID-19 US", "figs", paste("states_monthly.jpeg", sep = "")), 
     height = 5, width = 4, units = "in", res = 400)
print(g)
dev.off()

# Total US article time series
# Plot number of articles by day
USdaily <- states %>%
  select(date, week, title) %>%
  distinct() %>%
  group_by(date) %>%
  tally()

g <- ggplot(USdaily, aes(x = date, y = n)) +
  geom_line() +
  labs(y = "Number of Articles", x = "Date") +
  theme_minimal()

jpeg(filename = file.path("COVID-19 US", "figs", paste("US_ts_daily", ".jpeg", sep = "")), 
     height = 3, width = 4, units = "in", res = 400)
print(g)
dev.off()

# Plot number of articles by week
USweekly <- states %>%
  select(date, week, title) %>%
  distinct() %>%
  group_by(week) %>%
  tally()

g <- ggplot(USweekly, aes(x = week, y = n)) +
  geom_line() +
  labs(y = "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("COVID-19 US", "figs", paste("US_ts_weekly", ".jpeg", sep = "")), 
     height = 3, width = 4, units = "in", res = 400)
print(g)
dev.off()

# Interesting peaks:
# Week 4
# Weeks 12-17
# Week 19
# Week 30

