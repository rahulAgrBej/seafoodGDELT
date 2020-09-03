# Data exploration

# Load packages
library(rjson)
library(tidyverse)
library(ggplot2)
library(lubridate)
library(usmap)

# Load US-wide data json file
US <- fromJSON(file = "COVID-19 US/fullArticleData.txt")

# Convert json to dataframe
US <- data.frame(matrix(unlist(US), nrow=length(US), byrow=T))
colnames(US) <- c("domain", "language", "seendate", "socialimage", "sourcecountry", "title", "url", "url_mobile")

# Convert date/time to date format and select unique titles
US <- US %>%
  separate(col = seendate, into = c("date", "time"), sep = "T") %>%
  mutate(date = as.Date(date, format = "%Y%m%d")) %>%
  mutate(week = strftime(date, format = "%V")) %>%
  filter(!(str_detect(domain, "iheart.com$"))) %>% # remove irrelevant sources with high number of hits
  mutate(title = substr(title, start = 1, stop = 30)) %>%
  select(date, week, title) %>%
  distinct() 

US$week <- as.numeric(US$week)

# Plot number of articles by day
g <- ggplot(US %>% group_by(date) %>% tally(), aes(x = date, y = n)) +
  geom_line() +
  labs(y = "Number of Articles", x = "Date") +
  theme_minimal()

jpeg(filename = file.path("COVID-19 US", "figs", paste("US_ts_daily", ".jpeg", sep = "")), 
     height = 3, width = 4, units = "in", res = 400)
print(g)
dev.off()

# Plot number of articles by week
g <- ggplot(US %>% group_by(week) %>% tally(), aes(x = week, y = n)) +
  geom_line() +
  labs(y = "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("COVID-19 US", "figs", paste("US_ts_weekly", ".jpeg", sep = "")), 
       height = 3, width = 4, units = "in", res = 400)
print(g)
dev.off()

# Load states data and create single dataframe for all states
state_files <- list.files("COVID-19 US/statesDateCounts")

states <- fromJSON(file = file.path("COVID-19 US", "statesDateCounts", state_files[1]))
states <- data.frame(matrix(unlist(states), nrow=length(states), byrow=T))
colnames(states) <- c("date", "norm", "value")
states <- states %>%
  separate(col = date, into = c("date", "time"), sep = "T") %>%
  mutate(date = as.Date(date, format = "%Y%m%d"))
states$state <- substr(state_files[1], 1, nchar(state_files[1])-11)
  
for(i in 2:length(state_files)){
  states_temp <- fromJSON(file = file.path("COVID-19 US", "statesDateCounts", state_files[i]))
  states_temp <- data.frame(matrix(unlist(states_temp), nrow=length(states_temp), byrow=T))
  colnames(states_temp) <- c("date", "norm", "value")
  states_temp <- states_temp %>%
    separate(col = date, into = c("date", "time"), sep = "T") %>%
    mutate(date = as.Date(date, format = "%Y%m%d"))
  states_temp$state <- substr(state_files[i], 1, nchar(state_files[i])-11)
  
  states <- states %>%
    bind_rows(states_temp)
}

# Summarize counts by month
states$month <- month(states$date)
states$value <- as.numeric(as.character(states$value))
states$norm <- as.numeric(as.character(states$norm))

states_month <- states %>%
  group_by(month, state) %>%
  summarise(month_count = sum(value))

# Plot monthly state article counts (duplicates of articles cannot be removed)
months <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug")

for(i in 1:length(months)){
  g <-   plot_usmap(data = states_month %>% filter(month == i), values = "month_count") + 
    scale_fill_continuous(name = paste("No. articles in", months[i])) + 
    theme(legend.position = "right")
  jpeg(filename = file.path("COVID-19 US", "figs", paste("states_", months[i], ".jpeg", sep = "")), 
       height = 3, width = 4, units = "in", res = 400)
  print(g)
  dev.off()
}

# Normalize time series for US-wide article counts
df_norm <- states %>% 
  select(date, norm) %>%
  mutate(week = strftime(date, format = "%V")) %>%
  distinct()
df_norm$week <- as.numeric(df_norm$week)

# Plot normalized daily ts
g <- ggplot(US %>% group_by(date) %>% tally() %>%
              left_join(df_norm, by = "date") %>%
              mutate(count_norm = n/norm), 
            aes(x = date, y = count_norm)) +
  geom_line() +
  labs(y = "Number of Articles", x = "Date") +
  theme_minimal()
g

# Plot normalized weekly ts
df_norm_week <- df_norm %>%
  group_by(week) %>%
  summarise(norm = sum(norm))

g <- ggplot(US %>% group_by(week) %>% tally() %>%
              left_join(df_norm_week, by = "week") %>%
              mutate(count_norm = n/norm), 
            aes(x = week, y = count_norm)) +
  geom_line() +
  labs(y = "Number of Articles", x = "Date") +
  theme_minimal()
g

# Evaluate article titles during peaks
US %>% 
  group_by(week) %>% 
  tally() %>%
  arrange(-n)

# Top 10 weeks: 4-5, 12-13, 26-31
themes_1 <- US %>%
  filter(week %in% 4:5) %>%
  select(title) %>%
  distinct() %>%
  arrange(title)
# Weeks 4-5 (Jan 19-Feb 1) - Initial spread and outbreak, trade disruptions

themes_2 <- US %>%
  filter(week %in% 12:13) %>%
  select(title) %>%
  distinct() %>%
  arrange(title)
# Weeks 12-13 (Mar 17-27) - restaurant closures, relief bill

themes_3 <- US %>%
  filter(week %in% 26:31) %>%
  select(title) %>%
  distinct() %>%
  arrange(title)
# Weeks 26-31 (Jun 26- Aug 1) - unemployment, lobster prices (and EO for lobsters), and broader economic damage
