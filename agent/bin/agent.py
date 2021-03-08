"""agent
"""

import os
import sys
import wmi
from datetime import datetime
from ipaddress import ip_address, IPv4Address
import requests
import string
from tabular_log import tabular_log
from settings import settings
from json import loads, dumps

__author__ = "help@castellanidavide.it"
__version__ = "02.01 2021-03-08"

class agent:
	def __init__ (self):
		""" Where it all begins
		"""
		#Setup basic variabiles
		self.start_time = datetime.now()

		# Read log & settings
		self.settings = settings(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings", "settings.yaml")).read()
		self.log = tabular_log(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", f"{self.start_time.strftime('%Y%m%d')}agent.log"), "agent", verbose=self.settings['debug'])
		
		# Prepare other files
		if self.settings['folder'] == None : self.settings['folder'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi")
		print(self.settings['folder'])
		self.csv_names = open(os.path.join(self.settings['folder'], "computers.csv"), "r+")
		self.csv_agent_history = {}
		self.csv_agent = {}
		for key, value in self.settings["parts"].items():
			if value["validity"]:
				self.csv_agent_history[key] = open(os.path.join(self.settings['folder'], f"{key}_history.csv"), "a+")
				self.csv_agent_history[key].seek(0)
				self.csv_agent[key] = open(os.path.join(self.settings['folder'], f"{key}.csv"), "w+")
		self.csv_unchecked = open(os.path.join(self.settings['folder'], "unchecked_PC.csv"), "r+").read()
		self.csv_unchecked2 = open(os.path.join(self.settings['folder'], "unchecked_PC.csv"), "w+")
				
		self.log.print("Start")
		self.log.print("Opened all files")
		self.log.print("Running: agent.py")		
		
		# Init files
		self.init_csv()

		# Core
		agent.core(self)
		agent.update_unchecked_PC(self)

		# End
		self.csv_names.close()
		for key, value in self.settings["parts"].items():
			if value["validity"]:
				self.csv_agent[key].close()
				self.csv_agent_history[key].close()
		self.csv_unchecked2.close()
		self.log.print(f"End time")
		self.log.print(f"Total time: {datetime.now() - self.start_time}")

	def write_data(self, part, data):
		""" Write the same data into the two file of the istance
		"""
		self.csv_agent[part].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
		self.csv_agent_history[part].write(f"""{agent.make_csv_standard(data).replace("'", '"')}""")
		
		if self.settings["parts"][part]["db"]["enabled"]:
			index = agent.csv2array(self.settings["parts"][part]["intestation"])[0]
			infos = agent.csv2array(data)[0]

			dict_values = {}
			values_intestation = []
			values = []

			for key, value in self.settings["parts"][part]["db"]["change_intestation"].items():
				dict_values[key] = infos[index.index(value)][1:-1]

			for key, value in self.settings["parts"][part]["db"]["forced_values"].items():
				dict_values[key] = value

			for key, value in dict_values.items():
				values_intestation.append(key)
				values.append(value)

			values_intestation = agent.array2csv([values_intestation,]).replace("\n", "").replace("\"", "")
			values = agent.array2csv([values,]).replace("\n", "")
			payload = dumps({"operation": "sql", "sql": f"INSERT INTO {self.settings['parts'][part]['db']['table']} ({values_intestation}) VALUES ({values})"}).replace("\\\"", "'")

			try:
				response = requests.request("POST", self.settings["parts"][part]["db"]["url"], headers={'Content-Type': 'application/json','Authorization': f'''Basic {self.settings["parts"][part]["db"]["token"]}'''}, data=payload)
				self.log.print(f"    - By DB: {response.text}")
			except:
				self.log.print(f"    - Failed the DB insert")

	def analyze_PC(self, PC_name):
		"""Analyze the PC
		"""
		conn = wmi.WMI("." if self.settings['debug'] else PC_name)

		if self.settings["parts"]["osversion"]["validity"]:
			self.log.print("  - Istruction: Win32_OperatingSystem")
			for os_info in conn.Win32_OperatingSystem(["Caption", "Version"]):
				self.write_data("osversion", data=f"'{'My PC' if self.settings['debug'] else PC_name}','{os_info.Caption}','{os_info.Version}','{datetime.now()}','{int(datetime.utcnow().timestamp() * 10 ** 6)}'\n")
		
		if self.settings["parts"]["netinfo"]["validity"]:
			self.log.print("  - Istruction: Win32_NetworkClient && Win32_NetworkProtocol")
			for network_client, network_protocol, other in zip(conn.Win32_NetworkClient(["Caption", "Description", "Status", "Manufacturer", "Name"]), conn.Win32_NetworkProtocol(["GuaranteesDelivery", "GuaranteesSequencing", "MaximumAddressSize", "MaximumMessageSize", "SupportsConnectData", "SupportsEncryption", "SupportsEncryption", "SupportsGracefulClosing", "SupportsGuaranteedBandwidth", "SupportsQualityofService"]), conn.Win32_NetworkAdapterConfiguration(["DNSDomain", "DHCPEnabled", "DefaultIPGateway", "MACAddress"], IPEnabled=True)):
				try:
					for i in range(len(other.DefaultIPGateway)): 
						self.write_data("netinfo", data=f"""'{'My PC' if self.settings['debug'] else PC_name}','{network_client.Caption}','{network_client.Description}','{network_client.Status}','{network_client.Manufacturer}','{network_client.Name}','{network_protocol.GuaranteesDelivery}','{network_protocol.GuaranteesSequencing}','{network_protocol.MaximumAddressSize}','{network_protocol.MaximumMessageSize}','{network_protocol.SupportsConnectData}','{network_protocol.SupportsEncryption}','{network_protocol.SupportsGracefulClosing}','{network_protocol.SupportsGuaranteedBandwidth}','{network_protocol.SupportsQualityofService}','{other.DNSDomain}','{other.DHCPEnabled}','{"IPv4" if type(ip_address(other.DefaultIPGateway[i])) is IPv4Address else "IPv6"}','{other.DefaultIPGateway[i] if type(ip_address(other.DefaultIPGateway[i])) is IPv4Address else self.MACnormalization(other.DefaultIPGateway[i])}','{self.MACnormalization(other.MACAddress)}','{requests.get(f"http://macvendors.co/api/{other.MACAddress}").json()['result']['company']}','{datetime.now()}','{int(datetime.utcnow().timestamp() * 10 ** 6)}'\n""")
				except:
					pass
		
		if self.settings["parts"]["eventsview"]["validity"]:
			self.log.print("  - Istruction: Win32_NTLogEvent")
			for events_view in conn.Win32_NTLogEvent(['ComputerName ', 'User', 'Category', 'Type', 'CategoryString', 'EventCode', 'EventIdentifier', 'EventType', 'Logfile', 'RecordNumber'], type="Error"):
				self.write_data("eventsview", data=f"'{'My PC' if self.settings['debug'] else PC_name}','{events_view.User}','{events_view.Category}','{events_view.Type}','{events_view.CategoryString}','{events_view.EventCode}','{events_view.EventIdentifier}','{events_view.EventType}','{events_view.Logfile}','{events_view.RecordNumber}','{self.start_time}','{self.start_time.timestamp()}'\n")
		
		if self.settings["parts"]["product"]["validity"]:
			self.log.print("  - Istruction: Win32_Product")
			for product_infos in conn.Win32_Product(["Caption", "Description", "IdentifyingNumber", "InstallDate", "InstallLocation", "Language", "Name", "ProductID", "URLInfoAbout", "URLUpdateInfo", "Vendor", "Version"]):
				self.write_data("product", data=f"'{'My PC' if self.settings['debug'] else PC_name}','{product_infos.Caption}','{product_infos.Description}','{product_infos.IdentifyingNumber}','{product_infos.InstallDate}','{product_infos.InstallLocation}','{product_infos.Language}','{product_infos.Name}','{product_infos.ProductID}','{product_infos.URLInfoAbout}','{product_infos.URLUpdateInfo}','{product_infos.Vendor}','{product_infos.Version}','{self.start_time}','{self.start_time.timestamp()}'\n")

	def core(self):
		"""The core of the run
		"""
		self.fail = []

		self.log.print("- Run main part")
		for PC_name in ("My PC, debug option",) if self.settings['debug'] else self.csv_names.read().split("\n")[1:]:
			if agent.check_PC("localhost" if self.settings['debug'] else PC_name):
				self.log.print(f" - {PC_name}")
				self.analyze_PC(PC_name)
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

	def init_csv(self):
		"""Init the csv files
		"""
		self.log.print("- Inizialize files")

		self.csv_unchecked2.write('"names","fail_reach","total_search"\n')
		self.log.print("- Inizialized csv_unchecked2")

		for key, value in self.settings["parts"].items():
			if value["validity"]:
				self.log.print(f"- Inizialize {key} file")
				if self.csv_agent_history[key].read() == "":
					self.csv_agent_history[key].write(f"{self.settings['parts'][key]['intestation']}\n")
					self.log.print(f"- Inizialized {key} history file")
				self.csv_agent[key].write(f"{self.settings['parts'][key]['intestation']}\n")
				self.log.print(f"- Inizialized {key} file")

	def update_unchecked_PC(self):
		""" Update unchecked PC
		"""
		# Make my upgraded array
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

		self.log.print("Unchecked PC upgraded")

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
				result += c + self.settings["parts"]["netinfo"]["MACsep"]

		return result[:-1:]

if __name__ == "__main__":
	agent()
