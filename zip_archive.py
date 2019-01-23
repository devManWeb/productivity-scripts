'''
This script creates a zip archive of the contents of a selected directory
The file name of the zip is the union of the current year, month, day, hours and minutes
the archive is then moved to the selected directory
'''

import shutil
import os
import time

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

	def move(self):
		print("Moving " + self.file_name +".zip to " + self.destination + "...")
		shutil.move(self.file_name + '.zip', self.destination)

	def move_error(self):
		input("Press any key to exit...")


#Edit this with the path of your folder and with the destination folder
data = Zip_maker("D:/Sviluppo", "D:/backups")

try:
	data.compress()

except Exception as comp_error:
        data.set_compression_ok(False)
        print(comp_error)
        data.compress_error()

if data.get_compression_ok():

	try:
		data.move()

	except Exception as mov_error:
		print(mov_error)
		data.move_error()
