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

articles.getTimeSeries <- function(articleTable) {
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
  
  dataTS <- ts(zerosFilledIn.n)
  
  return(dataTS)
}

articles2017 <- articles.getTable("../summary_US_CH.csv")
articles2018 <- articles.getTable("../summary_US_CH_2018.csv")
articles2019 <- articles.getTable("../summary_US_CH_2019.csv")

ts2017 <- articles.getTimeSeries(articles2017)
ts2018 <- articles.getTimeSeries(articles2018)
ts2019 <- articles.getTimeSeries(articles2019)

shocks2017 <- shock.id(ts2017)
shocks2018 <- shock.id(ts2018)
shocks2019 <- shock.id(ts2019)

g <- ggplot(zerosFilledIn, aes(x = zerosFilledIn.week,y = zerosFilledIn.n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("figs", "Summary_US_CH_2017.jpeg"), 
     height = 3, width = 4, units ="in", res = 400)
print(g)
dev.off()

