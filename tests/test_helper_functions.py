import pytest
import pandas as pd
from src.helper_functions import dailyChanges
from src.helper_functions import smoother
from src.helper_functions import sumByDate

test_data = pd.DataFrame({v for v in range(1,11)}, index=range(10))
test_data.columns = ['val']

class TestDailyChanges(object):
    ''''''  
    def test_shape(self):
        '''Add a test'''
        applied = dailyChanges(test_data, cols=['val'])
        message = f"Expected (10,1) but got {applied.shape}" 
        assert applied.shape == (10,1), message

    def test_first_element(self):
        '''Add a test'''
        message = "The first element is not the same"
        applied = dailyChanges(test_data, cols=['val'])
        check = pd.DataFrame([1 for v in range(1,11)], index=range(10))
        assert applied.iloc[0].values == check.iloc[0].values, message
        
    def test_contents(self):
        '''Add a test'''
        applied = dailyChanges(test_data, cols=['val'])
        check = pd.DataFrame([1 for v in range(1,11)], index=range(10))
        vals = [applied.iloc[i][0] == check.iloc[i][0] for i in range(len(check))]
        message = f"Expected {check.values} but got {applied.values}" 
        assert sum(vals) == 10, message
        
    def test_column_type(self):
        '''Add a test'''
        applied = dailyChanges(test_data, cols=['val'])
        assert type(applied.columns[0]) == str
        
    def test_column_name(self):
        '''Add a test'''
        applied = dailyChanges(test_data, cols=['val'])
        assert applied.columns[0] == 'new_val'
        
class TestSmoother(object):
    ''''''   
    def test_shape(self):
        '''Add a test'''
        applied = smoother(test_data, cols=['val'])
        message = f"Expected (10,1) but got {applied.shape}" 
        assert applied.shape == (10,1), message

    def test_first_elements(self):
        '''Add a test'''
        message = "The first N-1 elements are not the same"
        applied = smoother(test_data, cols=['val'])
        assert sum(applied.iloc[i].values[0] == test_data.iloc[i].values[0] for i in range(6)) == 6, message
        
    def test_contents(self):
        '''Add a test'''
        applied = smoother(test_data, cols=['val'])
        check = pd.DataFrame([1.,2.,3.,4.,5.,6.,sum([*range(1,8)])/7,sum([*range(2,9)])/7,sum([*range(3,10)])/7,sum([*range(4,11)])/7], index=range(10))
        vals = [applied.iloc[i][0] == check.iloc[i][0] for i in range(len(check))]
        message = f"Expected {check.values} but got {applied.values}" 
        assert sum(vals) == 10, message
        
    def test_column_type(self):
        '''Add a test'''
        applied = smoother(test_data, cols=['val'])
        assert type(applied.columns[0]) == str
        
    def test_column_name(self):
        '''Add a test'''
        applied = smoother(test_data, cols=['val'])
        assert applied.columns[0] == 'average_val'
        
class TestSumByDate(object):
    ''''''
    def test_shape(self):
        dates = pd.date_range(start='1/1/2018', end='1/05/2018')
        test_data = pd.DataFrame({v for v in range(len(dates)*2)}, index=dates.append(dates))
        test_data.columns = ['val']
        assert sumByDate(test_data,['val']).shape == (5,1)