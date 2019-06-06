'''
This script adds the last modification date to all file or folder names in the current directory (YEAR_MONTH_DAY),
If, at the beginning of the file name, there is already YEAR_MO_DA_, if necessary we update the information
Attention: this script was developed for WIN only
'''

import os.path
import time
import re

class Initialize:

    def __init__(self):
        self.curr_path = os.path.dirname(os.path.abspath(__file__))
        self.script_name = os.path.basename(__file__)

    def run(self):
        print("Add/change the modification date on all file/folders in the current directory?")
        print("If there is YEAR_MO_DA_ the beginning of the files, it could be changed.")
        user_choice = input("Your choice (Y/N): ")
        user_choice = user_choice.upper()
        if user_choice == "Y":
            print("Processing...")
            for curr_file in os.listdir(self.curr_path):
                if curr_file != self.script_name:
                    #the script's name is never changed
                    self.add_date_string(curr_file,self.curr_path)
        elif user_choice == "N": 
            input("Press any key to exit..")
            quit()
        else:
            print("Not a valid choice!")
            self.run()

    def add_date_string(self,file_name,path_name):

        file_path = path_name + "\\" + file_name
        date = time.ctime(os.path.getmtime(file_path))

        def format_num(a):
            #this function returns a value with 0 at hte beginning (if needed)
            number = int(a)
            if number < 10:
                return "0" + str(number)
            else:
                return str(number)

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

        final_date_string = year + "_" + month + "_" + day

        def check_add_date(name,last_mod_date):
            '''
            check if the file name already contains the date in the YEAR_MO_DA_ format,
            if the date of the last modification of the file is the same, we keep the information
            otherwise we delete the old date and add the new one.
            If we do not fall within these conditions, we add the date to the file name
            '''
            findings = re.search(r'\d{4}_\d{2}_\d{2}',name)
            if findings is None:
                return last_mod_date + "_" + name
            else:
                result = findings.group(0)
                if(result == last_mod_date):
                    return name
                else:
                    return last_mod_date + "_" + name[11:]
        
        new_file_name = check_add_date(file_name,final_date_string)
        os.rename(file_name, new_file_name)

app = Initialize()

try:
    app.run()
except Exception as error:
    print(error)
input("Press any key to exit..")

