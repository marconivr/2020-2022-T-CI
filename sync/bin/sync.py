"""sync
"""
import os
import sys
import pymysql
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "01.03 2021-01-14"

class sync:
	def __init__ (self, agent=False, sync_DB=True, input_folder=None, output_folder=None, debug=False,):
		"""Where it all begins
		"""

		#Setup basic variabiles
		self.start_time = datetime.now()
		self.debug = debug
		self.agent = agent
		self.sync_DB = sync_DB

		# Open log
		self.log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", f"{self.start_time.strftime('%Y%m%d')}sync.log"), "a+")
		self.log.write("Execution_code,Message,user_friendly_time,time")
		self.print(f"Start")
		self.print("Running: sync.py")

		if input_folder == None:
			self.input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi")
		else:
			self.input_folder = input_folder

		if output_folder == None:
			self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi", "cloned")
		else:
			self.output_folder = output_folder

		self.print("Variabiles setted")

		# Read the config controller
		self.local_files = open(os.path.join(self.input_folder, "file_to_upload_and_where.csv"), "r").read()
		try:
			if self.sync_DB : self.config = eval(open(os.path.join(self.input_folder, "settings.json"), "r").read())
			if self.sync_DB : self.print(str(self.config))

			if (not self.agent or (self.agent and not self.sync_DB)):
				self.copy()	# Copy to the wanted folder

			if self.sync_DB:
				# Sync online if possible
				try:
					self.online_sync_all()
				except:
					self.print("Internet/ DB(s) not avariable")
		except:
			print("Error reading setting.json file, make sure it is in the input_folder and have correct syntax")
		
		# End
		self.print(f"End time: {datetime.now()}")
		self.print(f"Total time (python): {datetime.now() - self.start_time}")
		self.log.close()

	def copy(self):
		""" Copy all files in flussi input_folder
		"""
		try:
			for line in sync.csv2array(self.local_files)[1:]:
				file_path = line[0] + line[1]
				open(os.path.join(self.output_folder, f"""{sync.PC_name()}_{line[1]}"""), "w+").write(open(file_path).read())

			self.print("All files copied offline")
		except:
			self.print("Nothing to copy offline")

	def make_csv_standard(data):
		"""Convert my text in csv standard to prevent errors
		Reference: https://tools.ietf.org/html/rfc4180
		"""
		data.replace(",", "%x2C").replace("}%x2C{", "},{")	# make sure extra commas
		data.replace("\"", "%x22").replace("%x22", "\"", 1).replace("%x22", "\"") # make sure extra double commas
		data.replace("'", '"') # Use " and not ', as csv standard
		data.encode("ASCII")
		return data

	def print(self, item):
		"""Writes on the screen and in the log file
		"""
		if self.debug : print(item)
		self.log.write(f""""{self.start_time.timestamp()}","{item}","{str(datetime.now())}","{datetime.now().timestamp()}"\n""")

	def PC_name():
		""" Return the PC user-name in standard mode
		"""
		try:
			return os.getlogin().replace(" ", "_")
		except:
			return "PCname"
		
	def csv2array(csv):
		""" Converts csv file to a py array
		"""
		array = []
		item_valid = True

		for line in csv.split("\n"):
			temp = []
			item = ""
			for char in (line + ","):
				if char == "," and item_valid:
					temp.append(item.replace("\\\\", "\\"))
					item = ""
				elif char == '"':
					if item_valid:
						item_valid = False
					else:
						item_valid = True
				else:
					item += char

			if len(temp) > 1:
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

	def online_sync_all(self):
		""" If possible update all
		"""
		# Get files to upload
		files = []
		for (dirpath, dirnames, filenames) in os.walk(self.output_folder):
			files = filenames
			break
		while "test.csv" in files: files.remove("test.csv") 

		for i, file in enumerate(files):
			self.print(f" - {i}° File")
			
			# Get configuration
			self.sync_online_single(file, i, tablename=file.replace(".csv", ""))

	def sync_online_single(self, file, i, tablename):
		""" Sync a single file
		"""
		# Connenct to the DB for every file
		connection = pymysql.connect(self.config['host'], self.config['username'], self.config['password'], self.config['database'], int(self.config['port']))
		self.print(f"   - Connected {i}° database for {tablename} table")

		with connection.cursor() as cursor:
			file_to_sync = sync.csv2array(open(os.path.join(self.output_folder, file), "r").read())
			self.print(open(os.path.join(self.output_folder, file), "r").read())
			self.print(f"   - File to sync readed ({file}): {file_to_sync}")
				
			# If not exist create database
			variabiles = sync.array2csv([[f"""{a.replace(' ', '_')}""" for a in file_to_sync[0]],]).replace('""', '"').replace('"', '').replace('\n', '').replace('\\', '').replace('/', '')
			self.print(f"   - Variabiles = {variabiles}")

			try:
				cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.config['database']}.{tablename} (ID int AUTO_INCREMENT,{str([i+' varchar(255),' for i in variabiles.split(",")])[1:-1].replace("', '", "")[1:-2]},PRIMARY KEY (ID));""")
			except:
				cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tablename} (ID int AUTO_INCREMENT,{str([i+' varchar(255),' for i in variabiles.split(",")])[1:-1].replace("', '", "")[1:-2]},PRIMARY KEY (ID));""")
			self.print(f"   - Connected {tablename} table")

			# Add all new items
			for j, items in enumerate(file_to_sync[1:]):
				items = sync.array2csv([items,])[:-1:]

				try:
					cursor.execute(f"SELECT * FROM {self.config['database']}.{tablename} WHERE ({variabiles}) = ({items});")
				except:
					cursor.execute(f"SELECT * FROM {tablename} WHERE ({variabiles}) = ({items});")
				self.print(f"     - Read if already exists {items}")

				if len(cursor.fetchall()) == 0: # If not exist add it
					try:
						cursor.execute(f"INSERT INTO {self.config['database']}.{tablename} ({variabiles}) VALUES ({items});")
					except:
						cursor.execute(f"INSERT INTO {tablename} ({variabiles}) VALUES ({items});")
					self.print(f"   - Values added ({items})")
				self.print(f"     - Added {items}")

		# Push changes
		connection.commit()
		connection.close()
		self.print("Ended single connection")

if __name__ == "__main__":
	# Check if user needs an help
	if "-h" in sys.argv or "--help" in sys.argv:
			documentation = ["usage sync",
							"\t[--agent | -a]",
							"\t[--agentless | -al]",
							"\t[--batch | -b]",
							"\t[--debug | -d]",
							"\t[--sync | -s]",
							"\t[--nsync | -ns]",
							"\t[--input_folder= | -if=]",
							"\t[--output_folder= | -of=]",
							"",
							"These are the sync flags:",
							"\t--agent | -a					Run in the Agent mode",
							"\t--agentless | -al			\tRun in the Agentless mode or Run as the core manager of the Agent structure",
							"\t--batch | -b					Setting for the batch file",
							"\t--debug | -d					Choose this if you want debug option (for eg. you can see the output on the screen)",
							"\t--sync | -s					Try to sync online",
							"\t--nsync | -ns				Don't sync online",
							"",
							"These are the sync setting:",
							"\t--input_folder= | -if=		\t\t(OPTIONAL) You can choose the input file",
							"\t--output_folder= | -of=		\t\t(OPTIONAL) You can choose the output file",
							"",
							"Extra:",
							"\t--help or -h					You can see the documentation",
							"",
							"Made with ❤  by Castellani Davide (@DavideC03)",
							""]

			for line in documentation:
				print(line)
	else:
		# default values flag
		debug = True
		agent = False # if Talse is agentless
		input_folder = None
		output_folder = None
		sync_DB = True

		# Check inputs
		for arg in sys.argv:
			if "--agent" in arg or "-a" in arg:
				agent = True

			if "--agentless" in arg or "-al" in arg:
				agent = False

			if "--batch" in arg or "-b" in arg:
				debug = False

			if "--debug" in arg or "-d" in arg:
				debug = True

			if "--sync" in arg or "-s" in arg:
				sync_DB = True

			if "--nsync" in arg or "-ns" in arg:
				sync_DB = False

			if "--input_folder=" in arg or "-if=" in arg:
				input_folder = arg.replace("--input_folder=", "").replace("-if=", "")

			if "--output_folder=" in arg or "-of=" in arg:
				output_folder = arg.replace("--output_folder=", "").replace("-of=", "")

		try:
			sync(agent=agent, sync_DB=sync_DB, input_folder=input_folder, output_folder=output_folder, debug=debug)
		except:
			raise Exception("There is an error, make sure you have made done all settings.")
