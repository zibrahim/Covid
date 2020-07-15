library("RColorBrewer")
library("rpivotTable")
library("car")
rm(list=ls())
load(file="/Users/babylon/Documents/Data/KCHData/ClusteringData/SOMClusteringFirst2Days.RData")


########################2. 5 clusters

## 1: Label groups and set as categorical factors
patient.data$cluster_assignment = factor(patient.data$cluster_assignment)
patient.data$cluster_assignment = factor(patient.data$cluster_assignment, labels=c("1","2","3","4","5"))


##2. Perform levene test to see if the means vary among groups - all significant p-values, so we need non-parametric test and NO ANOVA
leveneTest(patient.data$Mortality7Days, patient.data$cluster_assignment, center=mean)
leveneTest(patient.data$Mortality14Days, patient.data$cluster_assignment, center=mean)
leveneTest(patient.data$Mortality30Days, patient.data$cluster_assignment, center=mean)
leveneTest(patient.data$ITUAdmission7Days, patient.data$cluster_assignment, center=mean)
leveneTest(patient.data$ITUAdmission14Days, patient.data$cluster_assignment, center=mean)
leveneTest(patient.data$ITUAdmission30Days, patient.data$cluster_assignment, center=mean)
leveneTest(patient.data$Age, patient.data$cluster_assignment, center=mean)


##3. Kruskal Wallis Test
kruskal.test(patient.data$Mortality7Days~cluster_assignment, data=patient.data)
kruskal.test(patient.data$Mortality14Days~cluster_assignment, data=patient.data)
kruskal.test(patient.data$Mortality30Days~cluster_assignment, data=patient.data)
kruskal.test(patient.data$ITUAdmission7Days~cluster_assignment,  data=patient.data)
kruskal.test(patient.data$ITUAdmission14Days~cluster_assignment,  data=patient.data)
kruskal.test(patient.data$ITUAdmission30Days~cluster_assignment, data=patient.data)



