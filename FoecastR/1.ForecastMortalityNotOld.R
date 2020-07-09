library(forecastML)
library(dplyr)
library(DT)
library(ggplot2)
library(xgboost)
library('lubridate')

patient_dataset = read.csv("/Users/babylon/Documents/Covid/Data/Patients.csv")
admission_dates <- patient_dataset[c(1,5)]

timeseries_dataset = read.csv("/Users/babylon/Documents/Covid/Data/timeseries_with_clusters_not_old.csv")

timeseries_dataset = merge(timeseries_dataset, admission_dates , by=c("PatientID"))
timeseries_dataset$AdmitDate = as.POSIXct(timeseries_dataset$AdmitDate)

timeseries_dataset$AdmitDate  = timeseries_dataset$AdmitDate  +lubridate::days(timeseries_dataset$Day) +lubridate::hours(timeseries_dataset$OrdinalHour)


drops <- c("OrdinalHour","Day","Hour","FourHourIndex")
drops <- c('ITUAdmission','FourHourIndex','OrdinalHour')
timeseries_dataset = timeseries_dataset[ , !(names(timeseries_dataset) %in% drops)]


timeseries_dataset = timeseries_dataset[,c(1,2,3,4, 5, 76, 77, 6:75)]

names(timeseries_dataset)[7] <- "Observation_Time"

DT::datatable(head(timeseries_dataset), options = list(scrollX = TRUE))


forecast_data <- forecastML::fill_gaps(timeseries_dataset, date_col = 7, frequency = '1 day',
                              groups = 'PatientID', static_features = c('Mortality','SxToAdmit','cluster_assignment'))

print(list(paste0("The original dataset with gaps in data collection is ", nrow(timeseries_dataset), " rows."),
paste0("The modified dataset with no gaps in data collection from fill_gaps() is ", nrow(forecast_data), " rows.")))


write.csv(forecast_data, "/Users/babylon/Documents/Covid/Data/forecast_data.csv", row.names=FALSE)


p <- ggplot(forecast_data, aes(x = AdmitDate, y = Mortality, color = ordered(PatientID), group = cluster_assignment))
p <- p + geom_line()
p <- p + facet_wrap(~ ordered(PatientID), scales = "fixed")
p <- p + theme_bw() + theme(
  legend.position = "none"
) + xlab(NULL)
p

ggsave(p , "mtcars.pdf")


forecast_data$PatientID <- as.numeric(factor(forecast_data$PatientID))

outcome_col <- 3  # The column position of mortality
horizons <- c(1:2)  # Forecast 1, 1:7, and 1:30 days into the future.
lookback <- c(1:2)  # Features from 1 to 3 days in the past

dates <- forecast_data$AdmitDate  # Grouped time series forecasting requires dates.
#forecast_data$AdmissionDate<- NULL  # Dates, however, don't need to be in the input data.
forecast_data$ITUAdmission <- NULL
frequency <- "4 hours"  # A string that works in base::seq(..., by = "frequency").
dynamic_features <- c("AdmissionDate")  # Features that change through time but which will not be lagged.
groups <- "PatientID"  # 1 forecast for each group or buoy.
static_features <- c('SxToAdmit','cluster_assignment')  # Features that do not change through time.
type <- "train"  # Create a model-training dataset.

data_train <- forecastML::create_lagged_df(forecast_data, type = type, outcome_col = outcome_col,
                                           horizons = horizons, lookback = lookback,
                                           dates = dates, frequency = frequency,
                                           groups = groups, static_features = static_features,
                                           use_future = FALSE)

write.csv(data_train$horizon_1, "/Users/babylon/Documents/Covid/Data/training_data.csv", row.names=FALSE)
DT::datatable(head(data_train$horizon_1), options = list(scrollX = TRUE))

p <- plot(data_train)  # plot.lagged_df() returns a ggplot object.
p <- p + geom_tile(NULL)  # Remove the gray border for a cleaner plot.
p



