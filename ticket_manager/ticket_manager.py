'''
This simple script manages tickets assistance files
Files are created with this structure:
* TICKET number (incremental)
* DATE
* COMPANY
* PRODUCT
* PROBLEM
* SOLUTION
* ADDITIONAL NOTES
Tickets are saved in txt format a subfolder called "tickets"
relative to where the script is located
'''

import configparser
import os
import time


class Ticket_manager():

	def __init__(self):
		self.today_date = time.strftime("%H:%M %d/%m/%Y")
		self.dir_path = os.path.dirname(os.path.realpath(__file__))

	def read_ini_file(self):
		config = configparser.ConfigParser()
		config.sections()
		config.read('config.ini')
		number_of_tickets = config['DEFAULT']['last_ticket']
		return number_of_tickets

	def write_ini_file(self,index):
		config = configparser.ConfigParser()
		config.sections()
		config['DEFAULT']['last_ticket'] = index
		with open('config.ini', 'w') as configfile:
			config.write(configfile)

	def new_ticket(self):
		new_ticket_num = str( int(self.read_ini_file()) + 1)
		print("\nNew ticket #" + new_ticket_num + ", date "+ self.today_date)
		self.write_ini_file(new_ticket_num)
		file = open(self.dir_path + "/tickets/#"+ new_ticket_num +".txt","w")   
		file.write("TICKET:\n#" + new_ticket_num + "\n\nDATE:\n" + self.today_date + "\n")
		def write_section(section_name, message):
			user_input = input(message + ": \n")
			file.write("\n" + section_name + ":\n") 
			file.write(user_input + "\n") 
		write_section("COMPANY","Company name")
		write_section("PRODUCT","What is the product")
		write_section("PROBLEM","Describe the problem")
		write_section("SOLUTION","Describe the solution")
		write_section("ADDITIONAL NOTES","Add some more notes")
		file.close()
		print("\nTicket registered!\n")

	def modify_ticket(self):
		ticket_num = input("Insert the number of the desired ticket to modify: \n")
		path_file_to_modify = self.dir_path + "/tickets/#"+ ticket_num +".txt"
		if os.path.isfile(path_file_to_modify):
			os.system("notepad.exe " + self.dir_path + "/tickets/#"+ ticket_num +".txt")
		else:
			print("That ticket does not exist!")
			
	def remove_ticket(self):
		ticket_num = input("Insert the number of the desired ticket to remove: \n")
		path_file_to_remove = self.dir_path + "/tickets/#"+ ticket_num +".txt"
		if os.path.isfile(path_file_to_remove):
			os.remove(self.dir_path + "/tickets/#"+ ticket_num +".txt")
			print("Ticket removed!")
		else:
			print("That ticket does not exist!")
			
	def choice(self):
		ticket_num = input("Choose an option:\nN - New Ticket,\nM - Modify Ticket,\nR - Remove Ticket,\nE - exit \n")
		if ticket_num.upper() == "N":
			self.new_ticket()
			self.choice()
		elif ticket_num.upper() == "M":
			self.modify_ticket()
			self.choice()
		elif ticket_num.upper() == "R":
			self.remove_ticket()
			self.choice()
		elif ticket_num.upper() == "E":
			exit()
		else:
			input("Choice not valid!\n")
			self.choice()
			
	def run(self):
		self.choice()		
			
			
data = Ticket_manager()


try:
	data.run()
	
except Exception as run_error:
	print(run_error)
	input("Press any key to exit...")
        
