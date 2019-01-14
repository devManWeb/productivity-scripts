from datetime import date
import shutil
import os

'''Variables'''
def variables():
	today_date = str(date.today())
	file_name = today_date.replace("-", "")

	folder_name = "C:/Work" #Edit this with the path of your folder

	return file_name,folder_name


try:
	'''Compressing'''
	print("Compressing " + variables()[0] +".zip ...")
	shutil.make_archive(variables()[0], 'zip', variables()[1])

	'''Moving'''
	print("Moving " + variables()[0] +".zip ...")
	shutil.move(variables()[0] + '.zip', variables()[1])

except Exception as e:
	'''Error managment from shutil operations'''
	print(e)
	input("Press any key to exit...")

