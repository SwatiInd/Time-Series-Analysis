import pandas as pd
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

class TargetVariableProcessing:
    '''A class for exploring charactersitics of target variable of a time series '''

    def __init__(self, output_series):
        '''
        Parameters
        ----------
        output_series: series
            A series of target variable
        '''
       
        self.output_series = output_series
        # self.output_column_name = output_column_name
        self.start_date = str(self.output_series.index[0].date)
    
    def missing_values(self):
        '''Determines the missing values of target variables

        Returns
        ------
        dataframe
            number of missing values of all target variables
        '''
        missing_df = self.output_series.copy()
        missing_values_count = missing_df.isna().sum()
        return missing_values_count

    def unique_value_counts(self):
        '''Counts the unique values of each target variable
        
        Returns
        ------
        dataframe
            Number of unique values of each variable
        '''

        unique_value_counts = self.output_series.nunique()
        # unique_value_counts = unique_value_counts.nunique()
        return unique_value_counts
    
    def plotting_timeseries(self,
                            series_to_plot,
                            start_date,
                            end_date = None,
                            days = 1, 
                            figsize = (15,8),
                            title = None
                            ):
        '''Plots timeseries from start date for number of days
        If arguments are not passed in, the default one day output series is plotted.

        Parameters
        ---------
        series_to_plot: timeseries
            A series to be plotted with time index, default -> output sereis
        start_date: str
            Start date for plotting the figure
        end_date: str
            End date (exclusive date) of figure, if None then it calculates based on number of days
        days: int
            Number of days, end_date is start_date + days
            default -> 1, end_date is the next day of the start day
        figsize: tuple
            figure size to be plotted, default -> (15,8)

        Returns
        -------
        figure
            a figure of timeseries for number of days and mentioned from the start date
        '''

        # series_to_plot = series_to_plot.copy()
        series_index = series_to_plot.index
        start_date = pd.to_datetime(start_date)
        
        if(end_date is None):
            end_date = start_date + timedelta(days = days)
        else:
            end_date = pd.to_datetime(end_date)

        data_to_plot = series_to_plot[(series_index >=start_date) & (series_index<=end_date)]
        data_to_plot.plot(figsize = figsize, title = title);

        # return data_to_plot

    def correlation_to_timeperiod(self, periods_parameters):
        '''Determines the correlation of periods parameters chosen 
        from hour, day, week day, month to the output series

        Parameters
        ----------
        periods_parameters: list
            A list of all periods parameters (e.g. ['hour', 'weekofday']) 

        Returns
        ------
        correlation of output to the time period in descending order 
        '''

        corr_df = pd.DataFrame(self.output_series.copy())
        output_parameter = self.output_series.name
        # print(output_parameter)
        index = corr_df.index
        if('hour' in periods_parameters):
            corr_df.loc[: , 'hour'] = index.hour
        
        if('day' in periods_parameters):
            corr_df.loc[:, 'day'] = index.day

        if('month' in periods_parameters):
            corr_df.loc[:, 'month'] = index.month    
        
        if('weekday' in periods_parameters):
            corr_df.loc[:, 'weekday'] = index.weekday # Monday ->0, Sunday -> 6
            # based on weekday (0, 1, 2, 3, 4) working day -> 0 , weekend (5, 6) ->1 
            corr_df.loc[:, 'working day'] = corr_df.weekday.apply(lambda x:0 if x<5 else 1)
        
        correlation_to_output = corr_df.corr()[output_parameter]
        # correlation_to_output  = correlation_to_output.abs()

        return correlation_to_output.sort_values(ascending = False)
    
    def autocorrelation(self, lag_number = 1):
        '''Evaluates absolute value of auto-correlationo of time series with its own lag

        Parameters
        ---------
        lag_number: int
            Lag numbers (including) for which autocorrelation is to be calculated

        Return
        ------
        series
            A series of autocorrelation values in descending order with index as number of lags
        '''

        autocorrs = pd.Series(data = [self.output_series.autocorr(lag = i) for i in range(1, lag_number+1)],
        index = np.arange(1, lag_number+1, 1))
        autocorrs = autocorrs.abs()

        return autocorrs.sort_values(ascending = False)

    def create_time_features(self, time_features_to_add = []):
        '''Builds a dataframe of time features to be considered as input features
        
        Parameters
        ----------
        time_features_to_add: list
            List of all time features (e.g.: hour, day etc.) of strong correlation to output
        
        Return
        ------
        dataframe
            A dataframe of the same index as of output series and values of time features
        '''

        index = self.output_series.index
        time_features_df = pd.DataFrame(index = index)
        if('hour' in time_features_to_add):
            time_features_df.loc[:, 'hour'] = index.hour
        
        if('day' in time_features_to_add):
            time_features_df.loc[:, 'day'] = index.day

        if('month' in time_features_to_add):
            time_features_df.loc[:, 'month'] = index.month    
        
        if('weekday' in time_features_to_add):
            time_features_df.loc[:, 'weekday'] = index.weekday # Monday ->0, Sunday -> 6
            # based on weekday (0, 1, 2, 3, 4) working day -> 0 , weekend (5, 6) ->1 
        if('working day' in time_features_to_add):
            time_features_df.loc[:, 'weekday'] = index.weekday # Monday ->0, Sunday -> 6
            time_features_df .loc[:, 'working day'] = time_features_df.weekday.apply(lambda x:0 if x<5 else 1)
            time_features_df.drop('weekday', axis = 1, inplace = True)
        
        return time_features_df

    def create_lag_features(self, lags = []):
        ''' Builds a dataframe of output values by shifting of mentioned lags values

        Parameters
        ---------
        lags: list
            List of all lags to be added in new dataframe
            default -> empty list (no lag to be added)

        Returns 
        -------
        dataframe with added lags for output parameter
        '''

        index = self.output_series.index
        output_parameter = self.output_series.name
        added_lags_df = pd.DataFrame(index = index)

        if(len(lags)!= 0):
            # print(len(lags))
            for lag in lags:
                new_column_name =  output_parameter  + '_lag' + str(lag)
                added_lags_df[new_column_name] = self.output_series.shift(lag)

        return added_lags_df    
    

    def stationarity(self):
        '''Determines stationarity of time series based on Augumented-Dickey Fuller Test
        
        Returns
        ------
        prints staionarity of output series
        '''

        adf_result = adfuller(self.output_series)
        stationarity = None
        if(adf_result[1] <0.05):
            stationarity = 'stationary'
            # print('Time series is stationary')
        else:
            adf_stationarity = 'non-stationary'
        print(stationarity)

        return adf_result