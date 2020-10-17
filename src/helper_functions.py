import pandas as pd
from typing import List


def dailyChanges(dataframe: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    '''
    Args:  
        dataframe (pandas DataFrame): the input dataframe of cumulative updates. 
                                      Must be single indexed.
        cols (list): list of column labels
        
    Returns:       
        changes (pandas DataFrame): the quantized difference between daily values as the 
                                    number of new cases per day. The values should be non-
                                    negative integers and have the same shape as dataframe.
    
    Notes: Calculates array subtraction for each date in the Time Series 
           i.e.
    
           changes = df_today_values - df_yesterday_values
           
           This method utilizes the underlying numpy arrays so no for-loops are needed.
           The old method was based on elementwise subtraction via for-loop iteration:
           
           new  = [dataframe[cols].iloc[0]]
    
           # Loop over each date and take the differences
           for i in range(1, len(dataframe)):
               new.append(dataframe[cols].iloc[i] - dataframe[cols].iloc[i-1])

           # Convert new into a DataFrame the same indices as dataframe
           new_df = pd.DataFrame(data=new, index=dataframe.index)
           
    '''
    today = dataframe[cols]
    
    # 1xlen(cols) pad of zeros for first element
    pad = pd.DataFrame({k:0 for k in cols}, index=[dataframe.index[0]]) 

    # Drop the last row this means the DF stops at second to latest date
    yesterday = today.drop(today.index[-1]) 
    
    # Relabel the index so every value is dated one day ahead (needed for the subtraction later)
    yesterday.index = today.index[1:]

    # glue the zero pad to temp
    yesterday = pd.concat((pad, yesterday)) 

    # Element wise calculation of the daily changes (dates need to match up)
    changes = today - yesterday
    
    # Edit the column names to reflect the daily changes
    changes.columns = ['new_' + name for name in cols]
    
    return changes

def smoother(dataframe: pd.DataFrame, cols: List[str], N: int =7) -> pd.DataFrame:
    '''
    Args:  
    
        dataframe (pandas DataFrame): the input dataframe of cumulative updates
        cols (list): column labels
        N (int >= 0): number of days to average
        
    Returns: 
    
        new (pandas DataFrame): smoothed N-day rolling average where the first N
                                entries are the same as dataframe. Columns are
                                renamed with 'average_' appending to beginning.
    
    Notes:
    
        The old method used for-loop iteration and a generator expression
        for readibility and to save memory but wasn't a great implementation:
        https://www.python.org/dev/peps/pep-0289/
        
        new  = []  
        # Loop over each date and take the differences
        for i in range(N, len(dataframe)):       
            # Generator expression to compute the sum
            ave = sum(dataframe[cols].iloc[i-k] for k in [*range(N)]) / N
            new.append(ave)
            
        # Get the indices of the data after the initial N-days and make DataFrame
        idx = dataframe.index[N: len(dataframe)]
        calc = pd.DataFrame(data=new, index=idx)
        
        # Append the averaged data to the initial N-days
        temp = dataframe[cols].iloc[:N].append(calc)
        
    '''
    # Calculate the rolling N-day average
    calc = dataframe.rolling(N).mean()
    
    # Append the averaged data to the initial N-days
    average = dataframe[cols].iloc[:N-1].append(calc.iloc[N-1:])
    
    # Edit the column name(s) in temp to include 'average'
    average.columns = ['average_' + name for name in cols]
    
    return average

def sumByDate(dataframe: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    '''
    Args:
        dataframe (DataFrame): A dataframe with multiple entries for 
                               any single date. Must be indexed by date.
        cols (list): list of columns to consider
        
    Returns:
        aggDF (DataFrame): A dataframe with a single entry for any
                           single date, aggregated by sum
        
    Notes:
    '''
    # Get the unique dates
    idx = dataframe.index.unique()
    sumDF = pd.DataFrame(index=idx, columns=cols)
    for date in idx:
        # aggregate by sum on a single date
        sumDF.loc[date] = dataframe[cols].loc[date].sum()
    return sumDF

