"""Test macaddresssep file
"""
from macaddresssep import *

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2020-11-23"

def test():
	"""Tests the macaddresssep function in the macaddresssep class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert macaddresssep.csv2array("'test','test'\n'example value','example value 2'\n'example value','example value 2'\n'example value','example value 2'") == [["'test'","'test'"], ["'example value'","'example value 2'"], ["'example value'","'example value 2'"], ["'example value'","'example value 2'"]], "CSV2Array fails (personal_code: 3a)"
	
	assert macaddresssep.array2csv([["test","test"], ["example value","example value 2"], ["example value","example value 2"], ["example value","example value 2"]]) == '"test","test"\n"example value","example value 2"\n"example value","example value 2"\n"example value","example value 2"\n', "Array2CSV fails (personal_code: 3b)"

	assert macaddresssep(), "test failed (personal_code: 0)" # check all code
	#assert macaddresssep.<function>(<values>) == <the result(s) you would like to have>, "<the fail message>"
	
if __name__ == "__main__":
	test()
