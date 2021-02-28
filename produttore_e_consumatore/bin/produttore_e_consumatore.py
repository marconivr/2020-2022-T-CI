"""produttore_e_consumatore
"""

from tabular_log import tabular_log
from os import path
from threading import Thread, Lock, active_count
from time import sleep
from random import random

__author__ = "help@castellanidavide.it"
__version__ = "2.0 2021-2-28"

class produttore_e_consumatore:
	def __init__ (self):
		"""Where it all begins
		"""
		self.setup()
		self.get_modality()
		self.run_core()
		self.end()
	
	def setup(self):
		"""Setup
		"""
		self.log = tabular_log(path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"))
		self.list_len = 100
		self.locks = [Lock()] * self.list_len
		self.values = [None] * self.list_len

		self.log.print("Setup done")

	def logo(self):
		"""Prints logo
		"""
		print("------------------------------")
		print("---produttore-&-consumatore---")
		print("------------------------------")
		self.log.print("Printed logo")

	def get_modality(self):
		"""Get the wanted modality
		"""
		modalities = [
						"Singular",
						"Linear",
						"Circular"
					]

		self.logo()
		for i, value in enumerate(modalities):
			print(f"{i+1}) {value}")

		self.choise = input("Insert your choise: ")
		self.log.print(f"Inserted {self.choise}")

		try:
			self.choise = int(self.choise)
		except:
			print("Your choise is not a number, try again")
			self.log.print("Given choise is not a number")
			self.get_modality()

		try:
			assert(self.choise - 1 in range(3))
		except:
			print("Your number is not valid, try again")
			self.log.print("Given number is not valid")
			self.get_modality()

		self.log.print(f"The selected modality is {self.choise}")

	def run_core(self):
		"""Run in the selected modality
		"""
		self.threads = []

		if self.choise == 1:
			self.threads.append(Thread(target=self.produttore, args=(0, "singular")))
			self.threads.append(Thread(target=self.consumatore, args=(0,)))
		elif self.choise == 2:
			for i in range(len(self.values)):
				self.threads.append(Thread(target=self.produttore, args=(i, f"linear #{i}")))
				self.threads.append(Thread(target=self.consumatore, args=(i,)))
		elif self.choise == 3:
			for i in range(5 * len(self.values)):
				self.threads.append(Thread(target=self.produttore, args=(i%len(self.values), f"circular #{i}")))
				self.threads.append(Thread(target=self.consumatore, args=(i%len(self.values),)))

		self.log.print("Setuped threads")

		for thread in self.threads:
			thread.start()

		self.log.print("Started threads")

		while active_count() != 1:
			pass

		self.log.print("Finished threads")
			
	def produttore(self, index, value):
		"""productor
		"""
		sleep(random() / 10)
		
		try:
			with self.locks[index]:
				assert(self.values[index] == None)
				self.values[index] = value
				print("Productor{index: " + str(index) + ", value: " + str(value) + "}")
				self.log.print("Productor{index: " + str(index) + ", value: " + str(value) + "}")
		except:
			Thread(target=self.produttore, args=(index, value)).start()
			
	def consumatore(self, index):
		"""consumator
		"""
		sleep(random() / 10)

		try:
			with self.locks[index]:
				assert(self.values[index] != None)
				print("Consumator{index: " + str(index) + ", value: " + str(self.values[index]) + "}")
				self.log.print("Consumator{index: " + str(index) + ", value: " + str(self.values[index]) + "}")
				self.values[index] = None # Reset value
		except:
			Thread(target=self.consumatore, args=(index,)).start()

	def end(self):
		"""End logo
		"""
		self.log.print("End")

		print()
		print("I hope this tool help you.")
		print("If you want see the project you can find it: https://github.com/CastellaniDavide/produttore_e_consumatore")
		print()
		print("Made w/ ❤️ by Castellani Davide")
		
if __name__ == "__main__":
	produttore_e_consumatore()
