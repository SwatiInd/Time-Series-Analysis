# Time Series Analysis

A time series can be considered of three parts:
- Time index
- Input variables
- Target variable

A class for each of them is developed to explore their characterisitcs. The class methods are illustrated in their respective example files. 

## Time Index Processing 

In modeling/forecasting, a continuous time series is required. Any missing or duplicated index can influence their results. Therefore, the following methods were developed to obtain cleaned time series index:

1. Convert column to time index
    The first step is to convert the column which represent date and time of time sereis into time index. 

2. Duplicate time index
    Some  pandas method don't work on duplicate index. Therefore, they need to be checked and further action like dropping, averaging etc. needs to be decided based on data. In the developed method, the first index of duplicates is kept in time series while others are dropped.

3. Missing time index
    A list of missing time index is identified. Subsequently, these missing rows are added in dataframe with null values for all columns.  

## Input Variable Processing

## Target Variable Processing

As a first step, missing and outlier values of targt variable are identified . Subsequently, basic characteristics of time series (seasonality, trend, stationary etc.) are observed from plots and statistics test. Then, correlation of current values with previous values and time parameters are evaluated. Based on the outcomes, dataframes of relevant features are created which are used in time sereis modeling. 

### Missing, unique, and outliers values
    Number of missing and outlier values are examined and imputed before any further processing. Number of unique values indicates whether target variable is a categorical or continous value. 
### Data Visualisation
    Daily, weekly, and monthly data are plotted to identify seasonality. In order to determine trend, the whole dataset is plotted. 
    
### Stationarity

    Augumented-Dickey Fuller Test is performed to confirm whether time series is stationary or non-stationary.

### Feature engineering
    This step is useful for creating features for supervised machine learning models (e.g.: linear regression, radnom forest, decision trees). In the developed class, methods are developed for following cases:
    1. *Autocorrelation*: Correlation of the current value to previous lags is determiend. 
    2. *Time parameters*:  Influence of hour of the day, day of the month, week day, and month of the year on electricity consumption is also understood. 

    Lags and time parameters of strong correlation are created as input features.

