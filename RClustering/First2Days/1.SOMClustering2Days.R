library("kohonen")
library("tibble")
library("magrittr")
library("dplyr")
library("tidyverse")
library("factoextra")
library("RColorBrewer")
library("NbClust")

rm(list=ls())



darkPalette <- brewer.pal(8, "Dark2")


Modes <- function(x) {
  ux <- unique(x)
  tab <- tabulate(match(x, ux))
  ux[tab == max(tab)]
}


################################1. Read data file
patient.data = read.csv(file='/Users/babylon/Documents/Data/KCHData/ClusteringData/BaselineAndDeltaObs.csv')
patient.data[,"SymptomsToAdmission"] <- as.numeric(substr(patient.data[,"SxToAdmit"], 1, regexpr(' day',patient.data[,"SxToAdmit"])))

#patient.data<-patient.data[!(patient.data$PatientID=='p_50'),]
#patient.data<-patient.data[patient.data$SymptomsToAdmission>= 0 ,]


colnames(patient.data) = make.names(names(patient.data))
patient.data[,-c(1)] <- mutate_all(patient.data[,-c(1)], function(x) as.numeric(as.character(x)))

clustering.columns = c("NEWSBaseline" , "CReactiveProteinBaseline", "SysBPBaseline", "DiasBPBaseline", "WBCBaseline" , "LymphocytesBaseline" , "NeutrophilsBaseline", "PLTBaseline" , "UreaBaseline", "CreatinineBaseline" , "HbBaseline" , "AlbuminBaseline" , "DeltaNEWS",  "DeltaCReactiveProtein"   ,"DeltaSysBP" ,  "DeltaDiasBP" ,  "DeltaWBC" , "DeltaLymphocytes" , "DeltaNeutrophils",  "DeltaPLT" , "DeltaUrea" , "DeltaCreatinine",  "DeltaHb", "DeltaAlbumin")

unscaled.colnames = c("NEWSBaseline_unscaled","CReactiveProteinBaseline_unscaled", "SysBPBaseline_unscaled", "DiasBPBaseline_unscaled", "WBCBaseline_unscaled","LymphocytesBaseline_unscaled","NeutrophilsBaseline_unscaled", "PLTBaseline_unscaled","UreaBaseline_unscaled", "CreatinineBaseline_unscaled","HbBaseline_unscaled","AlbuminBaseline_unscaled","DeltaNEWS_unscaled",  "DeltaCReactiveProtein_unscaled"   ,"DeltaSysBP_unscaled" ,  "DeltaDiasBP_unscaled" ,  "DeltaWBC_unscaled","DeltaLymphocytes_unscaled","DeltaNeutrophils_unscaled",  "DeltaPLT_unscaled","DeltaUrea_unscaled","DeltaCreatinine_unscaled",  "DeltaHb_unscaled", "DeltaAlbumin_unscaled")

unscaled.clustering.columns = patient.data[clustering.columns]
colnames(unscaled.clustering.columns) = unscaled.colnames

patient.data[clustering.columns] <- scale(patient.data[clustering.columns])

patient.data = cbind(patient.data,unscaled.clustering.columns)

clustering.data = patient.data[clustering.columns]
clustering.data= data.matrix(clustering.data, rownames.force = NA)

################################2. Train SOM grid
som_grid <- somgrid(xdim = 4, ydim=4, topo="hexagonal")

################################3. create SOM for clustering variables
knox.som = kohonen::supersom(clustering.data,grid = som_grid, rlen=1000,alpha=c(0.05,0.01),keep.data = TRUE)

################################4. Plot clustering performance metrics
    ##plot changes in neighbourhood to examining quality. It took 1000 iterations to reach a 'plateau' curve.
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/trainingQuality.pdf")
    plot(knox.som, type="changes", main="Training Progress")
    dev.off()

    ##plot the count of samples mapping to each cluster.
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/nodeCount.pdf")
    plot(knox.som, type="count", main="Node Counts")
    dev.off()

    ##Plot distance matrix: Often referred to as the “U-Matrix”, this visualisation is of the distance between each node and its neighbours. Typically viewed with a grayscale palette,
    ##areas of low neighbour distance indicate groups of nodes that are similar. Areas with large distances indicate the nodes are much more dissimilar –
    ##and indicate natural boundaries between node clusters. The U-Matrix can be used to identify clusters within the SOM map.
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/neighbourDistance.pdf")
    plot(knox.som, type="dist.neighbours", main = "SOM neighbour distances")
    dev.off()
    ##plot quality map: shows the mean distance of objects mapped to a unit to the codebook vector of that unit.
    ##The smaller the distances, the better the objects are represented by the codebook vectors.
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/quality.pdf")
    plot(knox.som, type="quality", main="Clustering Quality")
    dev.off()
    ##plot the codebook vectors, representing the distribution of each feature in each SOM node using a fan diagram.
    ##individual fan representations of the magnitude of each variable in the weight vector is shown for each node.
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/nodes.pdf")
    plot(knox.som, type="codes", main="Codes") #palette.name=coolBlueHotRed
    dev.off()

################################5. Hierarchical clustering with contiguity constraints
################################From: https://rpubs.com/erblast/SOM
    ############# 5.1 preparation and calculating distances
    codes = tibble( layers = colnames(knox.som$codes[[1]])
    ,codes = knox.som$codes ) %>%
    mutate( codes = purrr::map(codes, as_tibble) ) %>%
    spread( key = layers, value = codes) %>%
    apply(1, bind_cols) %>%
    .[[1]] %>%
    as_tibble()

    # generate distance matrix for codes
    dist_m = dist(codes) %>%
    as.matrix()

    # generate seperate distance matrix for map location
    dist_on_map = kohonen::unit.distances(som_grid)
    dist_adj = dist_m ^ dist_on_map
    #############6.2 calculating optimal number of clusters visually: Ellbow, Silhouette and Gap
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/optimalNoOfClustersElbow.pdf")
    factoextra::fviz_nbclust(dist_adj
                    , factoextra::hcut
                    , method = "wss"
                    , hc_method = 'ward.D2'
                    , k.max = 15)

    dev.off()

    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/optimalNoOfClustersSilhouette.pdf")
    factoextra::fviz_nbclust(dist_adj
                     , factoextra::hcut
                     , method = "silhouette"
                     , hc_method = "ward.D2"
                     , k.max =  15)
     dev.off()


    #############6.3 calculating optimal number of clusters: voting among many methods
    indexes = c( "wss","silhouette","gap", "kl", "ch", "hartigan", "ccc", "scott", "marriot", "trcovw", "tracew", "friedman", "rubin", "cindex", "db", "duda", "pseudot2", "beale", "ratkowsky")


    results_nb = list()
    safe_nb = purrr::safely(NbClust::NbClust)
    # we will time the execution time of each step
    best.number.of.clusters = vector()

    for(i in 1:length(indexes) ){
        t = lubridate::now()
        nb = safe_nb(as.dist(dist_adj)
                    , distance = "manhattan"
                    , min.nc = 4
                    , max.nc = 15
                    , method = "ward.D2"
                    , index = indexes[i]
                    )
         print(paste("at index", i, " doing method: ",indexes[i]))

        results_nb[[i]] = nb
	best.number.of.clusters = c(best.number.of.clusters,nb$result$Best.nc[1])

    }

   final.number.of.clusters = max(Modes(best.number.of.clusters))
   final.number.of.clusters  = 5

    df_clust = tibble( indexes = indexes
                            , nb = results_nb) %>%
                    mutate( results = purrr::map(nb,'result')
                                , error = purrr::map(nb, 'error')
                                , is_ok = purrr::map_lgl(error, is_null))

    df_clust_success = df_clust %>%
    filter( is_ok ) %>%
    mutate( names      = purrr::map(results, names)
                        ,all_index = purrr::map(results, 'All.index')
                        ,best_nc   = purrr::map(results, 'Best.nc')
                        ,best_nc   = purrr::map(best_nc, function(x) x[[1]])
                        ,is_ok     = !purrr::map_lgl(best_nc, is_null)
    ) %>%
    filter(is_ok) %>%
    mutate( best_nc    = purrr::flatten_dbl(best_nc))

    save(df_clust_success, file = 'NumberOfClustersVotes.Rdata')

    #plot votes
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/VotesOnNoOfClusters.pdf")
    df_clust_success %>%
    filter(!is_null(best_nc) )%>%
    ggplot( aes(x = as.factor(best_nc))) +
    geom_bar()+
    labs(title = 'Votes on optimal number of clusters'
                        ,x = 'Best No of Clusters')
        dev.off()




    #############6.4 cluster using hierarchical clustering
    dist_adj =  dist_m ^ dist_on_map
    clust_adj = hclust(as.dist(dist_adj), 'ward.D2')

    #############Cluster using final.number.of.clusters clusters (generated by analysis above).
    som_clusters = cutree(clust_adj, final.number.of.clusters) 
    pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/Clusters.pdf")
    plot(knox.som, type = "property", property=som_clusters,main="Clusters",palette.name=rainbow, heatkeywidth = 0.9)
    add.cluster.boundaries(knox.som, som_clusters,lwd=3)
    dev.off()

# get vector with cluster value for each original data sample
    cluster_assignment = vector()
    cluster_assignment <- som_clusters[knox.som$unit.classif]    #  knox.som$unit.classif is the som node for each data point in the original data.
    # make the cluster assignment a column in the original data for ease of retrieval.
    patient.data$cluster_assignment = cluster_assignment


    #############Save Image for plotting later on
    save.image(file="/Users/babylon/Documents/Data/KCHData/ClusteringData/SOMClusteringFirst2Days.RData")

    write.csv(patient.data, file = "/Users/babylon/Documents/Data/KCHData/ClusteringData/ClusteredDataFirst2Days.csv")
