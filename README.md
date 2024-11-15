# Time Series Analysis

A time series can be considered of three parts:
- Time index
- Input variables
- Target variable

A class for each of them is developed to explore their characterisitcs. The class methods are illustrated in their respective example files. 

## Time Index Processing 

## Input Variable Processing

## Target Variable Processing

As a first step, missing and outlier values of targt variable are identified . Subsequently, basic characteristics of time series (seasonality, trend, stationary etc.) are observed from plots and statistics test. Then, correlation with previous values and time parameters are evaluated. Based on the outcomes, dataframes of relevant features are created which are used in further modeling. 

### Missing, unique, and outliers values
    - Number of missing and outlier values are examined and imputed before any further processing. Number of unique values indicates whether target variable is a categorical or continous value. 
### Data Visualisation
    - Daily, weekly, and monthly data is plotted to identify seasonality.
    - From the plot of whole dataset, trend is observed.
    
### Stationarity
    - For time series, Augumented-Dickey Fuller Test is performed.

### Feature engineering
    - *Autocorrelation* : Correlation of the current value to previous lags is determiend. 
    - *Time parameters*:  Influence of hour of the day, day of the month, week day, and month of the year on electricity consumption is also understood. 

    Lags and time parameters of strong correlation are created as input features.

