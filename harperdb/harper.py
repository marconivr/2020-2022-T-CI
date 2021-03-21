__author__ = "Sabaini Chiara 4CI"
__email__ = "18762@studenti.marconiverona.edu.it"
__version__ = 01.01
__date__ = "2021-03-12"

import requests

url = "https://cloud-1-itimarconivr.harperdbcloud.com/"


payload = "{\n\t\"operation\":\"sql\",\n\t\"sql\": \"INSERT INTO dev.agent (Caption, DHCPServer, DNSDomain, DefaultGW, IPEnabled, IPV4, IPV6, MACAddress, TimeStamp) VALUES('ASUS PCE-N10 11n Wireless LAN PCI-E Card', '192.168.178.1', 'Sabaini Chiara', '192.168.178.1', 'True', '192.168.178.9', '2001:b07:ad4:350:6ccf:57f0:c211:b533', '0C-9D-92-BA-C2-F5', '16340523422')\"\n}"

headers = {

'Content-Type': 'application/json',

'Authorization': 'Basic Z2lhbm5pYmVsbGluaTpIYXJwZXJEQiQkNjM='

}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))