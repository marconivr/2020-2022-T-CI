"""product
"""
import os
import sys
import wmi
import sqlite3
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2020-11-20"

class product:
	def __init__ (self, folder=None, debug=False, db=True, vs=False):
		""" Where it all begins
		"""
		base_dir = "." if vs else ".." # the project "root" in Visual studio it is different

		if folder == None:
			folder = os.path.join(base_dir, "flussi")

		log = open(os.path.join(base_dir, "log", "log.log"), "a+")
		csv_names = open(os.path.join(folder, "computers.csv"), "r+")
		csv_product_history = open(os.path.join(folder, "product_history.csv"), "a+")
		csv_product = open(os.path.join(folder, "product.csv"), "w+")
		csv_unchecked = open(os.path.join(folder, "unchecked_PC.csv"), "r+").read()
		csv_unchecked2 = open(os.path.join(folder, "unchecked_PC.csv"), "w+")
		if db : db_product = sqlite3.connect(os.path.join(folder, "product.db"))
		
		product.log(log, f"Opened all files{' and database connected' if db else ' opened'}")
		
		start_time = datetime.now()
		product.log(log, f"Start time: {start_time}")
		product.log(log, "Running: product.py")
		
		# Init files and database
		intestation = "PC_name,Caption,Description,IdentifyingNumber,InstallDate,InstallLocation,Language,Name,ProductID,URLInfoAbout,URLUpdateInfo,Vendor,Version,Date_local,Date_universal_microsecond"
		intestation_unchecked = '"names","fail_reach","total_search"'
		product.init_csv(csv_product, intestation, log)
		csv_product_history.seek(0)
		if csv_product_history.read() == "" : product.init_csv(csv_product_history, intestation, log)
		if db : product.init_db(db_product.cursor(), intestation, intestation_unchecked, log, db)

		# Core
		fail = product.print_all(log, csv_names, csv_product, csv_product_history , db_product.cursor() if db else None, start_time, debug, db)
		product.update_unchecked_PC(fail, csv_unchecked, csv_unchecked2, db_product.cursor() if db else None, log, debug, db)
		
		if db and debug : product.print_db(db_product.cursor(), intestation, intestation_unchecked, log, db)

		# End
		csv_names.close()
		csv_product.close()
		csv_product_history.close()
		csv_unchecked2.close()
		if db : db_product.commit()
		product.log(log, f"End time: {datetime.now()}\nTotal time: {datetime.now() - start_time}")
		product.log(log, "")
		log.close()

	def print_all(log, csv_names, csv_product, csv_product_history, db_product, start_time, debug=False, db=True):
		"""Prints the infos by Win32_Product
		"""
		fail = []
		for PC_name in ("My PC, debug option",) if debug else csv_names.read().split("\n")[1:]:
			try:
				if product.check_PC("localhost" if debug else PC_name):			
					conn = wmi.WMI("." if debug else PC_name)
					product.print_and_log(log, f" - {PC_name}", debug)

					for product_infos in conn.Win32_Product(["Caption", "Description", "IdentifyingNumber", "InstallDate", "InstallLocation", "Language", "Name", "ProductID", "URLInfoAbout", "URLUpdateInfo", "Vendor", "Version"]):
						data = f"'{'localhost' if debug else PC_name}','{product_infos.Caption}','{product_infos.Description}','{product_infos.IdentifyingNumber}','{product_infos.InstallDate}','{product_infos.InstallLocation}','{product_infos.Language}','{product_infos.Name}','{product_infos.ProductID}','{product_infos.URLInfoAbout}','{product_infos.URLUpdateInfo}','{product_infos.Vendor}','{product_infos.Version}','{start_time}','{start_time.timestamp()}'"
						product.print_and_log(log, f"   - Istruction: Win32_Product => {data}", debug)

						csv_product.write(f"""{product.make_csv_standard(data).replace("'", '"')}\n""")
						csv_product_history.write(f"""{product.make_csv_standard(data).replace("'", '"')}\n""")
						if db : db_product.execute(f"INSERT INTO product VALUES ({data})")
						if db : db_product.execute(f"INSERT INTO product_history VALUES ({data})")
				else:
					fail.append(PC_name)
			except:
				pass

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
		data.replace("-", "")
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
		product.log(file, item)

	def init_db(db_product, intestation, intestation_unchecked, log, db=True):
		"""Init the database
		"""
		if db : db_product.execute(f'''CREATE TABLE IF NOT EXISTS product ({intestation})''')
		if db : db_product.execute(f'''DELETE FROM product''')

		if db : db_product.execute(f'''CREATE TABLE IF NOT EXISTS product_history ({intestation})''')

		if db : db_product.execute(f'''CREATE TABLE IF NOT EXISTS unchecked_PC ({intestation_unchecked})''')
		if db : db_product.execute(f'''DELETE FROM unchecked_PC''')
		
		product.log(log, "database now initialized")

	def init_csv(flie, intestation, log):
		"""Init the csv files
		"""
		flie.write(f"{intestation}\n")
		product.log(log, "csv now initialized")

	def print_db(db_file, intestation, intestation_unchecked, log, debug, tablename_main="product", tablename_history="product_history", tablename_unchecked="unchecked_PC"):
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
		last = product.csv2array(csv_unchecked_PC[:-1:])
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
		csv_out.write(product.array2csv(array))

		# Update db
		if db : db_unchecked_PC.executemany('INSERT INTO unchecked_PC VALUES (?,?,?)', array[1::])

		product.log(log, "Unchecked updated")

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
	db = False

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

	product(folder, debug, db, vs)
