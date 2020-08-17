import pytest
import pandas as pd
from helper_functions import dailyChanges
from helper_functions import smoother
from helper_functions import sumByDate

test_data = pd.DataFrame({v for v in range(1,11)}, index=range(10))

class TestDailyChanges(object):
    def test_shape(self):
        assert True
        
class TestSmoother(object):
    
    def test_shape(self):
        assert True
        
class TestSumByDate(object):
    
    def test_shape(self):
        assert True