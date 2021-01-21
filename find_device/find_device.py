'''
Search for one or more devices, in the local network, that have 
the same first three pairs of one of the mac addresses
provided for the chosen device.
If we find a corresponding device, we open it in the browser
with the protocol set in the configuration file.
If we found more than one devices, we ask you to make a choice.
The configuration parameters are loaded from the INI file
Important: this script was developed for Win OS only
'''

from configparser import ConfigParser
from re import match, compile
from nmap import PortScanner
from webbrowser import open
from os import name, path
import ctypes, sys

class Find_device():

	def __init__(self):

		self.devices = [
			[],		#MAC address (list of lists)
			[],		#device type
			[],		#protocol
			[]		#ip found (list of lists)
		]
		#used when looking for only one type of device
		self.protocol_single_device = ""

	def __reset_all(self):
		#delete the internal values
		self.devices = [[],[],[],[]]
		self.protocol_single_device = ""

	def __num_IP_found(self):
		#how many IP there are?
		empy_spots = 0
		for item in self.devices[3]:
			if item == []:
				empy_spots = empy_spots + 1
		return len(self.devices[3]) - empy_spots

	def __initialize_devices_list(self):
		#Loads the configuration from the ini file 
		#puts it on a list, to be used by the code
		self.config = ConfigParser()
		self.config.read("config_file.ini")
		
		devices_configuration = self.config.sections()
		for item in devices_configuration:

			# ------- MAC ------- #
			mac = []
			mac_regex = compile(r"MAC_\d")
			for key in self.config[item]:
				if match(mac_regex,key.upper()) is not None:
					mac.append(self.config[item][key])

			self.devices[0].append(mac)	
			# ------- Device name + protocol ------- #
			device_name = self.config[item]["device_name"]
			self.devices[1].append(device_name)
			protocol = self.config[item]["protocol"]
			self.devices[2].append(protocol)


	def __scan_network(self,what_device,all_devices):
		#here the actual network scan is done
		print("Scanning your network, please wait...\n")
		nm = PortScanner()
		nm.scan(hosts= self.config["DEFAULT"]["ip_range_to_scan"] , arguments="-sP")
		host_list = nm.all_hosts()

		#scans the network for all for all the configured devices
		#please note: here we handle list of lists
		if all_devices:

			for sublist in self.devices[0]:
				ip_found = []
				for current_mac in sublist: 
			
					for host in host_list:
						if "mac" not in nm[host]["addresses"]: 
							#if there is no MAC address
							continue
						else:
							mac_str = nm[host]['addresses']['mac']
							mac_str = mac_str[:-9] #we keep only the first part of the MAC address
							if current_mac == mac_str:
								ip_found.append(nm[host]["addresses"]["ipv4"])

				self.devices[3].append(ip_found)

		#scans the network for only a specific type of device
		else:
			self.protocol_single_device = self.devices[2][what_device]
			for current_mac in self.devices[0][what_device]: 
					
				for host in host_list:
					if "mac" not in nm[host]["addresses"]: 
						#if there is no MAC address
						continue
					else:
						mac_str = nm[host]['addresses']['mac']
						mac_str = mac_str[:-9] #we keep only the first part of the MAC address
						if current_mac == mac_str:
							self.devices[3].append(nm[host]["addresses"]["ipv4"])
	

	def __manage_results(self,what_device,all_devices):
		'''
		function for managing results
		loads the device found on the browser 
		with multiple devices, asks what to do
		'''

		#from the search for all types of devices
		if all_devices:

			if self.__num_IP_found() > 0:
				position = 0
				device = 0

				for sublist in self.devices[3]:
					#we skip empty lists
					if sublist is not None:
						type_device = str(self.devices[1][device])
						device = device + 1

						for IP in sublist:
							IP_device = str(IP)
							print(str(position) + " - " + type_device + " - " + IP_device)
							position = position + 1
				print("Other - Exit\n")

				user_choice = input("Your choice: ")
				try:
					user_choice = int(user_choice)

					if user_choice >= position:
						raise ValueError

					# ------- IP for the browser ------- #
					flatted_list_IP = []
					for sublist in self.devices[3]:
						for item in sublist:
							flatted_list_IP.append(item)
					IP_browser = str(flatted_list_IP[user_choice])
					# ------- protocol to use ------- #
					protocol_browser = ""
					for i, x in enumerate(self.devices[3]):
						if IP_browser in x:
							protocol_browser = str(self.devices[2][i])		

					open(protocol_browser + "://" + IP_browser, new = 2)

				except ValueError: 
					'''
					if the inserted value is not a int number or 
					is greater than the number of options available
					'''
					quit()

			else:
				print("No device found!")
				input("Press enter to exit..")

		#from the search of a specific type of device
		else:
			if self.__num_IP_found() > 1:

				position = 0
				for IP in self.devices[3]:
					IP_device = str(IP)
					print(str(position) + " - " + IP_device)
					position = position + 1
				print("Other - Exit\n")

				user_choice = input("Your choice: ")
				
				try:
					user_choice = int(user_choice)
					# ------- IP for the browser ------- #
					IP_browser = str(self.devices[3][user_choice])
					# ------- protocol to use ------- #
					protocol_browser = str(self.protocol_single_device)		
					open(protocol_browser + "://" + IP_browser, new = 2)

				except ValueError: 
					quit()
			
			elif self.__num_IP_found() == 1:
				protocol_browser = str(self.devices[2][what_device])
				IP_browser = str(self.devices[3][0])
				open(protocol_browser + "://" + IP_browser, new = 2)
			
			else:
				print("No device found!")
				input("Press enter to exit..")

	def run(self):
		#main and only public function
		if path.isfile("config_file.ini") is False:
			raise Exception("Configuration file not found!")
		else:
			self.__reset_all()
			self.__initialize_devices_list()

			position = 0
			for device_name in self.devices[1]:
				print(str(position) + " - " + str(device_name))
				position = position + 1

			if len(self.devices[1]) > 0:
				print(str(position) + " - All configured devices")

			print("Other - Exit\n")
			user_choice = input("Your choice: ")

			try:
				user_choice = int(user_choice)
				if user_choice > position:
					raise ValueError
				if 0 <= user_choice < len(self.devices[1]):
					#searches for this device
					self.__scan_network(user_choice,False)
					self.__manage_results(user_choice,False)
				else:
					#searches for all devices
					self.__scan_network(0,True)
					self.__manage_results(0,True)
			except ValueError: 
				'''
				if the inserted value is not a int number or 
				is greater than the number of options available
				'''
				quit()


def adminRights():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

app = Find_device()		

if adminRights():
	#if we have admin rights
	if name == "nt":
		try:
			app.run()
		except Exception as gen_error:
			print("Attention, " + str(gen_error))
			input("Press enter to exit..")
	else:
		print("Unsupported operating system")
		input("Press enter to exit..")
else:
    #if not, run the script again with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


