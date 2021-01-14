"""agent
"""

import os
import sys
import wmi
from datetime import datetime
from ipaddress import ip_address, IPv4Address
import requests
import string

__author__ = "help@castellanidavide.it"
__version__ = "01.03 2021-01-14"

class agent:
	def __init__ (self, folder=None, debug=False, vs=False, parts=["osversion", "netinfo", "eventsview", "product"]):
		""" Where it all begins
		"""
		#Setup basic variabiles
		self.start_time = datetime.now()
		self.debug = debug
		self.vs = vs
		self.parts = parts
		while (None in self.parts): self.parts.remove(None)

		if folder == None:
			self.folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi")
		else:
			self.folder = folder

		try:
			open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", f"{self.start_time.strftime('%Y%m%d')}agent.log"), "r+").read()
			self.log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", f"{self.start_time.strftime('%Y%m%d')}agent.log"), "a+")
		except:
			self.log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", f"{self.start_time.strftime('%Y%m%d')}agent.log"), "a+")
			self.initlog()

		self.csv_names = open(os.path.join(self.folder, "computers.csv"), "r+")
		self.csv_agent_history = {}
		self.csv_agent = {}
		for i in parts:
			self.csv_agent_history[i] = open(os.path.join(self.folder, f"{i}_history.csv"), "a+")
			self.csv_agent_history[i].seek(0)
			self.csv_agent[i] = open(os.path.join(self.folder, f"{i}.csv"), "w+")
		self.csv_unchecked = open(os.path.join(self.folder, "unchecked_PC.csv"), "r+").read()
		self.csv_unchecked2 = open(os.path.join(self.folder, "unchecked_PC.csv"), "w+")
				
		self.print(f"Start")
		self.print(f"Opened all files")
		self.print("Running: agent.py")		
		
		# Init files
		self.init_csv()

		# Core
		agent.print_all(self)
		agent.update_unchecked_PC(self)

		# End
		self.csv_names.close()
		for i in parts:
			self.csv_agent[i].close()
			self.csv_agent_history[i].close()
		self.csv_unchecked2.close()
		self.print(f"End time")
		self.print(f"Total time: {datetime.now() - self.start_time}")
		self.log.close()

	def print_all(self):
		"""Prints the infos by Win32_agent
		"""
		self.fail = []

		self.print("- Run core")
		for PC_name in ("My PC, debug option",) if self.debug else self.csv_names.read().split("\n")[1:]:
			if agent.check_PC("localhost" if self.debug else PC_name):			
				conn = wmi.WMI("." if self.debug else PC_name)
				self.print(f" - {PC_name}")

				for i in self.parts:
					if i == "osversion":
						self.print("  - Istructions: Win32_OperatingSystem")
						for os_info in conn.Win32_OperatingSystem(["Caption", "Version"]):
							data = f"'{'My PC' if self.debug else PC_name}','{os_info.Caption}','{os_info.Version}','{datetime.now()}','{int(datetime.utcnow().timestamp() * 10 ** 6)}'\n"
							self.csv_agent["osversion"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
							self.csv_agent_history["osversion"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")

					elif i == "netinfo":
						self.MACsep = '-'
						self.print("  - Istructions: Win32_NetworkClient && Win32_NetworkProtocol")
						for network_client, network_protocol, other in zip(conn.Win32_NetworkClient(["Caption", "Description", "Status", "Manufacturer", "Name"]), conn.Win32_NetworkProtocol(["GuaranteesDelivery", "GuaranteesSequencing", "MaximumAddressSize", "MaximumMessageSize", "SupportsConnectData", "SupportsEncryption", "SupportsEncryption", "SupportsGracefulClosing", "SupportsGuaranteedBandwidth", "SupportsQualityofService"]), conn.Win32_NetworkAdapterConfiguration(["DNSDomain", "DHCPEnabled", "DefaultIPGateway", "MACAddress"], IPEnabled=True)):
							try:
								for i in range(len(other.DefaultIPGateway)):
									data = f"""'{'My PC' if self.debug else PC_name}','{network_client.Caption}','{network_client.Description}','{network_client.Status}','{network_client.Manufacturer}','{network_client.Name}','{network_protocol.GuaranteesDelivery}','{network_protocol.GuaranteesSequencing}','{network_protocol.MaximumAddressSize}','{network_protocol.MaximumMessageSize}','{network_protocol.SupportsConnectData}','{network_protocol.SupportsEncryption}','{network_protocol.SupportsGracefulClosing}','{network_protocol.SupportsGuaranteedBandwidth}','{network_protocol.SupportsQualityofService}','{other.DNSDomain}','{other.DHCPEnabled}','{"IPv4" if type(ip_address(other.DefaultIPGateway[i])) is IPv4Address else "IPv6"}','{other.DefaultIPGateway[i] if type(ip_address(other.DefaultIPGateway[i])) is IPv4Address else self.MACnormalization(other.DefaultIPGateway[i])}','{self.MACnormalization(other.MACAddress)}','{requests.get(f"http://macvendors.co/api/{other.MACAddress}").json()['result']['company']}','{datetime.now()}','{int(datetime.utcnow().timestamp() * 10 ** 6)}'\n"""
									self.csv_agent["netinfo"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
									self.csv_agent_history["netinfo"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
							except:
								pass

					elif i == "eventsview":
						self.print("  - Istruction: Win32_NTLogEvent")
						for events_view in conn.Win32_NTLogEvent(['ComputerName ', 'User', 'Category', 'Type', 'CategoryString', 'EventCode', 'EventIdentifier', 'EventType', 'Logfile', 'RecordNumber'], type="Error"):
							data = f"'{'My PC' if self.debug else PC_name}','{events_view.User}','{events_view.Category}','{events_view.Type}','{events_view.CategoryString}','{events_view.EventCode}','{events_view.EventIdentifier}','{events_view.EventType}','{events_view.Logfile}','{events_view.RecordNumber}','{self.start_time}','{self.start_time.timestamp()}'\n"
							self.csv_agent["eventsview"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
							self.csv_agent_history["eventsview"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
		
					elif i == "product":
						self.print("  - Istruction: Win32_Product")
						for product_infos in conn.Win32_Product(["Caption", "Description", "IdentifyingNumber", "InstallDate", "InstallLocation", "Language", "Name", "ProductID", "URLInfoAbout", "URLUpdateInfo", "Vendor", "Version"]):
							data = f"'{'My PC' if self.debug else PC_name}','{product_infos.Caption}','{product_infos.Description}','{product_infos.IdentifyingNumber}','{product_infos.InstallDate}','{product_infos.InstallLocation}','{product_infos.Language}','{product_infos.Name}','{product_infos.ProductID}','{product_infos.URLInfoAbout}','{product_infos.URLUpdateInfo}','{product_infos.Vendor}','{product_infos.Version}','{self.start_time}','{self.start_time.timestamp()}'\n"
							self.csv_agent["product"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
							self.csv_agent_history["product"].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")

			else:
				self.fail.append(PC_name)

	def check_PC(PC_name, n_test=2):
		"""Checks if PC is disponible
		"""
		respond = os.popen(f"PING -n {n_test} {PC_name}").read()	# Windows
		respond += os.popen(f"PING -i {n_test} {PC_name}").read()	# Linux

		return "ms" in respond

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

	def initlog(self):
		"""Writes on the screen and in the log file
		"""
		self.log.write("Execution_code,Message,user_friendly_time,time")

	def print(self, item):
		"""Writes on the screen and in the log file
		"""
		if self.debug : print(item)
		self.log.write(f""""{self.start_time.timestamp()}","{item}","{str(datetime.now())}","{datetime.now().timestamp()}"\n""")

	def init_csv(self, intestations={"osversion": "PC_name, OS, OS_version,Date_local,Date_universal_microsecond", "netinfo": "PCname,Caption,Description,Status,Manufacturer,Name,GuaranteesDelivery,GuaranteesSequencing,MaximumAddressSize,MaximumMessageSize,SupportsConnectData,SupportsEncryption,SupportsGracefulClosing,SupportsGuaranteedBandwidth,SupportsQualityofService,DNSDomain,DHCPEnabled,IP_Type,DefaultIPGateway,MACAddress,MACAdress_company,Date_local,Date_universal_microsecond", "eventsview": "PCname,User,Category,Type,CategoryString,EventCode,EventIdentifier,EventType,Logfile,RecordNumber,Date_local,Date_universal_microsecond", "product": "PC_name,Caption,Description,IdentifyingNumber,InstallDate,InstallLocation,Language,Name,ProductID,URLInfoAbout,URLUpdateInfo,Vendor,Version,Date_local,Date_universal_microsecond"}):
		"""Init the csv files
		"""
		self.print("- Inizialize files")

		self.csv_unchecked2.write('"names","fail_reach","total_search"\n')
		self.print("- Inizialized csv_unchecked2")

		for i in self.parts:
			self.print(f"- Inizialize {i} file")
			if self.csv_agent_history[i].read() == "":
				self.csv_agent_history[i].write(f"{intestations[i]}\n")
				self.print(f"- Inizialized {i} history file")
			self.csv_agent[i].write(f"{intestations[i]}\n")
			self.print(f"- Inizialized {i} file")

	def update_unchecked_PC(self):
		""" Update unchecked PC
		"""
		# Make my updated array
		last = agent.csv2array(self.csv_unchecked[:-1:])
		array = []

		array.append(last[0]) # Add intestation

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
		self.csv_unchecked2.write(agent.array2csv(array))

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
	debug = True

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

	# choose the module
	parts=["osversion", "netinfo", "eventsview", "product"]
	for arg in sys.argv:
		if "--module=" in arg or "-m=" in arg:
			parts = [arg.replace("--module=", "").replace("-m=", ""), ]

	if(agent(folder, debug, vs, parts) == None): print("Done")
