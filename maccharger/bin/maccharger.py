"""maccharger
"""
import sys
from os import popen, path
from datetime import datetime
import randmac
import time

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2020-11-5"

class maccharger:
	def __init__ (self, args):
		"""Where it all begins
		"""
		start_time = datetime.now()

		# Defult values
		self.verbose = False
		self.terminal = False
		self.lastMAC = -1
		if self.lastMAC == -1 : self.lastMAC = popen(f"{'ip addr | grep ether' if maccharger.is_lnx() else 'getmac /NH'}").read().replace("    link/ether ", "").replace(" brd ff:ff:ff:ff:ff:ff", "").replace(":", "").replace("-", "")[:12:]

		if "-v" in args or "--verbose" in args:
			self.verbose = True
			try:
				args.remove("-v")
			except:
				args.remove("--verbose")

		if "-t" in args or "--terminal" in args:
			self.terminal = True
			try:
				args.remove("-t")
			except:
				args.remove("--terminal")

		self.logfile = open(path.join("..", "log", "log.log"), "a+")

		self.log(f"Start time: {start_time}")
		self.log(f"Opened all files")
		
		if (self.terminal):
			for arg in args:
				try:
					self.option = int(arg[0])
					if self.option == 1:
						self.log("Run option 1")
						self.get_MAC()
					if self.option == 2:
						self.log("Run option 2")
						self.set_MAC(arg[1:])
					if self.option == 3:
						self.log("Run option 3")
						self.set_random_MAC()
					if self.option == 4:
						self.log("Run option 4")
						self.set_MAC(self.lastMAC)
					time.sleep(1)
				except:
					pass
		else:
			self.option = -1
			while self.option != 0:
				self.gui()

		self.log(f"End time: {datetime.now()}\nTotal time: {datetime.now() - start_time}")
		self.log("")
		self.logfile.close()

	def log(self, text):
		"""Print in log file
		"""
		self.logfile.write(f"{text}\n")
		if self.verbose : print(text)

	def gui(self):
		"""My personal GUI (on termial)
		"""
		maccharger.print_istructions()
		self.option = int(input("Insert your option: "))

		if self.option == 1:
			self.log("Run option 1")
			self.get_MAC()
		if self.option == 2:
			self.log("Run option 2")
			self.set_MAC(input("Insert a new MAC Address: "))
		if self.option == 3:
			self.log("Run option 3")
			self.set_random_MAC()
		if self.option == 4:
			self.log("Run option 4")
			self.set_MAC(self.lastMAC)

	def print_istructions():
		"""Print my istructions
		"""
		options = ["===========================================",
				   "MAC CHARGER by Castellani Davide",
				   "===========================================",
				   "You can choose one of this functions",
				   "0) Exit",
				   "1) Read MAC Address",
 				   "2) Change MAC Address with a specific one",
 				   "3) Change MAC Address with a random one",
				   "4) Restore MAC Address"]

		for line in options:
			print(line)

	def is_lnx():
		"""Return True if the OS is linux, false overwise
		"""
		return sys.platform == "linux" or sys.platform == "linux2"

	def get_MAC (self):
		"""Get MAC Address
		"""
		my_MAC = popen(f"{'ip addr | grep ether' if maccharger.is_lnx() else 'getmac /NH'}").read().replace("    link/ether ", "").replace(" brd ff:ff:ff:ff:ff:ff", "").replace(":", "").replace("-", "")[:12:]
		self.log(f"{'The PC MAC Address is: ' if self.verbose == True else ''}{my_MAC}")

	def set_random_MAC (self):
		"""Set a new MAC address
		"""
		self.set_MAC(str(randmac.RandMac()).replace(":", ""))
		
	def set_MAC (self, new_MAC):
		"""Set a specific MAC Address
		"""
		self.log(f"My new MAC Addess is {new_MAC}")
		net_card = popen(f"{'ls /sys/class/net' if maccharger.is_lnx() else ''}").read().split( )[0]
		self.log(f"My net_card is: {net_card}")
		popen(f"{f'sudo ifconfig {net_card} hw ether {new_MAC}' if maccharger.is_lnx() else ''}")
		self.log(f"MAC Address changed")

	def sanity_check():
		"""My sanity check
		"""
		return __author__ == "help@castellanidavide.it"

if __name__ == "__main__":
	maccharger(sys.argv)
