library(tidyverse)
library(ggplot2)
library(circlize)


# Working with news in the form of matrices

data2017 <- read.csv('data/matrix2017.csv')
mat2017 <- as.matrix(data2017)
countryCodes <- colnames(mat2017)
rownames(mat2017) <- countryCodes

df <- data.frame(from = rep(rownames(mat2017), times = ncol(mat2017)),
                 to = rep(colnames(mat2017), each = nrow(mat2017)),
                 value = as.vector(mat2017),
                 stringsAsFactors = FALSE)
df <- df %>%
  filter(
    !str_detect(from, to) &
      value > 1000
  )

chordDiagram(df)