'''
Search for devices in the local network that have the same first three pairs of the MAC address.
Then, if we find one or more corresponding device, we show the IP
The configuration parameters are loaded from the INI file
Important: this script was developed for Windows only
'''
import configparser
import re
import nmap
import webbrowser

class Find_device():

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("config_file.ini")
		self.MAC_arr = []
		self.IP_found_arr = []

	def reset_vars(self):
		self.MAC_arr = []
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
				self.MAC_arr.append(self.config[name]["MAC_0"])	
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
		target_mac = self.MAC_arr[0]

		for host in host_list:
			if "mac" not in nm[host]["addresses"]: 
				#if there is no MAC address
				continue
			else:
				mac_str = nm[host]['addresses']['mac']
				mac_str = mac_str[:-9] #we keep only the first part of the MAC address
				if target_mac == mac_str:
					self.IP_found_arr.append(nm[host]["addresses"]["ipv4"])		

	def show_results(self):

		if not self.IP_found_arr:
			#if there is no compatible device
			print("No result!\n")
		else:
			print("\nIP address list:")
			for item in range (0,len(self.IP_found_arr)):
				print(str(item) + " - " + self.IP_found_arr[item] + "\n")
		input("Press any key to exit..")

app = Find_device()

try:
	app.user_menu()
	app.scan_network()
	app.show_results()
except Exception as gen_error:
	print("Attention, " + str(gen_error))
	input("Press any key to exit..")
