library('kohonen')

rm(list=ls())
load(file="/Users/babylon/Documents/Data/KCHData/ClusteringData/SOMClusteringFirst2Days.RData")

clusters = list()
clusters[[1]] = som_clusters


myPalette <- function(n=20, alpha = 1) { heat.colors(n,  alpha=alpha)[n:1] }
rainbowPalette <- function(n, alpha = 1) { rainbow(n,  alpha=alpha)[n:1] }
i = 1
k=max(unique(som_clusters))

pdf("/Users/babylon/Documents/Covid/Figures/Clustering/First2Days/AllFeatures.pdf")

layout(matrix(c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 17, 18, 19, 20),4,5,  byrow = TRUE))##,	widths=c(3,3,3,3))


Age.unscaled <- aggregate(as.numeric(patient.data$Age), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Age.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Age.unscaled$Node))
names(Age.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Age.unscaled<- rbind(Age.unscaled, data.frame(Node=missingNodes, Value=NA))
Age.unscaled <- Age.unscaled[order(Age.unscaled$Node),]
plot(knox.som, type = "property", property=Age.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Age", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

NumComorbidities.unscaled <- aggregate(as.numeric(patient.data$NumComorbidities), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(NumComorbidities.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% NumComorbidities.unscaled$Node))
names(NumComorbidities.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
NumComorbidities.unscaled<- rbind(NumComorbidities.unscaled, data.frame(Node=missingNodes, Value=NA))
NumComorbidities.unscaled <- NumComorbidities.unscaled[order(NumComorbidities.unscaled$Node),]
plot(knox.som, type = "property", property=NumComorbidities.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total NumComorbidities", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

Creatinine.unscaled <- aggregate(as.numeric(patient.data$DeltaCreatinine_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Creatinine.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Creatinine.unscaled$Node))
names(Creatinine.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Creatinine.unscaled<- rbind(Creatinine.unscaled, data.frame(Node=missingNodes, Value=NA))
Creatinine.unscaled <- Creatinine.unscaled[order(Creatinine.unscaled$Node),]
plot(knox.som, type = "property", property=Creatinine.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta Creatinine", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


SysBP.unscaled <- aggregate(as.numeric(patient.data$DeltaSysBP_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(SysBP.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% SysBP.unscaled$Node))
names(SysBP.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
SysBP.unscaled<- rbind(SysBP.unscaled, data.frame(Node=missingNodes, Value=NA))
SysBP.unscaled <- SysBP.unscaled[order(SysBP.unscaled$Node),]
plot(knox.som, type = "property", property=SysBP.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta SysBP", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


SysBP.unscaled <- aggregate(as.numeric(patient.data$DeltaDiasBP_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(SysBP.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% SysBP.unscaled$Node))
names(SysBP.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
SysBP.unscaled<- rbind(SysBP.unscaled, data.frame(Node=missingNodes, Value=NA))
SysBP.unscaled <- SysBP.unscaled[order(SysBP.unscaled$Node),]
plot(knox.som, type = "property", property=SysBP.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta DiasBP", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaCReactiveProtein_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta CRP", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaWBC_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta WBC", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaLymphocytes_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta Lymphocytes", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaNeutrophils_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta Neutrophils", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaPLT_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta PLT", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaUrea_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta Urea", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaHb_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta Hb", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)




HeartRate.unscaled <- aggregate(as.numeric(patient.data$DeltaAlbumin_unscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Delta Albumin", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


HeartRate.unscaled <- aggregate(as.numeric(patient.data$ITUAdmission30Days), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("30-Day ITU", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HeartRate.unscaled <- aggregate(as.numeric(patient.data$ITUAdmission14Days), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("14-Day ITU", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HeartRate.unscaled <- aggregate(as.numeric(patient.data$ITUAdmission7Days), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("7-Day ITU", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HeartRate.unscaled <- aggregate(as.numeric(patient.data$Mortality30Days), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("30-Day Mortality", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HeartRate.unscaled <- aggregate(as.numeric(patient.data$Mortality14Days), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("14-Day Mortality", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

HeartRate.unscaled <- aggregate(as.numeric(patient.data$Mortality7Days), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("7-Day Mortality", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)

dev.off()

