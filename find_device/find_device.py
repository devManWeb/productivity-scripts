'''
Search for devices in the local network that have the same first three pairs of the MAC address.
Then, if we find one or more corresponding device, we show the IP
The configuration parameters are loaded from the INI file
Important: this script was developed for Windows only
'''
import configparser
import re
import nmap

def scan_and_display(target_mac):
	print("Scanning your network, please wait...")
	config = configparser.ConfigParser()
	config.read("config_file.ini")
	nm = nmap.PortScanner()
	nm.scan(hosts= config["DEFAULT"]["ip_range_to_scan"] , arguments="-sP")
	host_list = nm.all_hosts()
	device_IP = []

	for host in host_list:
		if "mac" not in nm[host]["addresses"]:  #if there is no MAC address
			continue
		else:
			mac_str = nm[host]['addresses']['mac']
			mac_str = "\"" + mac_str[:-9] + "\"" #we keep only the first part of the MAC address
			if target_mac == mac_str:
				device_IP.append(nm[host]["addresses"]["ipv4"])

	if len(device_IP) == 0:
		print("\nNo result!")
		start()
	else:
		print("\nIP address list:")
		for item in range (0,len(device_IP)):
			print(str(item) + " - " + device_IP[item])

def start():
	config = configparser.ConfigParser()
	config.read("config_file.ini")
	cfg_list = config.sections()
	user_text = "\n"
	position = 0
	for device in config.sections():
		device = re.sub("[^a-zA-Z0-9 ]+","", device)
		position = cfg_list.index(device) #numeric position in the list
		user_text = user_text + str(position) + " - " + config[device]["device_name"] + " \n"
	user_text = user_text + "Other - Exit\n"
	print(user_text)
	user_choice = input("Your choice:")

	try:
		user_choice = int(user_choice)
		if 0 <= user_choice <= position:
			device_name = cfg_list[user_choice]
			scan_and_display(config[device_name]["initial_MAC"])
		else:
			quit()
	except ValueError: #if the inserted value is not a int number
		quit()

try:
	start()
except Exception as gen_error:
	print("Attention, " + str(gen_error))
