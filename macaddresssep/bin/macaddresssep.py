"""macaddresssep
"""
import os
import sys
from datetime import datetime
import re

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2020-11-23"

class macaddresssep:
	def __init__ (self, folder=None, debug=False, db=True, vs=False):
		"""Where it all begins
		"""
		base_dir = "." if vs else ".." # the project "root" in Visual studio it is different

		if folder == None:
			folder = os.path.join(base_dir, "flussi")

		log = open(os.path.join(base_dir, "log", "log.log"), "a+")
		csv_in = open(os.path.join(folder, "input.csv"), "r+").read()
		csv_out = open(os.path.join(folder, "output.csv"), "w+")
		
		macaddresssep.log(log, f"Opened all files{' and database connected' if db else ' opened'}")
		
		start_time = datetime.now()
		macaddresssep.log(log, f"Start time: {start_time}")
		macaddresssep.log(log, "Running: macaddresssep.py")
		
		# Core
		csv_out.write(macaddresssep.array2csv(macaddresssep.macaddresssep(macaddresssep.csv2array(csv_in), log, debug, ":")))

		# End
		csv_out.close()
		macaddresssep.log(log, f"End time: {datetime.now()}\nTotal time: {datetime.now() - start_time}")
		macaddresssep.log(log, "")
		log.close()
		
	def make_csv_standart(data):
		"""Convert my text in csv standard to prevent errors
		Reference: https://tools.ietf.org/html/rfc4180
		"""
		data.replace(",", "%x2C").replace("}%x2C{", "},{")	# make sure extra commas
		data.replace("\"", "%x22").replace("%x22", "\"", 1).replace("%x22", "\"") # make sure extra double commas
		data.replace("'", '"') # Use " and not ', as csv standard
		data.encode("ASCII")
		return data

	def log(file, item):
		"""Writes a line in the log.log file
		"""
		file.write(f"{item}\n")

	def print_and_log(file, item, debug):
		"""Writes on the screen and in the log file
		"""
		if debug : print(item)
		macaddresssep.log(file, item)

	def csv2array(csv):
		""" Converts csv file to a py array
		"""
		array = []

		for line in csv.split("\n"):
			temp = []
			for item in line.replace(",", "','").split("','"):
				try:
					temp.append(int(item.replace('"', "")))
				except:
					temp.append(item.replace('"', ""))
			array.append(temp)

		return array

	def array2csv(array):
		""" Converts py array to a csv file
		"""
		text = ""

		for line in array:
			if len(line) > 1:
				for item in line:
					text += f'"{item}",'
				text = text[:-1:] + "\n"

		return text

	def MACnormalization(MACAddress, sep=''):
		""" Helps to nomalize the MAC address
		"""
		result = ""
		for i, c in enumerate(MACAddress.replace("-", "").replace(":", "")): # Remove all delimitators
			if i % 2 == 0 or i == 11:
				result += c
			else:
				result += c + sep

		return result
	
	def macaddresssep(input, log, debug, sep=''):
		""" The core of all
		"""
		for i in range(len(input)):
			for j in range(len(input[i])):
				if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", input[i][j].lower()): # Check if it's a MAC
					input[i][j] = macaddresssep.MACnormalization(input[i][j], sep)

		return input
		
if __name__ == "__main__":
	# debug/visual studio flag
	debug = False

	# database flag
	db = True

	# Visual Studio flag
	vs = False

	# check if is launched by .bat file
	if "--batch" in sys.argv or "-b" in sys.argv:
		debug = False
		vs = False

	# select folder
	folder = None
	for arg in sys.argv:
		if "--folder=" in arg or "-f=" in arg:
			folder = arg.replace("--folder=", "").replace("-f=", "")

	macaddresssep(folder, debug, db, vs)
