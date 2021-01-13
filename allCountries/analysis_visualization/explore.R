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

shocks <- shock.id(dataTS)

g <- ggplot(zerosFilledIn, aes(x = zerosFilledIn.week,y = zerosFilledIn.n)) +
  geom_line() +
  labs(y= "Number of Articles", x = "Week") +
  theme_minimal()

jpeg(filename = file.path("figs", "Summary_US_CH_2017.jpeg"), 
     height = 3, width = 4, units ="in", res = 400)
print(g)
dev.off()

