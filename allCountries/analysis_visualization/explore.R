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
  articles$month <- as.numeric(articles$month)
  
  return(articles)
}

articles.getTimeSeries <- function(articleTable, startDate, freq) {
  
  if (freq == 52) {
    grouped_data <- articleTable %>% group_by(week) %>% tally()
  } else if (freq == 12) {
    grouped_data <- articleTable %>% group_by(month) %>% tally()
  }
  
  zerosFilledIn <- data.frame()
  zerosFilledIn.date <- seq.int(1, freq)
  zerosFilledIn.n <- rep(0, freq)
  
  for (row in 1:nrow(grouped_data)) {
    
    if (freq == 52) {
      currDate <- as.integer(grouped_data[row, "week"])
    } else if (freq == 12) {
      currDate <- as.integer(grouped_data[row, "month"])
    }
    
    freqN <- as.integer(grouped_data[row, "n"])
    zerosFilledIn.n[currDate] <- freqN
  }
  
  dataTS <- ts(zerosFilledIn.n, start=startDate, frequency=freq)
  
  return(dataTS)
}

# Getting all the article tables
articles2017 <- articles.getTable("data/US_CH_2017.csv")
articles2018 <- articles.getTable("data/US_CH_2018.csv")
articles2019 <- articles.getTable("data/US_CH_2019.csv")
articles2020 <- articles.getTable("data/US_CH_2020.csv")

# Frequency for time series
freq_week <- 52
freq_month <- 12

# Turning tables into time series divided by week
ts2017_weeks <- articles.getTimeSeries(articles2017, 2017, freq_week)
ts2018_weeks <- articles.getTimeSeries(articles2018, 2018, freq_week)
ts2019_weeks <- articles.getTimeSeries(articles2019, 2019, freq_week)
ts2020_weeks <- articles.getTimeSeries(articles2020, 2020, freq_week)

# Turning tables into time series divided by month
ts2017_months <- articles.getTimeSeries(articles2017, 2017, freq_month)
ts2018_months <- articles.getTimeSeries(articles2018, 2018, freq_month)
ts2019_months <- articles.getTimeSeries(articles2019, 2019, freq_month)
ts2020_months <- articles.getTimeSeries(articles2020, 2020, freq_month)

# Cook's D thresholds
cooks_d_thresh_week <- 0.077
cooks_d_thresh_month <- 0.333

# Checking for shocks in the yearly time series (divided by week)
shocks2017_weeks <- shock.id(ts2017_weeks, thresh=cooks_d_thresh_week)
shocks2018_weeks <- shock.id(ts2018_weeks, thresh=cooks_d_thresh_week)
shocks2019_weeks <- shock.id(ts2019_weeks, thresh=cooks_d_thresh_week)
shocks2020_weeks <- shock.id(ts2020_weeks, thresh=cooks_d_thresh_week)

# Checking for shocks in the yearly time series (divided by month)
shocks2017_months <- shock.id(ts2017_months, thresh=cooks_d_thresh_month)
shocks2018_months <- shock.id(ts2018_months, thresh=cooks_d_thresh_month)
shocks2019_months <- shock.id(ts2019_months, thresh=cooks_d_thresh_month)
shocks2020_months <- shock.id(ts2020_months, thresh=cooks_d_thresh_month)

# Creating a time series across multiple years (divided by week)
ts2017_2018_weeks <- ts(c(ts2017_weeks, ts2018_weeks), start=2017, frequency=freq_week)
ts2017_2019_weeks <- ts(c(ts2017_2018_weeks, ts2019_weeks), start=2017, frequency=freq_week)
ts2017_2020_weeks <- ts(c(ts2017_2019_weeks, ts2020_weeks), start=2017, frequency=freq_week)

# Creating a time series across multiple years (divided by month)
ts2017_2018_months <- ts(c(ts2017_weeks, ts2018_weeks), start=2017, frequency=freq_month)
ts2017_2019_months <- ts(c(ts2017_2018_weeks, ts2019_weeks), start=2017, frequency=freq_month)
ts2017_2020_months <- ts(c(ts2017_2019_weeks, ts2020_weeks), start=2017, frequency=freq_month)

# Checking for shocks across 2017-2020 (divided by WEEK)
multiyear_week_thresh <- 4 / (4 * 52)
shocks2017_2020_weeks <- shock.id(ts2017_2020_weeks, thresh=multiyear_week_thresh)

# Checking for shocks across 2017-2020 (divided by MONTH)
multiyear_month_thresh <- 4 / (4 * 12)
shocks2017_2020_months <- shock.id(ts2017_2020_months, thresh=multiyear_month_thresh)
