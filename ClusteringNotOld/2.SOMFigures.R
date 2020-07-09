library('kohonen')
library('Hmisc')
library('yarrr') ####the pirate library for colours and more
    ###### play with colors here: https://cran.r-project.org/web/packages/yarrr/vignettes/piratepal.html
    ###### my.cols <- piratepal(palette = "evildead",trans = .5)

rm(list=ls())
load(file="/Users/babylon/Documents/Covid/Data/SOMClusteringNotOldSxAdmit0.RData")

clusters = list()
clusters[[1]] = som_clusters


myPalette <- function(n=20, alpha = 1) { heat.colors(n,  alpha=alpha)[n:1] }
rainbowPalette <- function(n, alpha = 1) { rainbow(n,  alpha=alpha)[n:1] }
i = 1
k=max(unique(som_clusters))

pdf("/Users/babylon/Documents/Covid/Figures/ClustersNotOld/AllFeatures.pdf")

layout(matrix(c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),4,4,  byrow = TRUE))##,	widths=c(3,3,3,3))

Age.unscaled <- aggregate(as.numeric(patient.data$AgeUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Age.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Age.unscaled$Node))
names(Age.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Age.unscaled<- rbind(Age.unscaled, data.frame(Node=missingNodes, Value=NA))
Age.unscaled <- Age.unscaled[order(Age.unscaled$Node),]
plot(knox.som, type = "property", property=Age.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Age", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


Gender.unscaled <- aggregate(as.numeric(patient.data$Gender), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Gender.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Gender.unscaled$Node))
names(Gender.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Gender.unscaled<- rbind(Gender.unscaled, data.frame(Node=missingNodes, Value=NA))
Gender.unscaled <- Gender.unscaled[order(Gender.unscaled$Node),]
plot(knox.som, type = "property", property=Gender.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Gender", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

NumComorbidities.unscaled <- aggregate(as.numeric(patient.data$NumComorbiditiesUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(NumComorbidities.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% NumComorbidities.unscaled$Node))
names(NumComorbidities.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
NumComorbidities.unscaled<- rbind(NumComorbidities.unscaled, data.frame(Node=missingNodes, Value=NA))
NumComorbidities.unscaled <- NumComorbidities.unscaled[order(NumComorbidities.unscaled$Node),]
plot(knox.som, type = "property", property=NumComorbidities.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title(" NumComorbidities", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

SymptomsToAdmission.unscaled <- aggregate(as.numeric(patient.data$SymptomsToAdmissionUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(SymptomsToAdmission.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% SymptomsToAdmission.unscaled$Node))
names(SymptomsToAdmission.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
SymptomsToAdmission.unscaled<- rbind(SymptomsToAdmission.unscaled, data.frame(Node=missingNodes, Value=NA))
SymptomsToAdmission.unscaled <- SymptomsToAdmission.unscaled[order(SymptomsToAdmission.unscaled$Node),]
plot(knox.som, type = "property", property=SymptomsToAdmission.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title(" SymptomsToAdmission", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

COPD.unscaled <- aggregate(as.numeric(patient.data$COPD), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(COPD.unscaled) <- c("Node", "Value")
#missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% COPD.unscaled$Node))
#names(COPD.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
COPD.unscaled<- rbind(COPD.unscaled, data.frame(Node=missingNodes, Value=NA))
COPD.unscaled <- COPD.unscaled[order(COPD.unscaled$Node),]
plot(knox.som, type = "property", property=COPD.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("COPD", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


Asthma.unscaled <- aggregate(as.numeric(patient.data$Asthma), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Asthma.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Asthma.unscaled$Node))
#names(Asthma.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
#Asthma.unscaled<- rbind(Asthma.unscaled, data.frame(Node=missingNodes, Value=NA))
Asthma.unscaled <- Asthma.unscaled[order(Asthma.unscaled$Node),]
plot(knox.som, type = "property", property=Asthma.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Asthma", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HF.unscaled <- aggregate(as.numeric(patient.data$HF), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HF.unscaled) <- c("Node", "Value")
#missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HF.unscaled$Node))
#names(HF.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HF.unscaled<- rbind(HF.unscaled, data.frame(Node=missingNodes, Value=NA))
HF.unscaled <- HF.unscaled[order(HF.unscaled$Node),]
plot(knox.som, type = "property", property=HF.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("HF", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


Diabetes.unscaled <- aggregate(as.numeric(patient.data$Diabetes), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Diabetes.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Diabetes.unscaled$Node))
#names(Diabetes.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
#Diabetes.unscaled<- rbind(Diabetes.unscaled, data.frame(Node=missingNodes, Value=NA))
Diabetes.unscaled <- Diabetes.unscaled[order(Diabetes.unscaled$Node),]
plot(knox.som, type = "property", property=Diabetes.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Diabetes", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


IHD.unscaled <- aggregate(as.numeric(patient.data$IHD), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(IHD.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% IHD.unscaled$Node))
#names(IHD.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
#IHD.unscaled<- rbind(IHD.unscaled, data.frame(Node=missingNodes, Value=NA))
IHD.unscaled <- IHD.unscaled[order(IHD.unscaled$Node),]
plot(knox.som, type = "property", property=IHD.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("IHD", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HTN.unscaled <- aggregate(as.numeric(patient.data$HTN), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HTN.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HTN.unscaled$Node))
#names(HTN.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
#HTN.unscaled<- rbind(HTN.unscaled, data.frame(Node=missingNodes, Value=NA))
HTN.unscaled <- HTN.unscaled[order(HTN.unscaled$Node),]
plot(knox.som, type = "property", property=HTN.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("HTN", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

CKD.unscaled <- aggregate(as.numeric(patient.data$CKD), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(CKD.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% CKD.unscaled$Node))
#names(CKD.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
#CKD.unscaled<- rbind(CKD.unscaled, data.frame(Node=missingNodes, Value=NA))
CKD.unscaled <- CKD.unscaled[order(CKD.unscaled$Node),]
plot(knox.som, type = "property", property=CKD.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("CKD", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


Mortality.unscaled <- aggregate(as.numeric(patient.data$Mortality), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Mortality.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Mortality.unscaled$Node))
#names(Mortality.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
#Mortality.unscaled<- rbind(Mortality.unscaled, data.frame(Node=missingNodes, Value=NA))
Mortality.unscaled <- Mortality.unscaled[order(Mortality.unscaled$Node),]
plot(knox.som, type = "property", property=Mortality.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Mortality", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

ITUAdmission.unscaled <- aggregate(as.numeric(patient.data$ITUAdmission), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(ITUAdmission.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% ITUAdmission.unscaled$Node))
names(ITUAdmission.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
ITUAdmission.unscaled<- rbind(ITUAdmission.unscaled, data.frame(Node=missingNodes, Value=NA))
ITUAdmission.unscaled <- ITUAdmission.unscaled[order(ITUAdmission.unscaled$Node),]
plot(knox.som, type = "property", property=ITUAdmission.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title(" ITU Admission", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


dev.off()




