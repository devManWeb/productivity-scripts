'''
This snippet adds, in front of the name of the files and folders of the current directory,
the last modification date in this format: year, month and day
Attention: this script was developed for WIN only
'''

import os.path
import time
import re

def add_date_string(file_name,path_name):

    def format_num(a):
        #this function returns a value with 0 in front if needed
        number = int(a)
        if number < 10:
            return "0" + str(number)
        else:
            return str(number)
        
    file_path = path_name + "\\" + file_name
    date = time.ctime(os.path.getmtime(file_path))

    #year of last modification
    temp_year = re.search(r'\d{4}', date).group(0)
    year = format_num(temp_year)

    #month of last modification
    month = ""
    month_codes = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    index = 0
    for code in month_codes:
    	#loop until we find the numeric value of the month
        index = index + 1
        if code in date: 
            month = format_num(index)
            break

    #day of last modification
    temp_day = re.search(r'\d{1,2}', date).group(0)
    day = format_num(temp_day)

    final_date_string = year + "_" + month + "_" + day + "_"
    
    os.rename(file_name, final_date_string + file_name)

def run():
    print("Add the year, month and day of last modification to all the folder's files?")
    user_choice = input("Your choice (Y/N): ")
    user_choice = user_choice.upper()
    if user_choice == "Y":
        print("Processing...")
        curr_path = os.path.dirname(os.path.abspath(__file__))
        script_name = os.path.basename(__file__)
        for curr_file in os.listdir(curr_path):
            if curr_file != script_name:
                #the script's name is never changed
                add_date_string(curr_file,curr_path)
        input("Press any key to exit..")
    elif user_choice == "N": 
        quit()
    else:
        print("Not a valid choice!")
        run()

try:
    run()
except Exception as error:
    print(error)
    input("Press any key to exit..")