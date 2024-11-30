import pandas as pd

class TimeindexProcessing:
    '''A class for investigation of timeseries index'''
    
    def convert_column_to_timeindex(self, df, column_name = None):
        '''Converts and sorts a column to time index 
        
        Parameters
        ----------
        df: dataframe
            A dataframe whose column needs to be converted into timeindex
        columns_name: str
            A column which will be converted into index (default in None)
        '''

        time_index_df = df.copy()
        # for index in all_index:
        #     if(type(index) != pd._libs.tslibs.timestamps.Timestamp):
        #         index_to_drop.append(index)
        # time_index_df.drop(index_to_drop, axis = 0, inplace = True)
        if(column_name is not None):
            time_index_df.set_index(column_name, inplace = True)
            time_index_df.index = pd.to_datetime(time_index_df.index)
        time_index_df.sort_index(inplace = True)
        return time_index_df


    def missing_timeindex(self, df, time_interval):
        '''Identifies missing time index of a dataframe
        
        Parameters
        ----------
        time_interval: str
            Time interval between two consecutive data points
        
        Returns
        ------------
        list
            list of missing index in input dataframe
        dataframe
            dataframe after adding rows of missing index
        '''

        rows_added_df = df.copy()
        rows_added_df.sort_index(inplace = True)
        start_time, end_time = rows_added_df.index[0], rows_added_df.index[-1]
        series_index = rows_added_df.index.tolist()
        expected_index = pd.date_range(start= start_time, 
                                    end= end_time,
                                    freq = time_interval).tolist()
        
        missing_index = set(expected_index) - set(series_index)
        missing_index_list = list(missing_index)

        if(len(missing_index_list)!= 0):
            original_dtypes = rows_added_df.dtypes
            print('There are', len(missing_index), 'missing index in the time series')
            #Creating dataframe of missing index and columns of original dataframe
            missing_df = pd.DataFrame(columns = rows_added_df.columns, 
                                index = missing_index_list) 
            #Adding the the missing index into df
            rows_added_df = pd.concat([rows_added_df, missing_df], axis = 'index') 
            # data types of row_added_df change to object types and therefore, converting them to original data types
            for column in rows_added_df.columns:
                column_data_type = original_dtypes.loc[column]
                # print(column, column_data_type)
                rows_added_df[column] = rows_added_df[column].astype(column_data_type)
            rows_added_df.sort_index(inplace = True)
        else:
            missing_df = pd.DataFrame()
            print('All time index present')
    
        return sorted(missing_index_list), rows_added_df

    def duplicate_timeindex(self, df):
        '''Identifies duplicate timeindex
        
        Parameters
        ----------
        df: dataframe
            A dataframe whose duplicate index to be identified

        Returns
        -------
        list
            A list of duplicated time index in the input dataframe
        dataframe
            Dataframe by keeping the first rows of duplicated index
        '''
        
        duplicate_corrected_df = df.copy()
        duplicated_index_list = duplicate_corrected_df[duplicate_corrected_df.index.duplicated()].index.tolist()
        if(len(duplicated_index_list)!=0):
            print('There are', len(duplicated_index_list), 'duplicate index in the time series. ')
            # print(duplicate_corrected_df.loc[duplicated_index_list,:])
            # print('we are keeping the first index of duplicated index')
            duplicate_corrected_df = duplicate_corrected_df[~duplicate_corrected_df.index.duplicated(keep = 'first')]
        else:
            print('There are no duplicate time index')
            
        return duplicated_index_list, duplicate_corrected_df