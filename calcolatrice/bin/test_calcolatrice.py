"""Test calcolatrice file
"""
import calcolatrice

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2021-2-12"

def test():
	"""Tests the calcolatrice function in the calcolatrice class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert calcolatrice.__author__ == "help@castellanidavide.it", "sanity test failed"
	#assert calcolatrice.<function>(<values>) == <the result(s) you would like to have>, "<the fail message>"
	
if __name__ == "__main__":
	test()
