'''
Search for devices, in the local network, that have 
the same first three pairs of one of the mac addresses
provided for the chosen device.

If we find a corresponding device, we open it in the browser
with the protocol set in the configuration file.
If we found more than one devices, we ask you to make a choice.

The configuration parameters are loaded from the INI file
Important: this script was developed for Win OS only
'''
import configparser
import re
import nmap
import webbrowser
import os

class Find_device():

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("config_file.ini")
		self.MAC_arr = []
		self.protocol = ""
		self.IP_found_arr = []

	def reset_vars(self):
		self.MAC_arr = []
		self.protocol = ""
		self.IP_found_arr = []

	def user_menu(self):	
		cfg_list = self.config.sections()
		user_text = ""
		position = 0
		self.reset_vars()

		for device in self.config.sections(): #search for all configurations in the ini file
			device = re.sub("[^a-zA-Z0-9 ]+","", device)
			position = cfg_list.index(device) #numeric position in the list
			user_text = user_text + str(position) + " - " + self.config[device]["device_name"] + " \n"
		user_text = user_text + "Other - Exit\n"
		print(user_text)
		user_choice = input("Your choice:")
		try:
			
			user_choice = int(user_choice)
			if 0 <= user_choice <= position:
				name = cfg_list[user_choice]

				#looks for all mac address associated with this device
				item_list = self.config.items(name)
				mac_regex = re.compile(r"MAC_\d")
				for param_name in item_list:
					to_check = (param_name[0]).upper()
					if re.match(mac_regex,to_check) is not None:
						self.MAC_arr.append(param_name[1])
					
				self.protocol = self.config[name]["protocol"]
			else:
				quit()

		except ValueError: 
			#if the inserted value is not a int number
			quit()	

	def scan_network(self):
		print("Scanning your network, please wait...")
		nm = nmap.PortScanner()
		nm.scan(hosts= self.config["DEFAULT"]["ip_range_to_scan"] , arguments="-sP")
		host_list = nm.all_hosts()

		for current_mac in self.MAC_arr:
			#scans the network for all for all associated mac address

			for host in host_list:
				if "mac" not in nm[host]["addresses"]: 
					#if there is no MAC address
					continue
				else:
					mac_str = nm[host]['addresses']['mac']
					mac_str = mac_str[:-9] #we keep only the first part of the MAC address
					if current_mac == mac_str:
						self.IP_found_arr.append(nm[host]["addresses"]["ipv4"])		

	def choose_and_open(self):

		if not self.IP_found_arr:
			#if there is no compatible device
			print("No result!\n")
			#we call the whole procedure again
			self.user_menu()
			self.scan_network()
			self.choose_and_open()
			
		elif len(self.IP_found_arr) == 1:
			#if there is one compatible device
			webbrowser.open(self.protocol + "://" + self.IP_found_arr[0], new = 2)
		else:
			#if we have more than one device with the same initial MAC address
			print("\nPlease choose an IP address:")
			for item in range (0,len(self.IP_found_arr)):
				print(str(item) + " - " + self.IP_found_arr[item])
			user_choice = input("\nYour choice: ")
			try:
				user_choice = int(user_choice)
				if 0 <= user_choice <= len(self.IP_found_arr):
					webbrowser.open(self.protocol + "://" + self.IP_found_arr[user_choice], new = 2)
				else:
					print("Not a valid choice!")
					self.choose_and_open()
			except ValueError: 
					#if the inserted value is not a int number
					print("Not a valid choice!")
					self.choose_and_open()


app = Find_device()

if os.name == "nt":
	try:
		app.user_menu()
		app.scan_network()
		app.choose_and_open()
	except Exception as gen_error:
		print("Attention, " + str(gen_error))
		input("Press any key to exit..")
else:
	print("Unsupported operating system")
	input("Press any key to exit..")
