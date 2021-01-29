library(tidyverse)
library(ggplot2)
library(igraph)
library(tidygraph)
library(ggraph)
library(circlize)


# working with an edge list with igraph package
data <- read_csv('data/edges2017.csv')
data <- data %>% filter(
  weight > 2000
)

pointAs <- data %>%
  distinct(from) %>%
  rename(label = from)

pointBs <- data %>%
  distinct(to) %>%
  rename(label = to)

nodes <- full_join(pointAs, pointBs, by='label')
nodes <- nodes %>% rowid_to_column('id')

edges <- data %>%
  left_join(nodes, by = c('from' = 'label')) %>%
  rename (source = id)

edges <- edges %>%
  left_join(nodes, by = c('to' = 'label')) %>%
  rename(destination = id)

edges <- select(edges, source, destination, weight)


routes_igraph <- graph_from_data_frame(d = edges, vertices = nodes, directed = FALSE, weighted=TRUE)
plot(routes_igraph)


routes_tidy <- tbl_graph(nodes = nodes, edges = edges, directed = FALSE)
ggraph(routes_tidy) + 
  geom_edge_link(aes(width = weight), alpha = 0.8) +
  scale_edge_width(range = c(0.2, 2)) +
  geom_node_point() + 
  geom_node_text(aes(label = label), repel = TRUE) +
  labs(edge_width = "Number of Articles")
  theme_graph()


# ============================================================================
  
  
# Working with news in the form of matrices

# Returns a matrix for each country connection
networks.getMat <- function(filePath) {
  data <- read.csv(filePath)
  mat <- as.matrix(data)
  countryCodes <- colnames(mat)
  rownames(mat) <- countryCodes
  return(mat)
}

# Returns a data frame with to and from rows for each country connection
networks.getDF <- function(filePath) {
  data <- read.csv(filePath)
  mat <- as.matrix(data)
  countryCodes <- colnames(mat)
  rownames(mat) <- countryCodes
  
  df <- data.frame(from = rep(rownames(mat), times = ncol(mat)),
                        to = rep(colnames(mat), each = nrow(mat)),
                        value = as.vector(mat),
                        stringsAsFactors = FALSE)
  df <- df %>%
    filter(
      !str_detect(from, to) &
        value > 1000
    )
  
  return(df)
}

df_2017 <- networks.getDF('data/matrix2017.csv')
df_2018 <- networks.getDF('data/matrix2018.csv')
df_2019 <- networks.getDF('data/matrix2019.csv')
df_2020 <- networks.getDF('data/matrix2020.csv')

mat_2017 <- networks.getMat('data/matrix2017.csv')

chordDiagram(df_2017)
circos.clear
chordDiagram(df_2017)
circos.clear


