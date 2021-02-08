library(tidyverse)
library(ggplot2)
library(cowplot)

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

exports2017 <- trades.cleanExports('data/trades/exports2017.csv')
exports2018 <- trades.cleanExports('data/trades/exports2018.csv')
exports2019 <- trades.cleanExports('data/trades/exports2019.csv')
exports2020 <- trades.cleanExports('data/trades/exports2020.csv')

p17 <- ggplot(exports2017, aes(x = MONTH, y = ALL_VAL_MO)) +
  geom_line() +
  labs(y = 'Trade Quantity', x = 'Month') +
  theme_minimal()

p18 <- ggplot(exports2018, aes(x = MONTH, y = ALL_VAL_MO)) +
  geom_line() +
  labs(y = 'Trade Quantity', x = 'Month') +
  theme_minimal()

p19 <- ggplot(exports2019, aes(x = MONTH, y = ALL_VAL_MO)) +
  geom_line() +
  labs(y = 'Trade Quantity', x = 'Month') +
  theme_minimal()

p20 <- ggplot(exports2020, aes(x = MONTH, y = ALL_VAL_MO)) +
  geom_line() +
  labs(y = 'Trade Quantity', x = 'Month') +
  theme_minimal()

plot_grid(p17, p18, p19, p20)

