library('kohonen')
library('Hmisc')
library('yarrr') ####the pirate library for colours and more
    ###### play with colors here: https://cran.r-project.org/web/package/yarrr/vignettes/piratepal.html
    ###### my.cols <- piratepal(palette = "evildead",trans = .5)

rm(list=ls())
load(file="/Users/babylon/Documents/Data/KCHData/SOMClusteringBaseline.RData")

clusters = list()
clusters[[1]] = som_clusters


myPalette <- function(n=20, alpha = 1) { heat.colors(n,  alpha=alpha)[n:1] }
rainbowPalette <- function(n, alpha = 1) { rainbow(n,  alpha=alpha)[n:1] }
i = 1
k=max(unique(som_clusters))

pdf("/Users/babylon/Documents/Covid/Figures/ClusteringBaseline/AllFeatures.pdf")

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


Creatinine.unscaled <- aggregate(as.numeric(patient.data$CreatinineUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Creatinine.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Creatinine.unscaled$Node))
names(Creatinine.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Creatinine.unscaled<- rbind(Creatinine.unscaled, data.frame(Node=missingNodes, Value=NA))
Creatinine.unscaled <- Creatinine.unscaled[order(Creatinine.unscaled$Node),]
plot(knox.som, type = "property", property=Creatinine.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Creatinine", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



SysBP.unscaled <- aggregate(as.numeric(patient.data$SysBPUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(SysBP.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% SysBP.unscaled$Node))
names(SysBP.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
SysBP.unscaled<- rbind(SysBP.unscaled, data.frame(Node=missingNodes, Value=NA))
SysBP.unscaled <- SysBP.unscaled[order(SysBP.unscaled$Node),]
plot(knox.som, type = "property", property=SysBP.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total SysBP", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



HeartRate.unscaled <- aggregate(as.numeric(patient.data$HeartRateUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(HeartRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% HeartRate.unscaled$Node))
names(HeartRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled<- rbind(HeartRate.unscaled, data.frame(Node=missingNodes, Value=NA))
HeartRate.unscaled <- HeartRate.unscaled[order(HeartRate.unscaled$Node),]
plot(knox.som, type = "property", property=HeartRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total HeartRate", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


SupplementalOxygen.unscaled <- aggregate(as.numeric(patient.data$SupplementalOxygenUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(SupplementalOxygen.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% SupplementalOxygen.unscaled$Node))
names(SupplementalOxygen.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
SupplementalOxygen.unscaled<- rbind(SupplementalOxygen.unscaled, data.frame(Node=missingNodes, Value=NA))
SupplementalOxygen.unscaled <- SupplementalOxygen.unscaled[order(SupplementalOxygen.unscaled$Node),]
plot(knox.som, type = "property", property=SupplementalOxygen.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total SupplementalOxygen", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



OxygenSaturation.unscaled <- aggregate(as.numeric(patient.data$OxygenSaturationUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(OxygenSaturation.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% OxygenSaturation.unscaled$Node))
names(OxygenSaturation.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
OxygenSaturation.unscaled<- rbind(OxygenSaturation.unscaled, data.frame(Node=missingNodes, Value=NA))
OxygenSaturation.unscaled <- OxygenSaturation.unscaled[order(OxygenSaturation.unscaled$Node),]
plot(knox.som, type = "property", property=OxygenSaturation.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total OxygenSaturation", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



Temperature.unscaled <- aggregate(as.numeric(patient.data$TemperatureUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Temperature.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Temperature.unscaled$Node))
names(Temperature.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Temperature.unscaled<- rbind(Temperature.unscaled, data.frame(Node=missingNodes, Value=NA))
Temperature.unscaled <- Temperature.unscaled[order(Temperature.unscaled$Node),]
plot(knox.som, type = "property", property=Temperature.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Temperature", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


RespirationRate.unscaled <- aggregate(as.numeric(patient.data$RespirationRateUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(RespirationRate.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% RespirationRate.unscaled$Node))
names(RespirationRate.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
RespirationRate.unscaled<- rbind(RespirationRate.unscaled, data.frame(Node=missingNodes, Value=NA))
RespirationRate.unscaled <- RespirationRate.unscaled[order(RespirationRate.unscaled$Node),]
plot(knox.som, type = "property", property=RespirationRate.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total RespirationRate", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



WBC.unscaled <- aggregate(as.numeric(patient.data$WBCUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(WBC.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% WBC.unscaled$Node))
names(WBC.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
WBC.unscaled<- rbind(WBC.unscaled, data.frame(Node=missingNodes, Value=NA))
WBC.unscaled <- WBC.unscaled[order(WBC.unscaled$Node),]
plot(knox.som, type = "property", property=WBC.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total WBC", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


Hb.unscaled <- aggregate(as.numeric(patient.data$HbUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Hb.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Hb.unscaled$Node))
names(Hb.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Hb.unscaled<- rbind(Hb.unscaled, data.frame(Node=missingNodes, Value=NA))
Hb.unscaled <- Hb.unscaled[order(Hb.unscaled$Node),]
plot(knox.som, type = "property", property=Hb.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Hb", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



Urea.unscaled <- aggregate(as.numeric(patient.data$UreaUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Urea.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Urea.unscaled$Node))
names(Urea.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Urea.unscaled<- rbind(Urea.unscaled, data.frame(Node=missingNodes, Value=NA))
Urea.unscaled <- Urea.unscaled[order(Urea.unscaled$Node),]
plot(knox.som, type = "property", property=Urea.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Urea", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


C.Reactive.Protein.unscaled <- aggregate(as.numeric(patient.data$C.Reactive.ProteinUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(C.Reactive.Protein.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% C.Reactive.Protein.unscaled$Node))
names(C.Reactive.Protein.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
C.Reactive.Protein.unscaled<- rbind(C.Reactive.Protein.unscaled, data.frame(Node=missingNodes, Value=NA))
C.Reactive.Protein.unscaled <- C.Reactive.Protein.unscaled[order(C.Reactive.Protein.unscaled$Node),]
plot(knox.som, type = "property", property=C.Reactive.Protein.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total C.Reactive.Protein", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


Albumin.unscaled <- aggregate(as.numeric(patient.data$AlbuminUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(Albumin.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% Albumin.unscaled$Node))
names(Albumin.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
Albumin.unscaled<- rbind(Albumin.unscaled, data.frame(Node=missingNodes, Value=NA))
Albumin.unscaled <- Albumin.unscaled[order(Albumin.unscaled$Node),]
plot(knox.som, type = "property", property=Albumin.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total Albumin", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



PLT.unscaled <- aggregate(as.numeric(patient.data$PLTUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(PLT.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% PLT.unscaled$Node))
names(PLT.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
PLT.unscaled<- rbind(PLT.unscaled, data.frame(Node=missingNodes, Value=NA))
PLT.unscaled <- PLT.unscaled[order(PLT.unscaled$Node),]
plot(knox.som, type = "property", property=PLT.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total PLT", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)


GCSVerbal.unscaled <- aggregate(as.numeric(patient.data$GCSVerbalUnscaled), by=list(knox.som$unit.classif), FUN=mean, simplify=TRUE)
names(GCSVerbal.unscaled) <- c("Node", "Value")
missingNodes <- which(!(seq(1,nrow(knox.som$codes[[1]])) %in% GCSVerbal.unscaled$Node))
names(GCSVerbal.unscaled) = names(data.frame(Node=missingNodes, Value=NA))
GCSVerbal.unscaled<- rbind(GCSVerbal.unscaled, data.frame(Node=missingNodes, Value=NA))
GCSVerbal.unscaled <- GCSVerbal.unscaled[order(GCSVerbal.unscaled$Node),]
plot(knox.som, type = "property", property=GCSVerbal.unscaled$Value,main="",palette.name=myPalette, heatkeywidth = 0.9)
title("Total GCSVerbal", line=1)
add.cluster.boundaries(knox.som, clusters[[i]],lwd=5)



dev.off()




