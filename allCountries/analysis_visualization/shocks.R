
library(tidyverse)
library(ggplot2)
library(dplyr)

source('helpers.R')


# Top seafood trade partners with the US, Canada, China, Norway, Chile Japan,
importsCA <- shocksImports('CANADA')
plot(shockPlots(importsCA, 'Canada Imports'))
exportsCA <- shocksExports('CANADA')
plot(shockPlots(exportsCA, 'Canada Exports'))

importsCH <- shocksImports('CHINA')
plot(shockPlots(importsCH, 'China Imports'))
exportsCH <- shocksExports('CHINA')
plot(shockPlots(exportsCH, 'China Exports'))

importsCI <- shocksImports('CHILE')
plot(shockPlots(importsCI, 'Chile Imports'))
exportsCI <- shocksExports('CHILE')
plot(shockPlots(exportsCI, 'Chile Exports'))

importsNO <- shocksImports('NORWAY')
plot(shockPlots(importsNO, 'Norway Imports'))
exportsNO <- shocksExports('NORWAY')
plot(shockPlots(exportsNO, 'Norway Exports'))

importsJA <- shocksImports('JAPAN')
plot(shockPlots(importsJA, 'Japan Imports'))
exportsJA <- shocksExports('JAPAN')
plot(shockPlots(exportsJA, 'Japan Exports'))

importsVT <- shocksImports('VIETNAM')
plot(shockPlots(importsVT, 'Vietnam Imports'))
exportsVT <- shocksExports('VIETNAM')
plot(shockPlots(exportsVT, 'Vietnam Exports'))

