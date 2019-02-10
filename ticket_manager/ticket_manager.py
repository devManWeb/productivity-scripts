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
This script can also remove or edit tickets or perform searches
'''

import configparser
import os
import time
import re


class Ticket_manager():

	def __init__(self):
		self.today_date = time.strftime("%H:%M %d/%m/%Y")
		self.dir_path = os.path.dirname(os.path.realpath(__file__))

	def read_ini_file(self):
		config = configparser.ConfigParser()
		config.sections()
		config.read('config_file.ini')
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

		def write_section(section_name, message): #write a specific section of the ticket
			user_input = input(message + ": \n")
			file.write("\n" + section_name + ":\n")

			def break_word(): #maximum sixty letters per line
				processed_text = ""
				line_size = 0;
				is_broken_word = re.compile('[^\S]')  #everything else than a whitespace
				for i in range(len(user_input)):
					if line_size < 60:
						line_size = line_size + 1
						processed_text = processed_text + user_input[i]
					else:
						line_size = 0
						if not re.match(is_broken_word, user_input[i]):
							processed_text = processed_text + user_input[i] + "-\n"
						else:
							processed_text = processed_text + user_input[i] + "\n"
				return processed_text


			file.write(break_word() + "\n")

		write_section("COMPANY","Company name")
		write_section("PRODUCT","What is the product")
		write_section("PROBLEM","Describe the problem")
		write_section("SOLUTION","Describe the solution")
		write_section("ADDITIONAL NOTES","Add some more notes")
		file.close()
		print("\nTicket registered!\n")

	def search(self):
		term_to_search = input("\nInsert the term to search: \n").upper()
		items_found = ""
		#now we search in the saved text files for the term
		for file in [f for f in os.listdir(self.dir_path + "/tickets/") if f.endswith('.txt')]:
			search_file = open(self.dir_path + "/tickets/" + file, "r")
			for line in search_file:
				if term_to_search in line.upper(): #we confront all uppercase characters
					items_found = items_found + file + "\n"
					break
			search_file.close()
		if not items_found: #if it is empty
			print("No result\n")
		else:
			print("Term found in:\n" + items_found)

	def modify_ticket(self):
		ticket_num = input("\nInsert the number of the desired ticket to modify: \n")
		path_file_to_modify = self.dir_path + "/tickets/#"+ ticket_num +".txt"
		if os.path.isfile(path_file_to_modify):
			os.system("notepad.exe " + self.dir_path + "/tickets/#"+ ticket_num +".txt")
		else:
			print("That ticket does not exist!\n")

	def remove_ticket(self):
		ticket_num = input("\nInsert the number of the desired ticket to remove: \n")
		path_file_to_remove = self.dir_path + "/tickets/#"+ ticket_num +".txt"
		if os.path.isfile(path_file_to_remove):
			os.remove(self.dir_path + "/tickets/#"+ ticket_num +".txt")
			print("Ticket removed!\n")
		else:
			print("That ticket does not exist!\n")

	def choice(self):
		print("\nChoose an option:\n")
		ticket_num = input("N - New Ticket,\nS - Search,\nM - Modify Ticket,\nR - Remove Ticket,\nE - exit \n")
		if ticket_num.upper() == "N":
			self.new_ticket()
			self.choice()
		elif ticket_num.upper() == "S":
			self.search()
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
