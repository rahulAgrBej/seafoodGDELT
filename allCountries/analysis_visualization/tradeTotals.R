library(tidyverse)
library(ggplot2)

trades.cleanExports <- function(fp) {
  exports <- read_csv(fp)
  #exports$MONTH <- as.numeric(exports$MONTH)
  exports <- exports %>%
    filter(
      DF == 2
    )
  
  exports <- subset(exports, select = -c(DF))
  exports$MONTH <- as.numeric(exports$MONTH)
  exports$YEAR <- as.numeric(exports$YEAR)
  exports$ALL_VAL_MO <- as.numeric(exports$ALL_VAL_MO)
  return(exports)
}

# Gets monthly count for the US news articles
trades.getNewsCounts <- function(fp, year) {
  news <- read_csv(fp)
  news <- news %>%
    filter(
      str_detect(country1, 'US') | str_detect(country2, 'US')
    ) %>% group_by(month) %>% tally()
  
  monthCounts <- data.frame()
  
  for (row in 1:12) {
    
    monthCounts <- rbind(monthCounts, c(row, 0, year))
  }
  
  colnames(monthCounts) <- c('MONTH', 'COUNTS', 'YEAR')
  
  for (newRow in 1:nrow(news)) {
    idx <- as.integer(news[newRow, 'month'])
    freq <- as.integer(news[newRow, 'n'])
    monthCounts[idx, 2] <- freq
  }
  
  return(monthCounts)
}

news17 <- trades.getNewsCounts('data/summary_table_2017.csv', 2017)
news18 <- trades.getNewsCounts('data/summary_table_2018.csv', 2018)
news19 <- trades.getNewsCounts('data/summary_table_2019.csv', 2019)
news20 <- trades.getNewsCounts('data/summary_table_2020.csv', 2020)
newsTotal <- rbind(news17, news18, news19, news20)
newsRows <- nrow(newsTotal)
newsKindCol <- rep(c('NEWS'), times=newsRows)
newsKindDF <- data.frame(newsKindCol)
colnames(newsKindDF) <- c('KIND')
newsTotal <- cbind(newsTotal, newsKindDF)


exports17 <- trades.cleanExports('data/trades/totals/exports2017.csv')
exports18 <- trades.cleanExports('data/trades/totals/exports2018.csv')
exports19 <- trades.cleanExports('data/trades/totals/exports2019.csv')
exports20 <- trades.cleanExports('data/trades/totals/exports2020.csv')
exportsTotal <- rbind(exports17, exports18, exports19, exports20)
exportsTotal <- subset(exportsTotal, select=-c(COMM_LVL, E_COMMODITY))
colnames(exportsTotal) <- c('COUNTS', 'MONTH', 'YEAR')
tradeRows <- nrow(exportsTotal)
tradeKindCol <- rep(c('TRADE'), times=tradeRows)
tradeKindDF <- data.frame(tradeKindCol)
colnames(tradeKindDF) <- c('KIND')
exportsTotal<- cbind(exportsTotal, tradeKindDF)

p <- ggplot() +
  geom_line(data=exportsTotal, aes(x=MONTH, y=COUNTS), color="blue") +
  geom_line(data=newsTotal, aes(x=MONTH, y=COUNTS), color="red") +
  scale_x_continuous(breaks = seq(1, 48, by = 1)) +
  facet_grid(KIND~YEAR,scales="free_y")
plot(p)
