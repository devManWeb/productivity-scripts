'''
This script creates a zip archive of the contents of a selected directory
The file name of the zip is the union of the current year, month, day, hours and minutes
the archive is then moved to the selected directory
Important: this script was developed for Win only
'''

import shutil
import os
import time
import glob
import sys

class Zip_maker():

	def __init__(self, folder_name, destination):
		self.folder_name = folder_name
		self.destination = destination
		self.compression_ok = True	
		self.file_name = time.strftime("%Y%m%d-%H%M")

	def compress(self):
		print("Compressing " + self.file_name +".zip ...")
		shutil.make_archive(self.file_name, 'zip', self.folder_name)

	def get_compression_ok(self):
		return self.compression_ok
		
	def set_compression_ok(self,bool):
		self.compression_ok = bool

	def compress_error(self):
		print("Deleting " + self.file_name +".zip ...")
		os.remove(self.file_name +".zip ...")
		input("Press any key to exit...")
		
	def previous_backups(self):
		list = glob.glob(self.destination +'/*-*.zip')
		backup_list = [pathname.replace('\\', '/') for pathname in list] #Windows path
		if backup_list: #if not empty
			print("Saved backups:\n")
			for file in backup_list:
				print(file)
			def backups_remover():
				user_choice = input("Remove previous backups in " + self.destination + "? (Y/N)\n")
				if user_choice.upper() == "Y":
					for file in backup_list:
						os.remove(file) 
					print("Backups removed")
				elif user_choice.upper() == "N":
					print(self.file_name + " is not moved")
					input("Press any key to exit...")
					sys.exit()
				else:
					print("Not valid choice!")
					backups_remover()
			backups_remover()
				
	def move_and_exit(self):
		print("Moving " + self.file_name +".zip to " + self.destination + "...")
		shutil.move(self.file_name + '.zip', self.destination)
		for i in range(10, 0, -1): #reverse loop to autoclosing
			print('Closing in {} seconds...'.format(i), end='\r') #redraw line
			time.sleep(1)
		sys.exit()

	def move_error(self):
		input("Press any key to exit...")
	

#Edit this with the path of your folder and with the destination folder	
data = Zip_maker("D:/Sviluppo", "T:/UFFICIO SOFTWARE/Leonardo/BACKUP SVILUPPO")

try:
	data.compress()
	
except Exception as comp_error:
        data.set_compression_ok(False)
        print(comp_error)
        data.compress_error()

if data.get_compression_ok(): 	

	try:
		data.previous_backups()
		data.move_and_exit()
		
	except Exception as del_mov_error:
		print(del_mov_error)
		data.move_error()
