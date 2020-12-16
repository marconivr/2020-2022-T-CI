"""uptime
"""

import os
import sys
import wmi
from datetime import datetime
import requests
import string

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2020-12-05"

class uptime:
	def __init__ (self, folder=None, debug=False, vs=False, parts=["uptime"]):
		""" Where it all begins
		"""
		#Setup basic variabiles
		self.start_time = datetime.now()
		self.debug = debug
		self.vs = vs
		self.parts = parts
		while (None in self.parts): self.parts.remove(None)

		self.base_dir = "." if self.vs else ".." # the project "root" in Visual studio it is different

		if folder == None:
			self.folder = os.path.join(self.base_dir, "flussi")
		else:
			self.folder = folder

		self.log = open(os.path.join(self.base_dir, "log", f"trace.log"), "a+")
		self.csv_names = open(os.path.join(self.folder, "computers.csv"), "r+")
		self.csv_uptime_history = {}
		self.csv_uptime = {}
		for i in parts:
			self.csv_uptime_history[i] = open(os.path.join(self.folder, f"{i}_history.csv"), "a+")
			self.csv_uptime_history[i].seek(0)
			self.csv_uptime[i] = open(os.path.join(self.folder, f"{i}.csv"), "w+")
		self.csv_unchecked = open(os.path.join(self.folder, "unchecked_PC.csv"), "r+").read()
		self.csv_unchecked2 = open(os.path.join(self.folder, "unchecked_PC.csv"), "w+")
				
		self.print(f"Start time: {self.start_time}")
		self.print(f"Opened all files")
		self.print("Running: uptime.py")		
		
		# Init files
		self.init_csv()

		# Core
		uptime.print_all(self)
		uptime.update_unchecked_PC(self)

		# End
		self.csv_names.close()
		for i in parts:
			self.csv_uptime[i].close()
			self.csv_uptime_history[i].close()
		self.csv_unchecked2.close()
		self.print(f"End time: {datetime.now()}\n\tTotal time: {datetime.now() - self.start_time}\n")
		self.log.close()

	def print_all(self):
		"""Prints the infos by Win32_uptime
		"""
		self.fail = []

		self.print("- Run core")
		for PC_name in ("My PC, debug option",) if self.debug else self.csv_names.read().split("\n")[1:]:
			if uptime.check_PC("localhost" if self.debug else PC_name):			
				conn = wmi.WMI("." if self.debug else PC_name)
				self.print(f"\t- {PC_name}")

				for i in self.parts:
					if i == "uptime":
						self.print("\t\t- Istructions: Win32_PerfFormattedData_PerfOS_System")
						for uptime_info in conn.Win32_PerfFormattedData_PerfOS_System(["SystemUpTime"]):
							data = f"'{'My PC' if self.debug else PC_name}','{uptime_info.SystemUpTime}','{datetime.now()}','{int(datetime.utcnow().timestamp() * 10 ** 6)}'\n"
							self.csv_uptime["uptime"].write(f"""{uptime.make_csv_standard(data).replace("'", '"')}""")
							self.csv_uptime_history["uptime"].write(f"""{uptime.make_csv_standard(data).replace("'", '"')}""")
	
			else:
				self.fail.append(PC_name)

	def check_PC(PC_name, n_test=2):
		"""Checks if PC is disponible
		"""
		respond = os.popen(f"PING -n {n_test} {PC_name}").read()	# Windows
		respond += os.popen(f"PING -i {n_test} {PC_name}").read()	# Linux

		return f"Received = {n_test}" in respond

	def make_csv_standard(data):
		"""Convert my text in csv standard to prevent errors
		Reference: https://tools.ietf.org/html/rfc4180
		"""
		data.replace("-", "")
		data.replace(",", "%x2C").replace("}%x2C{", "},{")	# make sure extra commas
		data.replace("\"", "%x22").replace("%x22", "\"", 1).replace("%x22", "\"") # make sure extra double commas
		data.replace("'", '"') # Use " and not ', as csv standard
		data = ''.join(filter(lambda x: x in set(string.printable), data))
		return data

	def print(self, item):
		"""Writes on the screen and in the log file
		"""
		if self.debug : print(f"\t{item}")
		self.log.write(f"\t{item}\n")

	def init_csv(self, intestations={"uptime": "PC_name,uptime_sec,Date_local,Date_universal_microsecond"}):
		"""Init the csv files
		"""
		self.print("- Inizialize files")

		self.csv_unchecked2.write('"names","fail_reach","total_search"\n')
		self.print("\t- Inizialized csv_unchecked2")

		for i in self.parts:
			self.print(f"\t- Inizialize {i} file")
			if self.csv_uptime_history[i].read() == "":
				self.csv_uptime_history[i].write(f"{intestations[i]}\n")
				self.print(f"\t- Inizialized {i} history file")
			self.csv_uptime[i].write(f"{intestations[i]}\n")
			self.print(f"\t- Inizialized {i} file")

	def update_unchecked_PC(self):
		""" Update unchecked PC
		"""
		# Make my updated array
		last = uptime.csv2array(self.csv_unchecked[:-1:])
		array = []

		for item in last[1::]:
			if len(last) == 3:
				if item[0] in self.fail:
					array.append([item[0], int(item[1]) + 1, int(item[2]) + 1])
					self.fail.remove(item[0])
				else:
					array.append([item[0], item[1], int(item[2]) + 1])

		for item in self.fail:
			array.append([item, 1, 1])

		# Update csv
		self.csv_unchecked2.write(uptime.array2csv(array))

		self.print("Unchecked PC updated")

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
			for item in line:
				text += f'"{item}",'
			text = text[:-1:] + "\n"

		return text

	def MACnormalization(self, MACAddress):
		""" Helps to nomalize the MAC address
		"""
		result = ""
		for i, c in enumerate(MACAddress.replace("-", "").replace(":", "")): # Remove all delimitators
			if i % 2 == 0:
				result += c
			else:
				result += c + self.MACsep

		return result[:-1:]

if __name__ == "__main__":
	# debug flag
	debug = False

	# Visual Studio flag
	vs = True

	# check if is launched by .bat file
	if "--batch" in sys.argv or "-b" in sys.argv:
		debug = False
		vs = False

	# select folder
	folder = None
	for arg in sys.argv:
		if "--folder=" in arg or "-f=" in arg:
			folder = arg.replace("--folder=", "").replace("-f=", "")

	uptime(folder, debug, vs)
