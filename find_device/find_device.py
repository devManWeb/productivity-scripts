'''
Search for devices in the local network that have the same first three pairs of the MAC address.
Then, if we find a corresponding device, we a new browser tab with that IP. 
If we found more than one devices, we make a choice.
'''

import nmap
import webbrowser

def scan_open(protocol,target_mac):
	print("Scanning your network, please wait...")
	nm = nmap.PortScanner()
	nm.scan(hosts='192.168.1.0/24', arguments='-sP') #IP range to scan
	host_list = nm.all_hosts()
	device_list = []	
		
	for host in host_list:
		if 'mac' in nm[host]['addresses'] and(target_mac in nm[host]['addresses']['mac']):
			device_list.append(nm[host]['addresses']['ipv4'])
				
	def choose_one():
		for i in range (0,len(device_list)):
			print(str(i + 1) + " - " + device_list[i])
		user_choice = int(input("Your choice: ")) - 1
		if 0 <= user_choice <= len(device_list):
			webbrowser.open(protocol + device_list[user_choice], new=2)
		else:
			print("Not a valid choice!")
			choose_one()	
	
	if len(device_list) == 0:
		print("No result!")
		start()
	elif len(device_list) == 1:
		webbrowser.open(protocol + device_list[0], new=2)
	else:
		choose_one()

def start():
	user_choice = input("\n1 - Device A\n2 - Device B\nOther - Exit\n\n")	
	if user_choice == "1":  #device A
		scan_open("https://","AA:BB:CC")
	elif user_choice == "2": #device B
		scan_open("https://","AA:BB:CC")
	else:
		quit()

try:
    start()
except Exception as gen_error:		
	print("Attention, " + gen_error)
