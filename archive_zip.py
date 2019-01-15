'''
This script creates a zip archive of the contents of a selected directory
The name of the zip file is the combination of the current year, month and day
the zip archive is then moved to the selected directory
'''

from datetime import date
import shutil
import os

class Zip_maker():

	def __init__(self, folder_name):
		self.folder_name = folder_name
		self.compression_ok = True	
		self.today_date = str(date.today())
		self.file_name = self.today_date.replace("-", "")

	def compress(self):
		print("Compressing " + self.file_name +".zip ...")
		shutil.make_archive(self.file_name, 'zip', self.folder_name)

	def get_compression_ok(self):
		return self.compression_ok
		
	def set_compression_ok(value,bool):
		self.compression_ok = bool

	def compress_error(self):
		print("Deleting " + self.file_name +".zip ...")
		os.remove(self.file_name +".zip ...")
		input("Press any key to exit...")

	def move(self):
		print("Moving " + self.file_name +".zip ...")
		shutil.move(self.file_name + '.zip', self.folder_name)

	def move_error(self):
		input("Press any key to exit...")
	

data = Zip_maker("D:/Sviluppo") #Edit this with the path of your folder

try:
	data.compress()
	
except Exception as comp_error:
        data.set_compression_ok(False)
        print(comp_error)
        data.compress_error()

if data.get_compression_ok: 	

	try:
		data.move()
		
	except Exception as mov_error:
		print(mov_error)
		data.move_error()


