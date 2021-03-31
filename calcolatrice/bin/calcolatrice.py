"""calcolatrice
"""
import os
from threading import Thread
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2021-02-15"

class calcolatrice:
	def __init__ (self):
		"""Where it all begins
		"""
		self.setup()

		while self.operation != 0:
			self.get_numbers()
			self.calcolate()
			self.get_operation()
		self.end()

	def setup(self):
		"""Setup
		"""
		self.start_time = datetime.now()
		try:
			open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", "trace.log"), "r+").read()
			self.log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", "trace.log"), "a+")
		except:
			self.log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", "trace.log"), "a+")
			self.initlog()

		self.print_log("Setup done")

		self.get_operation()

	def initlog(self):
		"""Writes on the screen and in the log file
		"""
		self.log.write("Execution_code,Message,user_friendly_time,time")

	def print_log(self, item):
		"""Writes on the screen and in the log file
		"""
		self.log.write(f""""{self.start_time.timestamp()}","{item}","{str(datetime.now())}","{datetime.now().timestamp()}"\n""")
	
	def get_operation(self):
		"""Get the operation by the user
		"""
		operations = ["Sum",
					  "Subtraction",
					  "Product",
					  "Division"]

		print("----------------------------------")
		print("---Calculator-Castellani-Davide---")
		print("----------------------------------")
		print("0) Exit")

		for i, operation in enumerate(operations):
			print(f"{i+1}) {operation}")
		
		try:
			self.operation = int(input("Choose your operation: "))
			assert(self.operation >= 0 and self.operation < 5)
			self.print_log(f"Selected option {self.operation}")
		except:
			self.get_operation()

	def get_numbers(self, n=2):
		"""Get n° numbers
		"""
		self.numbers = []

		for i in range(n):
			temp = None

			while "int" not in str(type(temp)):
				temp = input("Insert a number: ")

				try:
					temp = int(temp)
					self.numbers.append(temp)
				except:
					print("This is not a number :(")
					
		self.print_log(f"Selected numbers: {self.numbers}")

	def calcolate(self):
		"""Run the wanted operation
		"""
		self.print_log("Calcolate")
		
		if self.operation == 1:
			self.sum()
		elif self.operation == 2:
			self.sub()
		elif self.operation == 3:
			self.prod()
		elif self.operation == 4:
			self.div()

	def sum(self, quiet=False):
		"""Do a sum between the two given numbers
		"""
		assert(len(self.numbers) == 2)

		threads = []
		for i in range(abs(self.numbers[1])):
			if self.numbers[1] > 0:
				threads.append(Thread(self.increment()))
			else:
				threads.append(Thread(self.decrement()))
				
		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

		if not quiet:
			print(f"The result is: {self.numbers[0]}")
			self.print_log(f"The result is: {self.numbers[0]}")

	def increment(self):
		"""Increment the self.number[0]
		"""
		self.numbers[0] += 1
		self.print_log("Incremented")

	def decrement(self):
		"""Decrement the self.number[0]
		"""
		self.numbers[0] -= 1
		self.print_log("Decremented")

	def sub(self, quiet=False):
		"""Do a sub between the two given numbers
		"""
		assert(len(self.numbers) == 2)

		self.numbers[1] *= -1
		self.sum(quiet)
		
	def prod(self, quiet=False):
		"""Do a product between the two given numbers
		"""
		assert(len(self.numbers) == 2)

		threads = []
		self.prod_result = 0

		for i in range(abs(self.numbers[0])):
			threads.append(Thread(self.single_molt_part()))
				
		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

		if self.numbers[0] < 0:
			self.prod_result *= -1

		if not quiet:
			print(f"The result is: {self.prod_result}")
			self.print_log(f"The result is: {self.prod_result}")
		
	def single_molt_part(self):
		"""self.numbers[0] += self.numbers[1] using sum
		"""
		mem = self.numbers[0]
		self.numbers[0] = self.prod_result
		self.sum(quiet=True)
		self.prod_result = self.numbers[0]
		self.numbers[0] = mem
		self.print_log(f"The partial result is: {self.prod_result}")

	def div(self, quiet=False):
		"""Do a division between the two given numbers
		"""
		assert(len(self.numbers) == 2)

		self.div_result = 0
		self.div_end = False
		correct = self.numbers[0] < 0 ^ self.numbers[0] < 0
		self.numbers[0] = abs(self.numbers[0])
		self.numbers[1] = abs(self.numbers[1])

		while not self.div_end:
			thread = Thread(self.single_div_part())
			thread.start()
			thread.join()

		if correct:
			self.div_result *= -1

		if not quiet:
			print(f"The result is: {self.div_result}")
			self.print_log(f"The result is: {self.div_result}")

	def single_div_part(self):
		"""self.numbers[0] += self.numbers[1] using sum
		"""
		mem = self.numbers[1]
		self.sub(quiet=True)
		self.numbers[1] = mem

		if self.numbers[0] >= 0:
			self.div_result += 1
		else:
			self.div_end = True
			
		self.print_log(f"The partial result is: {self.div_result}")

	def end(self):
		"""End logo
		"""
		self.print_log("End")

		print()
		print("I hope this tool help you.")
		print("If you want see the project you can find it: https://github.com/CastellaniDavide/calcolatrice")
		print()
		print("Made w/ ❤️ by Castellani Davide")
		
if __name__ == "__main__":
	calcolatrice()
