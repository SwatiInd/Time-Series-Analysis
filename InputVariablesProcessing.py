import pandas as pd
class InputVariablesProcessing:
    '''A class for data cleaning and imputing of input features'''

    def __init__(self, df):
        '''
        Parameters
        ----------
        df: dataframe
            The dataframe for data processing
        '''

        self.df = df.copy()
        self.unique_counts = self.df.nunique()

    def constant_values(self):
        '''Identifies constant value columns 

        Parameters
        ---------
        df: dataframe
            A raw dataframe 
        
        Returns
        ---------
        list
            a list of columns of constant values
        '''

        constant_value_columns = self.unique_counts[self.unique_counts==1].index.tolist()
        constant_values_series = pd.Series({c: self.df[c].unique() for c in self.df[constant_value_columns]})

        return constant_values_series

    def small_unique_values(self, max_num = 5):
        '''Determines columns having unique values less tahn max_num but more than 1
        
        Parameters
        ----------
        max_num: int
            Maximum number of unique values of a column
        
        Returns
        -------
        list 
            a list of columns of unique values less than max_int
        dataframe
            a dataframe of column names and unique value counts
        '''

        # unique_counts = self.df.nunique()
        small_uniquevalue_columns = self.unique_counts[(self.unique_counts>1)*(self.unique_counts<=max_num)].index.tolist()
        small_uniquevalue_series = pd.Series({c: self.df[c].unique() for c in self.df[small_uniquevalue_columns]})
        
        return small_uniquevalue_series
    
    def missing_rows_count(self):
        '''Calculates number of rows of missing data for each column

        Returns
        ------
        Series
            a series of number of rows who have missing data
        '''

        missing_sum_series = self.df.isna().sum()
        missing_sum_series = missing_sum_series[missing_sum_series >0]

        return missing_sum_series


    def data_imputation(self, df_to_impute, imputing_methods = {}):
        '''
        imputes dataframe of columns (categorical and continuous)
        
        Parameters
        ---------
        imputing_methds: dir, optional
            columns to be imputed by methods mentioned as key of the dictionary 
            e.g. dir['ffill'] = ['column1', 'column2']
        Returns 
        -------
        dataframe
            a dataframe after imputing missing values.

        '''
        imputed_df = df_to_impute.copy() 
        # cleaned_df.drop(columns_to_drop, axis = 1, inplace = True)

        # imputing columns with methods in imputing_methods 
        if (len(imputing_methods)!=0):
            for imputing_method,columns in imputing_methods.items():
                # print(imputing_method)
                imputed_df[columns] = imputed_df[columns].interpolate(method = imputing_method)
                
        return imputed_df
    
    
    def data_cleaning(self, df_to_clean, columns_to_drop = [], rows_to_drop = []):
        '''
        Dropped rows and columns 
        
        Parameters
        ----------
        columns_to_drop: list
            The columns to drop from dataframe, (default is None)
        rows_to_drop: list, optional
            List of rows to be dropped from dataframe, (default is None)
        Returns
        --------
        dataframe
            A dataframe after dropping rows and columns
        '''
        
        cleaned_df = df_to_clean.copy()
        cleaned_df.drop(columns_to_drop, axis = 1, inplace = True)
        cleaned_df.drop(rows_to_drop, axis = 0, inplace = True)

        return cleaned_df