'''
This simple script manages ticket assistance files
Files are created with this structure:
* TICKET number (incremental)
* DATE
* COMPANY
* PRODUCT
* PROBLEM
* SOLUTION
* ADDITIONAL NOTES
Tickets are saved in txt format a subfolder called "tickets"
This script can also remove, edit tickets or perform searches
'''

from configparser import ConfigParser
from os import path, system, remove, listdir
from time import strftime
from re import compile, match


class Ticket_manager():

	def __init__(self):
		self.today_date = strftime("%H:%M %d/%m/%Y")
		self.dir_path = path.dirname(path.realpath(__file__))

	def __read_ini_file(self):
		'''Reads data from configuration file'''
		config = ConfigParser()
		config.sections()
		config.read('config.ini')
		number_of_tickets = config['DEFAULT']['last_ticket']
		return number_of_tickets

	def __write_ini_file(self,index):
		'''Writes data from configuration file, private method'''
		config = ConfigParser()
		config.sections()
		config['DEFAULT']['last_ticket'] = index
		with open('config.ini', 'w') as configfile:
			config.write(configfile)

	def __new_ticket(self):
		'''Function used to add a new ticket'''
		new_ticket_num = str( int(self.__read_ini_file()) + 1)
		print("\nNew ticket #" + new_ticket_num + ", date "+ self.today_date)
		self.__write_ini_file(new_ticket_num)
		file = open(self.dir_path + "/tickets/#"+ new_ticket_num +".txt","w")   
		file.write("TICKET:\n#" + new_ticket_num + "\n\nDATE:\n" + self.today_date + "\n")
		
		def write_section(section_name, message): 
			'''
			writes a specific section of the ticket
			arguments
				section_name: string, name of the section to write
				message: string, text to put under section_name
			'''

			user_input = input(message + ": ")
			file.write("\n" + section_name + ":\n") 
			
			def break_word(): 
				'''
				used to format the text, max 60 characters per line
				returns
					string, formatted text
				'''
				processed_text = ""
				line_size = 0
				is_broken_word = compile('[^\S]')  #everything else than a whitespace
				for i in range(len(user_input)):
					if line_size < 60:
						line_size = line_size + 1
						processed_text = processed_text + user_input[i]
					else:
						line_size = 0
						if not match(is_broken_word, user_input[i]):
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
		print("\nTicket registered!")	

	def __search(self):
		'''Used to search in the saved text files'''
		term_to_search = input("\nInsert the term to search: ").upper()
		items_found = []

		for file in [f for f in listdir(self.dir_path + "/tickets/") if f.endswith('.txt')]:
			search_file = open(self.dir_path + "/tickets/" + file, "r")
			for line in search_file:
				if term_to_search in line.upper(): #we confront all uppercase characters

					item_data = ["",""]
					item_data[0] = file
					item_data[1] = line
					#we use an array to store data - faster than using a string
					items_found.append(item_data)

			search_file.close()

		if not items_found: #if it is empty
			print("\nNo result")
		else:
			for entry in items_found:
				print("\nTicket id:" + entry[0])
				print("Line content:" + entry[1])

	def __modify_ticket(self):
		'''Used to edit a ticket with the text editor with the id number'''
		ticket_num = input("\nInsert the number of the desired ticket to modify: ")
		path_file_to_modify = self.dir_path + "/tickets/#"+ ticket_num +".txt"

		if path.isfile(path_file_to_modify):
			system("notepad.exe " + self.dir_path + "/tickets/#"+ ticket_num +".txt")
		else:
			print("\nThat ticket does not exist!")
			
	def __remove_ticket(self):
		'''Used to remove a ticket with the text editor with the id number'''
		ticket_num = input("\nInsert the number of the desired ticket to remove: ")
		path_file_to_remove = self.dir_path + "/tickets/#"+ ticket_num +".txt"
		if path.isfile(path_file_to_remove):
			remove(self.dir_path + "/tickets/#"+ ticket_num +".txt")
			print("\nTicket removed!")
		else:
			print("\nThat ticket does not exist!")
			
	def run(self):
		print("\nChoose an option: \
				\nN - New Ticket, \
				\nS - Search, \
				\nM - Modify Ticket, \
				\nR - Remove Ticket, \
				\nE - exit")
		ticket_num = input("\nYour choiche: ")
		if ticket_num.upper() == "N":
			self.__new_ticket()
			self.run()
		elif ticket_num.upper() == "S":
			self.__search()
			self.run()
		elif ticket_num.upper() == "M":
			self.__modify_ticket()
			self.run()
		elif ticket_num.upper() == "R":
			self.__remove_ticket()
			self.run()
		elif ticket_num.upper() == "E":
			exit()
		else:
			input("Choice not valid!\n")
			self.run()
			
			
data = Ticket_manager()

try:
	data.run()
	
except Exception as run_error:
	print(run_error)
	input("Press any key to exit...")

