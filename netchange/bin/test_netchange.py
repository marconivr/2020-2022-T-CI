"""Test netchange file
"""
from netchange import *

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2020-11-2"

def test():
	"""Tests the netchange function in the netchange class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert netchange.netchange() == "netchange", "test failed"
	#assert netchange.<function>(<values>) == <the result(s) you would like to have>, "<the fail message>"
	
if __name__ == "__main__":
	test()
