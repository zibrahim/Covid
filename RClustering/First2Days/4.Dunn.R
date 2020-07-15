library("RColorBrewer")
library("rpivotTable")
library('dunn.test')
library("car")
load(file="/Users/babylon/Documents/Data/KCHData/ClusteringData/SOMClusteringFirst2Days.RData")



##1. prepare etiology - regroup it into one column:
##abdominal: 1, biliar: 2, liver: 3, renal: 4, soft tissue: 5, 6: UTI, 7: pneumonia, 8: other

clust1 = subset(patient.data, patient.data$cluster_assignment==1)
clust2 = subset(patient.data, patient.data$cluster_assignment==2)
clust3 = subset(patient.data, patient.data$cluster_assignment==3)
clust4 = subset(patient.data, patient.data$cluster_assignment==4)
clust5 = subset(patient.data, patient.data$cluster_assignment==5)



sink("/Users/babylon/Documents/Covid/RClustering/First2Days/DunnTest.txt")

##Sofa and subcomponents

print("**********************************  7 Day Mortality ********************************** ")
dtsofa = dunn.test(x=list(clust1$Mortality7Days,clust2$Mortality7Days,clust3$Mortality7Days,clust4$Mortality7Days,clust5$Mortality7Days),method='Bonferroni',kw=TRUE)


print("**********************************  14 Day Mortality ********************************** ")
dtsofa = dunn.test(x=list(clust1$Mortality14Days,clust2$Mortality14Days,clust3$Mortality14Days,clust4$Mortality14Days,clust5$Mortality14Days),method='Bonferroni',kw=TRUE)


print("**********************************  30 Day Mortlity ********************************* ")

dtrespiration = dunn.test(x=list(clust1$Mortality30Days,clust2$Mortality30Days,clust3$Mortality30Days,clust4$Mortality30Days,clust5$Mortality30Days),method='Bonferroni',kw=TRUE)

print("**********************************  ITU Admission 7 Days********************************** ")

dtcogulation = dunn.test(x=list(clust1$ITUAdmission7Days,clust2$ITUAdmission7Days,clust3$ITUAdmission7Days,clust4$ITUAdmission7Days,clust5$ITUAdmission7Days),method='Bonferroni',kw=TRUE)

print("**********************************  ITU Admission 14 Days********************************** ")

dtcogulation = dunn.test(x=list(clust1$ITUAdmission14Days,clust2$ITUAdmission14Days,clust3$ITUAdmission14Days,clust4$ITUAdmission14Days,clust5$ITUAdmission14Days),method='Bonferroni',kw=TRUE)

print("********************************** ITU Admission 30 Days********************************* ")


dtliver = dunn.test(x=list(clust1$ITUAdmission30Days,clust2$ITUAdmission30Days,clust3$ITUAdmission30Days,clust4$ITUAdmission30Days,clust5$ITUAdmission30Days),method='Bonferroni',kw=TRUE)





sink()
