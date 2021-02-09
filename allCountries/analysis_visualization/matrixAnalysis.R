library(tidyverse)
library(ggplot2)
library(igraph)
library(tidygraph)
library(ggraph)
library(networkD3)
library(circlize)

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
        value > 500
    )
  
  return(df)
}

# working with an edge list with igraph package
data <- read_csv('data/edges2017.csv')
data <- data %>% filter(
  weight > 500
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


routes_igraph <- graph_from_data_frame(d = edges, vertices = nodes, directed = FALSE)
plot(routes_igraph)


routes_tidy <- tbl_graph(nodes = nodes, edges = edges, directed = FALSE)
ggraph(routes_tidy, layout='linear') + 
  geom_edge_link(aes(width = weight), alpha = 0.8) +
  geom_edge_arc() +
  scale_edge_width(range = c(0.2, 2)) +
  geom_node_point() + 
  geom_node_text(aes(label = label), repel = TRUE) +
  labs(edge_width 
       = "Number of Articles")
  theme_graph()

nodes_d3 <- mutate(
  nodes, 
  id = id - 1
  )
edges_d3 <- mutate(
  edges, 
  source = source - 1, 
  destination = destination - 1
  )

forceNetwork(Links = as_tibble(edges_d3), Nodes = (nodes_d3), Source = "source", Target = "destination", 
             NodeID = "label", Group = "id", Value = "weight", 
             opacity = 1, fontSize = 16, zoom = TRUE)

sankeyNetwork(Links = edges_d3, Nodes = nodes_d3, Source = "source", Target = "destination", 
              NodeID = "label", Value = "weight", fontSize = 16, unit = "News Articles")


mat2017 <- networks.getMat('data/matrix2017.csv')
df2017 <- networks.getDF('data/matrix2017.csv')
chordNetwork(Data = mat2017, height = 500, width = 500, initialOpacity = 0.8,
            useTicks = 0, colourScale = c("#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78",
                                          "#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", "#8c564b",
                                          "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f", "#c7c7c7", "#bcbd22", "#dbdb8d",
                                          "#17becf", "#9edae5"), padding = 0.1, fontSize = 14,
            fontFamily = "sans-serif", labels = c(), labelDistance = 30)

# ============================================================================
  
  
# Working with news in the form of matrices





df_2017 <- networks.getDF('data/matrix2017.csv')
df_2018 <- networks.getDF('data/matrix2018.csv')
df_2019 <- networks.getDF('data/matrix2019.csv')
df_2020 <- networks.getDF('data/matrix2020.csv')

mat_2017 <- networks.getMat('data/matrix2017.csv')

hist(df_2017$value, breaks=50)
max(df_2017$value)

chordDiagram(df_2017, reduce=0.02)
circos.clear
chordDiagram(df_2018)
circos.clear
chordDiagram(df_2018)
circos.clear
chordDiagram(df_2018)
circos.clear


