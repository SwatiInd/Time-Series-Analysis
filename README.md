# Time Series Analysis

A time series can be considered of three parts:
- Time index
- Target (independent) variable 
- Input (dependent) variables

A class for each of them is developed to explore their characterisitcs. The class methods are illustrated in their respective example files. 

## 1. Time Index Processing 

In modeling/forecasting, a continuous time series is required. Any missing or duplicated index can influence their results. Therefore, the following methods were developed to obtain cleaned time series index:

### 1.1 Convert column to time index
   
The first step is to convert the column which represent date and time of time sereis into time index.

### 1.2 Duplicate time index

Some  pandas method don't work on duplicate index. Therefore, they need to be checked and further action like dropping, averaging etc. needs to be decided based on data. 
In the developed method, the first index of duplicates is kept in time series while others are dropped. 

### 1.3 Missing time index
   
A list of missing time index is identified and subsequently, these missing rows are added in dataframe with null values for all columns.  

The above methods can be used by the following code:
```python
from TimeindexProcessing import TimeindexProcessing 

# Create the class object
index_processing = TimeindexProcessing()

# Convert a column 'datetime' into time index
indexed_df = index_processing.convert_column_to_timeindex(df, column_name= 'Datetime')

# Determine a list of duplicates index and build a new dataframe by keeping only first row of duplicates index
duplicates_index_list, duplicates_corrected_df = index_processing.duplicate_timeindex(indexed_df)

# Duplicates index in the original dataframe can be checked by:
indexed_df.loc[duplicates_index_list]

# Duplicates corrected dataframe for original dataframe's duplicates:
duplicates_corrected_df.loc[duplicates_index_list]

# Identify missing index based on declared data frequency and add these rows into duplicates corrected dataframe
data_freq = '1H' # Define the expected data frequency
missing_index_list, rows_added_df = index_processing.missing_timeindex(duplicates_corrected_df, data_freq)

# To confirm whether missing rows are added in dataframe:
rows_added_df.loc[missing_index_list]
```

## 2. Target Variable Processing

As a first step, missing and outlier values of targt variable are identified . Subsequently, basic characteristics of time series (seasonality, trend, stationary etc.) are observed from plots and statistics test. Then, correlation of current values with previous values and time parameters are evaluated. Based on the outcomes, dataframes of relevant features are created which are used in time sereis modeling. 

### 2.1 Missing, unique, and outliers values
Number of missing and outlier values are examined and imputed before any further processing. Number of unique values indicates whether target variable is a categorical or continous value.

### 2.2 Data Visualisation
Daily, weekly, and monthly data are plotted to identify seasonality. In order to determine trend, the whole dataset is plotted. 

### 2.3 Stationarity
Augumented-Dickey Fuller Test is performed to confirm whether time series is stationary or non-stationary.

### 2.4 Feature engineering
This step is useful for creating features for supervised machine learning models (e.g.: linear regression, radnom forest, decision trees). In the developed class, methods are developed for following cases:

(a) *Autocorrelation*: Correlation of the current value to previous lags is determiend. 
    
(b) *Time parameters*:  Influence of hour of the day, day of the month, week day, and month of the year on output parameter is also understood. 

Parameters which have strong coorelation with the output parameter can be created as input features.

Methods of section 2 are in continuation to the section 1 as shown below:
```python
from TargetVariableProcessing import TargetVariableProcessing

# Extract the output series from cleaned dataframe
output_parameter = 'PJME_MW' # String of output parameter
output_series = rows_added_df[output_parameter]

# Create Target Variable Processing class object
tvp = TargetVariableProcessing(output_series)

# Determine missing, and unique value counts in output series
missing_values = tvp.missing_values()
unique_value_counts = tvp.unique_value_counts()

# Data visualisation for the defined start date and number of days 
start_date = '2003-12-31'
days = 1

title = 'Daily Electricity Consumption'
plot = tvp.plotting_timeseries(output_series, 
                             start_date = start_date, 
                             days = days, 
                             figsize = (8,6), 
                             title = title)

# Identifying whethter output series is stationary or not
adf_result = tvp.stationarity()

# Measuring correlation of defined time parameters to output series
time_parameters = ['hour', 'day', 'month', 'weekday']
time_correlation = tvp.correlation_to_timeperiod(time_parameters)

# Creating features of strongly correlated time parameters 
time_features_to_add = ['hour', 'working day']
time_features_df = tvp.create_time_features(time_features_to_add)

# Evaluating correlation of the current value to defined previous lags
previous_lags = 24*7
autocorrelation = tvp.autocorrelation(lag_number = previous_lags)

# Adding features of previous lags showing strong correlation to the current value
previous_strong_lags = [1, 2, 24]
added_lags_df = tvp.create_lag_features(previous_strong_lags)
```
   

