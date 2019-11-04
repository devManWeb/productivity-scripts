'''
This script creates a zip archive of a list of selected folders
The zip name file is the union of the current year, month, day, hours and minutes
If, in the target directory, there are saved backups we choose if keep them or not
All configurations of this script are found on the INI file 
Important: this script was developed for Win only
Plase note: if this script is closed before the end 
the user has to manually remove the temporary folder"
'''

from shutil import copytree, make_archive, move, rmtree
from configparser import ConfigParser
from os import path, remove, name, walk, chdir, mkdir
from time import strftime, sleep
from glob import glob
from tempfile import mkdtemp, gettempdir

class Zip_maker():

	def __init__(self):

		print("Plase note:")
		print("If this script is closed before the end,")
		print("the user has to manually remove the temporary folder")
		
		#reading of the configuration file
		config = ConfigParser()
		config.read('config_file.ini')
		self.destination = self.__replace_slash(config["DEFAULT"]["destination_folder"])
		self.auto_remove_previous = config["DEFAULT"]["auto_remove_previous"]

		#array of folder paths to backup
		self.folder_name = []
		self.num_folders = len(config.items('SOURCE')) - 1
		for i in range(1,self.num_folders):
			self.folder_name.append(config["SOURCE"]["folder_" + str(i)])
			
		#Other variables used in this class
		self.file_name = strftime("%Y%m%d-%H%M")
		#temporary folder, deleted when we close this script
		self.full_temp_path = mkdtemp(prefix="zip-archive-")

	def __temp_cleanup(self):
		#private method, removes the temporary folder
		print("\nRemoving temporary files...")
		#we exit from the temp folder to avoid an error
		chdir('..')
		rmtree(self.full_temp_path)

	def __replace_slash(self,full_path):
		#private method, replace / with \\
		return full_path.replace('/', '\\')

	def copy_compress(self):
		#if not Win, we raise an error
		if name != "nt":
			raise Exception("OS not supported!")

		'''
		we copy all the content from the specified paths 
		to to_backup in the temp folder
		'''
		partial = ""
		for current_path in self.folder_name:
			print("\nCopying " + current_path + "...")
			partial = path.basename(current_path)
			copytree(current_path,self.full_temp_path + '\\to_backup\\' + partial)

		#we change the current directory to the temp folder
		chdir(self.full_temp_path)

		#here we make a zip archive	
		print("\nCompressing " + self.file_name +".zip ...")
		make_archive(
			base_name=self.file_name,
			format='zip',
  			base_dir='to_backup'
		)

	def previous_backups(self):
		#list of available backups with a Windows path style
		list = glob(self.destination +'/*-*.zip')
		backup_list = [self.__replace_slash(pathname) for pathname in list] 
		
		#if there are saved backups, we choose if we want to keep it
		if backup_list:
			if self.auto_remove_previous == "True":
				for file in backup_list:
					remove(file) 
					print("\nBackups removed")
			else:
				print("Saved backups:\n")
				for file in range(0,len(backup_list)):
					print(str(file) + " - " + backup_list[file])

				def backups_remover():
					print("\nDo you want to delete backups in " + self.destination + "?")
					user_choice = input("Your choice (Y/N): ")
					if user_choice.upper() == "Y":
						for file in backup_list:
							remove(file) 
						print("\nBackups removed")					
					elif user_choice.upper() == "N":
						print("\nPrevious backups have not been removed!")				
					else:
						print("\nNot valid choice!")
						backups_remover()
						
				backups_remover()
				
	def move_backup(self):
		#move the backup to the desired folder
		print("\nMoving " + self.file_name +".zip to " + self.destination + "...")
		move(
			self.full_temp_path + "\\" + self.file_name + '.zip',
			self.destination
		)

	def exit_function(self):	
		#Exit message with an autoclosing loop
		self.__temp_cleanup()
		for i in range(10, 0, -1):
			print('Closing in {} seconds...'.format(i), end='\r') #redraw line
			sleep(1)
		exit()	

try:	
	data = Zip_maker()
	data.copy_compress()

except Exception as comp_error:
	print(comp_error)

else:
	try:
		data.previous_backups()
		data.move_backup()	
	except Exception as del_mov_error:
		print(del_mov_error)

data.exit_function()
