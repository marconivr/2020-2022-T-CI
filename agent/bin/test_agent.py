"""Test agent file
"""
from agent import *

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2020-11-30"

def test():
	"""Tests the agent function in the agent class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert agent.check_PC("localhost", 1) == True, "Checker PC fails (personal_code: 1)"
	assert agent.check_PC("localhost", 2) == True, "Checker PC fails (personal_code: 1)"
	assert agent.check_PC("localhost", 10) == True, "Checker PC fails (personal_code: 1)"

	assert agent.make_csv_standard("'test','test'\n'example value','example value 2'\n'example value','example value 2'\n'example value','example value 2'") == "'test','test'\n'example value','example value 2'\n'example value','example value 2'\n'example value','example value 2'", "Maker CSV standard fails (personal_code: 2)"

	assert agent.csv2array("'test','test'\n'example value','example value 2'\n'example value','example value 2'\n'example value','example value 2'") == [["'test'","'test'"], ["'example value'","'example value 2'"], ["'example value'","'example value 2'"], ["'example value'","'example value 2'"]], "CSV2Array fails (personal_code: 3a)"
	
	assert agent.array2csv([["test","test"], ["example value","example value 2"], ["example value","example value 2"], ["example value","example value 2"]]) == '"test","test"\n"example value","example value 2"\n"example value","example value 2"\n"example value","example value 2"\n', "Array2CSV fails (personal_code: 3b)"

	assert agent(parts=["osversion", ], vs=True) != 1, "test failed (personal_code: 0)" # check all code
	assert agent(parts=["netinfo", ], vs=True) != 1, "test failed (personal_code: 0)" # check all code
	assert agent(parts=["eventsview", ], vs=True) != 1, "test failed (personal_code: 0)" # check all code
	assert agent(parts=["product", ], vs=True) != 1, "test failed (personal_code: 0)" # check all code
	assert agent(vs=True) != 1, "test failed (personal_code: 0)" # check all code

	#assert agent.<function>(<values>) == <the result(s) you would like to have>, "<the fail message>"
	
if __name__ == "__main__":
	test()
