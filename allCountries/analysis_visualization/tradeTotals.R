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

exports2017 <- trades.cleanExports('data/trades/totals/exports2017.csv')
exports2018 <- trades.cleanExports('data/trades/totals/exports2018.csv')
exports2019 <- trades.cleanExports('data/trades/totals/exports2019.csv')
exports2020 <- trades.cleanExports('data/trades/totals/exports2020.csv')
exportsTotal <- rbind(exports2017, exports2018, exports2019, exports2020)

p <- ggplot(exportsTotal, aes(x = MONTH, y = ALL_VAL_MO)) +
  geom_line() +
  scale_x_continuous(breaks = seq(1, 48, by = 1)) +
  labs(y = 'Trade Quantity', x = 'Month') +
  theme_minimal() +
  facet_wrap(~YEAR)

plot(p)