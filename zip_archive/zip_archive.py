'''
This script creates a zip archive of a list of selected folders
The zip name file is the union of the current year, month, day, hours and minutes
If, in the target directory, there are saved backups we choose if keep them or not
All configurations of this script are found on the INI file 
Important: this script was developed for Win only
'''

import shutil
from configparser import ConfigParser
import os
from time import strftime,sleep
import stat
from glob import glob

class Zip_maker():

	def __init__(self):
		#reading of the configuration file
		config = ConfigParser()
		config.read('config_file.ini')
		self.destination = config["DEFAULT"]["destination_folder"]
		
		#array of folder paths to backup
		self.folder_name = []
		for i in range(1,len(config.items('SOURCE'))):
			self.folder_name.append(config["SOURCE"]["folder_" + str(i)])
			
		#Other variables used in this class
		self.compression_ok = True	
		self.file_name = strftime("%Y%m%d-%H%M")
		self.local_path = os.path.dirname(os.path.abspath(__file__))

	def copy_compress(self):
		partial = ""
		#we copy all the content from the specified paths
		for path in self.folder_name:
			print("Copying " + path + "...\n")
			partial = os.path.basename(path)
			shutil.copytree(path,self.local_path + '\\temp\\' + partial)
		#making a zip archive	
		print("Compressing " + self.file_name +".zip ...\n")
		shutil.make_archive(self.file_name,"zip","temp")

	def get_compression_ok(self):
		return self.compression_ok
		
	def set_compression_ok(self,bool):
		self.compression_ok = bool

	def remove_temp_zip(self):
		#we delete the zip and the temp folder if there is any error
		try:
			print("Deleting " + self.file_name +".zip ...\n")
			os.remove(self.file_name +".zip ...")
		except:
			pass
		
		#this part is for removing the temp folder
		print("Deleting temporary files...\n")
		temp_dir_array = []
		def rm_files(dir_list, dir_path):
			for file in dir_list:
				try:
					os.remove(dir_path + "/" + file)
				except PermissionError:		
					os.chmod(dir_path + "/" + file, stat.S_IWRITE) #fix for only r files
					os.remove(dir_path + "/" + file)

		def rmv_directory(dir_entry):
			rm_files(dir_entry[2], dir_entry[0])
			temp_dir_array.insert(0, dir_entry[0])

		for directory in os.walk("temp"):
			rmv_directory(directory)

		for dir in temp_dir_array:
			os.rmdir(dir)
		
	def previous_backups(self):
		#list of available backups with a Windows path style
		list = glob(self.destination +'/*-*.zip')
		backup_list = [pathname.replace('\\', '/') for pathname in list] 
		
		 #if there are saved backups, we choose if we want to keep it
		if backup_list:
			print("Saved backups:\n")
			for file in range(0,len(backup_list)):
				print(str(file) + " - " + backup_list[file])
			
			def backups_remover():
				user_choice = input("Do you want to delete backups in " + self.destination + "? (Y/N)\n")
				if user_choice.upper() == "Y":
					for file in backup_list:
						os.remove(file) 
					print("Backups removed\n")					
				elif user_choice.upper() == "N":
					print("previous backups have not been removed!\n")				
				else:
					print("Not valid choice!\n")
					backups_remover()
					
			backups_remover()
				
	def move_and_exit(self):
		print("Moving " + self.file_name +".zip to " + self.destination + "...")
		shutil.move(self.file_name + '.zip', self.destination)
		
		#used only to delete temp at the end
		self.remove_temp_zip()
		
		#reverse loop for autoclosing ath the end
		for i in range(10, 0, -1):
			print('Closing in {} seconds...'.format(i), end='\r') #redraw line
			sleep(1)
		exit()	

data = Zip_maker()

try:
	data.copy_compress()
	
except Exception as comp_error:
        data.set_compression_ok(False)
        print(comp_error)
        data.remove_temp_zip()

if data.get_compression_ok(): 	
	try:
		data.previous_backups()
		data.move_and_exit()
		
	except Exception as del_mov_error:
		print(del_mov_error)
		data.remove_temp_zip()
		
		
