source('helpers.R')

# Example with Chile
chileExport <- records.getFullCountryExports('CHILE')
tradeRows <- nrow(chileExport)
tradeKindCol <- rep(c('EXPORTS'), times=tradeRows)
tradeKindDF <- data.frame(tradeKindCol)
colnames(tradeKindDF) <- c('KIND')
chileExport <- cbind(chileExport, tradeKindDF)

# Example with Chile
chileImport <- records.getFullCountryImports('CHILE')
tradeRows <- nrow(chileImport)
tradeKindCol <- rep(c('IMPORTS'), times=tradeRows)
tradeKindDF <- data.frame(tradeKindCol)
colnames(tradeKindDF) <- c('KIND')
chileImport <- cbind(chileImport, tradeKindDF)

chileNews <- records.getFullCountryNewsCounts('CI')
newsRows <- nrow(chileNews)
newsKindCol <- rep(c('NEWS'), times=newsRows)
newsKindDF <- data.frame(newsKindCol)
colnames(newsKindDF) <- c('KIND')
chileNews <- cbind(chileNews, newsKindDF)

p <- ggplot() +
  geom_line(data=chileNews, aes(MONTH, COUNTS), color="red") +
  geom_line(data=chileExport, aes(MONTH, COUNTS), color="blue") +
  geom_line(data=chileImport, aes(MONTH, COUNTS), color="black") +
  scale_x_continuous(breaks=seq(1,48,by=1)) +
  facet_grid(KIND~YEAR,scales="free_y")
plot(p)