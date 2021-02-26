
# file for residual function models

source('helpers.R')

addTypeCol <- function(data, colTitle, val) {
  
  typeCol <- data.frame(rep(val, nrow(data)))
  colnames(typeCol) <- c(colTitle)
  data <- cbind(data, typeCol)
  
  return (data)
}

getResiduals <- function(data) {
  
  shocks <- shock.id(data$COUNTS)
  shocks <- shocks %>%
    mutate(residual = abs(residual)) %>%
    mutate(cooks.d = replace_na(cooks.d, 0)) %>%
    mutate(shock.event = replace_na(shock.event, 0))
  data <- cbind(data, shocks)
  return(data)
}

getInfo <- function(country) {
  
  exports <- records.getFullCountryExports(country$name)
  exports <- getResiduals(exports)
  exports <- addTypeCol(exports,'TYPE', 'EXPORTS')
  exports$COUNT_PLOT <-exports$residual
  exports$MONTH_IDX <- seq(1, nrow(exports))
  
  imports <- records.getFullCountryImports(country$name)
  imports <- getResiduals(imports)
  imports <- addTypeCol(imports, 'TYPE', 'IMPORTS')
  imports$COUNT_PLOT <-imports$residual
  imports$MONTH_IDX <- seq(1, nrow(imports))
  
  news <- records.getFullCountryNewsCounts(country$code)
  news <- addTypeCol(news, 'CTY_NAME', country$name)
  news <- getResiduals(news)
  news <- addTypeCol(news, 'TYPE', 'NEWS')
  news$COUNT_PLOT <- news$COUNTS
  news$MONTH_IDX <- seq(1, nrow(news))
  
  complete <- rbind(exports, imports, news)
  print(complete)
  
  return(complete)
}

relevantCountries <- read_csv('data/relevantCountries.csv')
country <- relevantCountries[1,]
countryInfo <- getInfo(country)

p <- countryInfo %>%
  ggplot() +
  ggtitle(country$name) +
  geom_line(aes(x=MONTH_IDX, y=COUNT_PLOT)) +
  scale_x_continuous(breaks=seq(1,nrow(countryInfo)/3,by=1)) +
  facet_grid(rows=vars(TYPE), scales='free_y') 

plot(p)

print(nrow(countryInfo))


# Get all residuals for exports