"""usb
"""
import os
import sys
import sqlite3
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "01.03 2020-10-15"

class usb:
	def __init__ (self, debug=False, db=True, vs=False, folder=None):
		"""Where it all begins
		"""
		base_dir = "." if vs else ".." # the project "root" in Visual studio it is different

		if folder == None:
			folder = os.path.join(base_dir, "flussi")

		log = open(os.path.join(base_dir, "log", "trace.log"), "a+")
		csv_temp = open(os.path.join(folder, "temp.csv"), "r+")
		csv_usb_last = open(os.path.join(folder, "usb.csv"), "r+").read()
		csv_usb = open(os.path.join(folder, "usb.csv"), "w+")
		last_user_last = open(os.path.join(folder, "lastUser.txt"), "r+").read()
		last_user = open(os.path.join(folder, "lastUser.txt"), "w+")
		if db : db_usb = sqlite3.connect(os.path.join(folder, "usb.db"))
		
		usb.log(log, f"Opened all files{' and database connected' if db else ' opened'}")
		
		start_time = datetime.now()
		usb.log(log, f"Start time (python): {start_time}")
		usb.log(log, "Running: usb.py")
		
		# Init files and database
		intestation = "'Last User','Device Name','Description','Device Type','Connected','Safe To Unplug','Disabled','USB Hub','Drive Letter','Serial Number','Created Date','Last Plug/Unplug Date','VendorID','ProductID','Firmware Revision','USB Class','USB SubClass','USB Protocol','Hub / Port','Computer Name','Vendor Name','Product Name','ParentId Prefix','Service Name','Service Description','Driver Filename','Device Class','Device Mfg','Power','USB Version','Driver Description','Driver Version','Instance ID'"
		usb.init_csv(csv_usb, intestation.replace("'", '"'), log)
		if db : usb.init_db(db_usb.cursor(), intestation.replace("'", '"'), log, db)

		# Core
		clean_array = usb.filter(usb.csv2array(csv_temp.read()))
		usb.print_and_log(log, "Delate unwanted items", debug)

		usb.save_all(clean_array, csv_usb, usb.csv2array(csv_usb_last), last_user_last.replace("\n", ""), db, None if not db else db_usb) 
		usb.print_and_log(log, "Salved items", debug)

		usb.save_current_username(last_user)
		
		if db and debug : usb.print_db(db_usb.cursor(), intestation, log, db)

		# End
		if db : db_usb.commit()
		csv_usb.close()
		last_user.close()
		usb.log(log, f"End time: {datetime.now()}\nTotal time (python): {datetime.now() - start_time}")
		if debug : usb.log(log, "")
		log.close()

	def filter(array, unwanted_value=("HID (Human Interface Device)",)):
		""" Filter my value
		"""
		delate_array = []

		for i, line in enumerate(array):
			delate_line = False
			for item in line:
				if item in unwanted_value:	# Check if value is unwanted
					delate_line = True

			if delate_line:					# If value is unwanted insert it into a "black list"
				delate_array.append(i)

		for item_to_delate in delate_array[::-1]:
			array.pop(item_to_delate)

		return array
		
	def save_all(array, csv_usb, csv_usb_last_array, last_user, db=False, db_usb=None):
		""" Salve all info into a csv and (optional) db
		"""
		pseudo_csv_usb_last_array = []
		for line in csv_usb_last_array:
			temp = []
			for item in line[1:]:
				temp.append(item.replace("\\\\", "\\").replace("\\\\", "\\"))
			pseudo_csv_usb_last_array.append(temp)

		for line in array:
			if line in pseudo_csv_usb_last_array:
				line = f"""{str(csv_usb_last_array[pseudo_csv_usb_last_array.index(line)])[1:-1].replace(", ", ",").replace("'", '"')}"""
			else:
				line = f""""{last_user}",{str(line)[1:-1].replace(", ", ",").replace("'", '"')}"""

			if db : db_usb.execute(f"INSERT INTO usb VALUES ({line})")
			csv_usb.write(f"{line}\n")

	def make_csv_standard(data):
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
		usb.log(file, item)

	def init_db(db_usb, intestation, log, db=True):
		"""Init the database
		"""
		if db : db_usb.execute(f'''CREATE TABLE IF NOT EXISTS usb ({intestation})''')
		if db : db_usb.execute(f'''DELETE FROM usb''')
		
		usb.log(log, "database now initialized")

	def init_csv(flie, intestation, log):
		"""Init the csv files
		"""
		flie.write(f"{intestation}\n")
		usb.log(log, "csv now initialized")

	def print_db(db_file, intestation, log, debug, tablename_main="usb"):
		"""Checks the database content
		"""
		# Main content
		if debug : print("\nDatabase main content:")
		if debug : print(intestation.replace("\\\\", "\\"))

		for row in db_file.execute(f"SELECT * FROM {tablename_main}").fetchall():
			if debug : print(str(row)[1:-1].replace("'", "").replace("\\\\", "\\").replace("\\\\", "\\"))
		
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

	def save_current_username(file):
		""" Save current username for the next time
		"""
		file.write(os.getlogin())

if __name__ == "__main__":
	# debug flag
	debug = True

	# visual studio flag
	vs = True

	# database flag
	db = True

	# check if is launched by .bat file
	if "--batch" in sys.argv or "-b" in sys.argv:
		debug = False
		vs = False

	# select folder
	folder = None
	for arg in sys.argv:
		if "--folder=" in arg or "-f=" in arg:
			folder = arg.replace("--folder=", "").replace("-f=", "")

	usb(debug, db, vs, folder)
