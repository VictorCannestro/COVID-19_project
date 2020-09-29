import pytest
import pandas as pd
from helper_functions import dailyChanges
from helper_functions import smoother
from helper_functions import sumByDate

test_data = pd.DataFrame({v for v in range(1,11)}, index=range(10))

class TestDailyChanges(object):
    '''
    A test class for use in TravisCI (Continuous Integration)
    
    Here are several assert methods for reference:
            assertEqual(a, b)           a == b
            assertNotEqual(a, b)        a != b
            assertTrue(x)              bool(x) is True
            assertFalse(x)              bool(x) is False
            assertIs(a, b)              a is b
            assertIsNot(a, b)           a is not b
            assertIsNone(x)             x is None
            assertIsNotNone(x)          x is not None
            assertIn(a, b)              a in b
            assertNotIn(a, b)           a not in b
            assertIsInstance(a, b)      isinstance(a, b)
            assertNotIsInstance(a, b)   !isinstance(a, b)
    '''
    def test_shape(self):
        '''Add a test'''
        assert False
        
class TestSmoother(object):
    
    def test_shape(self):
        '''Add a test'''
        assert False
        
class TestSumByDate(object):
    
    def test_shape(self):
        '''Add a test'''
        assert False