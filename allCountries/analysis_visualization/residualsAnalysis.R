
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

test <- function(country) {
  
  exports <- records.getFullCountryExports(country$name)
  exports <- getResiduals(exports)
  exports <- addTypeCol(exports,'TYPE', 'EXPORTS')
  
  
  
  imports <- records.getFullCountryImports(country$name)
  imports <- getResiduals(imports)
  imports <- addTypeCol(imports, 'TYPE', 'IMPORTS')
  
  
  news <- records.getFullCountryNewsCounts(country$code)
  news <- addTypeCol(news, 'CTY_NAME', country$name)
  news <- getResiduals(news)
  news <- addTypeCol(news, 'TYPE', 'NEWS')
  
  complete <- rbind(exports, imports, news)
  
  return(complete)
}

relevantCountries <- read_csv('data/relevantCountries.csv')
chile <- relevantCountries[1,]
print(test(chile))

# Get all residuals for exports