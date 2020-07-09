library('kohonen')
library('Hmisc')
library('yarrr') ####the pirate library for colours and more
    ###### play with colors here: https://cran.r-project.org/web/packages/yarrr/vignettes/piratepal.html
    ###### my.cols <- piratepal(palette = "evildead",trans = .5)

rm(list=ls())
load(file="/Users/babylon/Documents/Covid/Data/SOMClustering.RData")


cluster1 = subset(patient.data, subset = patient.data$cluster_assignment ==1)
cluster2 = subset(patient.data, subset = patient.data$cluster_assignment ==2)
cluster3 = subset(patient.data, subset = patient.data$cluster_assignment ==3)
cluster4 = subset(patient.data, subset = patient.data$cluster_assignment ==4)
cluster5 = subset(patient.data, subset = patient.data$cluster_assignment ==5)
