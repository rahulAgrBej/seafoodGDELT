library(tidyverse)
library(ggplot2)
library(lubridate)

shock.id <- function(dat, thresh=0.35){
  # dat is your time series data and threshold is the threshold you want for Cook's D (defaulted to 0.35)
  outt <- array(dim=c(length(dat), 3))
  x <- 1:length(dat)
  ll <- lowess(x, dat) # Fits lowess curve (can specify other options for how the curve is estimated and can change the span)
  rr <- as.numeric(dat[order(x)]-ll$y) #residuals off lowess
  rrp1 <- rr[2:length(rr)] # Residuals at time t
  rrm1 <- rr[1:(length(rr)-1)] # Residuals at time t-1
  ll2 <- lm(rrp1~rrm1) # Linear fit of the residuals
  cd <- cooks.distance(ll2) # Calculate the Cook's D
  outt[2:length(rr),1] <- as.numeric(cd) # Output the Cook's D
  outt[,2] <- rr # Output the residuals
  outt[2:length(rr),3] <- ifelse(as.numeric(cd) >= thresh,1,0) # Logical of whether point is a shock
  outt <- as.data.frame(outt)
  colnames(outt) <- c("cooks.d", "residual", "shock.event")
  return(outt)
}


articles.getTable <- function(filePath) {
  articles <- read_csv(filePath)
  articles <- articles %>%
    mutate(date = make_date(year, month, day)) %>%
    mutate(week = strftime(date, format = "%V")) %>%
    filter(
      !(str_detect(domain, "iheart.com$")) &
        !(str_detect(domain, "floridastar.com$")) &
        !(str_detect(domain, "jewishtimes.com$")) &
        !(str_detect(domain, "oyetimes.com$"))) # remove irrelevant sources with high number of hits
  
  articles$week <- as.numeric(articles$week)
  
  return(articles)
}

articles.getTimeSeries <- function(articleTable, startDate, freq) {
  grouped_by_week <- articleTable %>% group_by(week) %>% tally()
  
  zerosFilledIn <- data.frame()
  zerosFilledIn.week <- seq.int(1, 52)
  zerosFilledIn.n <- rep(0, 52)
  zerosFilledIn.n[4] <- 50
  
  for (row in 1:nrow(grouped_by_week)) {
    
    currWeek <- as.integer(grouped_by_week[row, "week"])
    freq <- as.integer(grouped_by_week[row, "n"])
    zerosFilledIn.n[currWeek] <- freq
  }
  
  dataTS <- ts(zerosFilledIn.n, start=startDate, frequency=freq)
  
  return(dataTS)
}

# Getting all the article tables
articles2017 <- articles.getTable("data/US_CH_2017.csv")
articles2018 <- articles.getTable("data/US_CH_2018.csv")
articles2019 <- articles.getTable("data/US_CH_2019.csv")
articles2020 <- articles.getTable("data/US_CH_2020.csv")

# Turning tables into time series
ts2017 <- articles.getTimeSeries(articles2017, 2017, 52)
ts2018 <- articles.getTimeSeries(articles2018, 2018, 52)
ts2019 <- articles.getTimeSeries(articles2019, 2019, 52)
ts2020 <- articles.getTimeSeries(articles2020, 2020, 52)

# Checking for shocks in the yearly time series
shocks2017 <- shock.id(ts2017)
shocks2018 <- shock.id(ts2018)
shocks2019 <- shock.id(ts2019)
shocks2020 <- shock.id(ts2020)

# Creating a time series across multiple years
ts2017_2018 <- ts(c(ts2017, ts2018), start=2017, frequency=52)
ts2017_2019 <- ts(c(ts2017_2018, ts2019), start=2017, frequency=52)
ts2017_2020 <- ts(c(ts2017_2019, ts2020), start=2017, frequency=52)

# Checking for shocks across 2017-2020
shocks2017_2020 <- shock.id(ts2017_2020)
