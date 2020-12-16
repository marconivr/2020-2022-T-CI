"""ldisk
"""
import os
import sys
import wmi
import sqlite3
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "03.01 2020-10-24"

class ldisk:
	def __init__ (self, folder=None, debug=False, db=True, vs=False):
		""" Where it all begins
		"""
		base_dir = "." if vs else ".." # the project "root" in Visual studio it is different

		if folder == None:
			folder = os.path.join(base_dir, "flussi")

		log = open(os.path.join(base_dir, "log", "log.log"), "a+")
		csv_names = open(os.path.join(folder, "computers.csv"), "r+")
		csv_ldisk_history = open(os.path.join(folder, "ldisk_history.csv"), "a+")
		csv_ldisk = open(os.path.join(folder, "ldisk.csv"), "w+")
		csv_unchecked = open(os.path.join(folder, "unchecked_PC.csv"), "r+").read()
		csv_unchecked2 = open(os.path.join(folder, "unchecked_PC.csv"), "w+")
		if db : db_ldisk = sqlite3.connect(os.path.join(folder, "ldisk.db"))
		
		ldisk.log(log, f"Opened all files{' and database connected' if db else ' opened'}")
		
		start_time = datetime.now()
		ldisk.log(log, f"Start time: {start_time}")
		ldisk.log(log, "Running: ldisk.py")
		
		# Init files and database
		intestation = "PCname,Caption,Description,DriveType,FileSystem,Name,VolumeName,FreeSpace,Size,NumberOfBlocks,Status,Date_local,Date_universal_microsecond"
		intestation_unchecked = '"names","fail_reach","total_search"'
		ldisk.init_csv(csv_ldisk, intestation, log)
		csv_ldisk_history.seek(0)
		if csv_ldisk_history.read() == "" : ldisk.init_csv(csv_ldisk_history, intestation, log)
		if db : ldisk.init_db(db_ldisk.cursor(), intestation, intestation_unchecked, log, db)

		# Core
		fail = ldisk.print_all(log, csv_names, csv_ldisk, csv_ldisk_history , db_ldisk.cursor() if db else None, start_time, debug, db)
		ldisk.update_unchecked_PC(fail, csv_unchecked, csv_unchecked2, db_ldisk.cursor() if db else None, log, debug, db)
		
		if db and debug : ldisk.print_db(db_ldisk.cursor(), intestation, intestation_unchecked, log, db)

		# End
		csv_names.close()
		csv_ldisk.close()
		csv_ldisk_history.close()
		csv_unchecked2.close()
		if db : db_ldisk.commit()
		ldisk.log(log, f"End time: {datetime.now()}\nTotal time: {datetime.now() - start_time}")
		ldisk.log(log, "")
		log.close()

	def print_all(log, csv_names, csv_ldisk, csv_ldisk_history, db_ldisk, start_time, debug=False, db=True, drivetype_array=["0 -> Unknown", "1 -> No Root Directory", "2 -> Removable Disk", "3 -> Local Disk", "4 -> Network Drive", "5 -> Compact Disc", "6 -> RAM Disk"]):
		"""Prints the infos by Win32_NetworkClient & Win32_NetworkProtocol
		"""
		fail = []
		for PC_name in ("My PC, debug option",) if debug else csv_names.read().split("\n")[1:]:

			if ldisk.check_PC("localhost" if debug else PC_name):			
				conn = wmi.WMI("." if debug else PC_name)
				ldisk.print_and_log(log, f" - {PC_name}", debug)

				for logical_disk in conn.Win32_LogicalDisk(["Caption", "Description", "DriveType", "FileSystem", "Name", "VolumeName", "FreeSpace", "Size", "NumberOfBlocks", "Status"]):
					ldisk.print_and_log(log, "   - Istruction: Win32_LogicalDisk", debug)
					data = f"'{'localhost' if debug else PC_name}','{logical_disk.Caption}','{logical_disk.Description}','{drivetype_array[int(logical_disk.DriveType)]}','{logical_disk.FileSystem}','{logical_disk.Name}','{logical_disk.VolumeName}','{logical_disk.FreeSpace}','{logical_disk.Size}','{logical_disk.NumberOfBlocks}','{logical_disk.Status}','{start_time}','{start_time.timestamp()}'"

					csv_ldisk.write(f"""{ldisk.make_csv_standard(data).replace("'", '"')}\n""")
					csv_ldisk_history.write(f"""{ldisk.make_csv_standard(data).replace("'", '"')}\n""")
					if db : db_ldisk.execute(f"INSERT INTO ldisk VALUES ({data})")
					if db : db_ldisk.execute(f"INSERT INTO ldisk_history VALUES ({data})")
			else:
				fail.append(PC_name)

		return fail

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
		ldisk.log(file, item)

	def init_db(db_ldisk, intestation, intestation_unchecked, log, db=True):
		"""Init the database
		"""
		if db : db_ldisk.execute(f'''CREATE TABLE IF NOT EXISTS ldisk ({intestation})''')
		if db : db_ldisk.execute(f'''DELETE FROM ldisk''')

		if db : db_ldisk.execute(f'''CREATE TABLE IF NOT EXISTS ldisk_history ({intestation})''')

		if db : db_ldisk.execute(f'''CREATE TABLE IF NOT EXISTS unchecked_PC ({intestation_unchecked})''')
		if db : db_ldisk.execute(f'''DELETE FROM unchecked_PC''')
		
		ldisk.log(log, "database now initialized")

	def init_csv(flie, intestation, log):
		"""Init the csv files
		"""
		flie.write(f"{intestation}\n")
		ldisk.log(log, "csv now initialized")

	def print_db(db_file, intestation, intestation_unchecked, log, debug, tablename_main="ldisk", tablename_history="ldisk_history", tablename_unchecked="unchecked_PC"):
		"""Checks the database content
		"""
		# Main content
		if debug : print("\nDatabase main content:")
		if debug : print(intestation)

		for row in db_file.execute(f"SELECT * FROM {tablename_main}").fetchall():
			if debug : print(str(row)[1:-1].replace("'", ""))

		# History content
		if debug : print("\n\nDatabase history content:")
		if debug : print(intestation)

		for row in db_file.execute(f"SELECT * FROM {tablename_history}").fetchall():
			if debug : print(str(row)[1:-1].replace("'", ""))

		# Unchecked content
		if debug : print("\n\nDatabase unchecked content:")
		if debug : print(intestation_unchecked)

		for row in db_file.execute(f"SELECT * FROM {tablename_unchecked}").fetchall():
			if debug : print(str(row)[1:-1].replace("'", ""))

	def update_unchecked_PC(unchecked_PCs, csv_unchecked_PC, csv_out, db_unchecked_PC, log, debug, db):
		""" Update unchecked PC
		"""
		# Make my updated array
		last = ldisk.csv2array(csv_unchecked_PC[:-1:])
		array = []

		array.append(last[0]) # Add intestation

		for item in last[1::]:
			if item[0] in unchecked_PCs:
				array.append([item[0], item[1] + 1, item[2] + 1])
				unchecked_PCs.remove(item[0])
			else:
				array.append([item[0], item[1], item[2] + 1])

		for item in unchecked_PCs:
			array.append([item, 1, 1])

		# Update csv
		csv_out.write(ldisk.array2csv(array))

		# Update db
		if db : db_unchecked_PC.executemany('INSERT INTO unchecked_PC VALUES (?,?,?)', array[1::])

		ldisk.log(log, "Unchecked updated")

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

if __name__ == "__main__":
	# debug flag
	debug = False

	# database flag
	db = True

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

	ldisk(folder, debug, db, vs)
