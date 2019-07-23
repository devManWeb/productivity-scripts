'''
Based on the set parameters (start and end time of work, duration of the lunch break),
shows how much we have to work again, if it is time to get up from the chair 
or to start working again. This script can be run at computer startup

TODO:run extensive tests and implement checks for the configuration data
TODO:set the settable pause time and support for those who work at night
'''

import configparser
from datetime import datetime
from threading import Timer

class HealthTimer():
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("config_file.ini")
		self.configured = self.config["DEFAULT"]["configured"]
		print("Welcome to the Health Timer!")
		if self.configured == "no":
			self.firstStart()

	def firstStart(self):
		''' 
		If this is the first time we start the script,
		we configure the start and end date of the work
		'''

		def confWriter(inputTxt,configIndex):
			#Collects the data in thw correct format
			previousValue = self.config['DEFAULT'][configIndex]
			insertedValue = str(input(inputTxt))
			if not insertedValue:
				#if the inserted string is empty
				self.config['DEFAULT'][configIndex] = previousValue
				print("Previous value keeped!")
			else:
				self.config['DEFAULT'][configIndex] = insertedValue
			
		confWriter("Enter the work start time (default 08:30): ","workStart")
		confWriter("Enter the work end time (default 18:00): ","workEnd")
		confWriter("Enter the start time of the lunch break (default 12:30): ","lunchStart")
		confWriter("Enter the end time of the lunch break (default 14:00): ","lunchEnd")

		#Only at the first start
		self.config['DEFAULT']["configured"] = "yes"

		#actual writing on config.ini
		with open("config_file.ini", "w") as newParams:    
			self.config.write(newParams)

	def notification(self,msgText):
		#TODO:use a proper desktop notification
		actualTime = datetime.now().strftime('%H:%M')
		print(actualTime + " - " + msgText)

	def clock(self):

		def timeChecker():

			'''
			This is the main timer. Based on the current hour and minute, 
			the script shows a warning if it's time to take a break, 
			to resume work or to take a lunch break
			'''
			
			workStart = self.config["DEFAULT"]["workStart"]
			workEnd = self.config["DEFAULT"]["workEnd"]
			lunchStart = self.config["DEFAULT"]["lunchStart"]
			lunchEnd = self.config["DEFAULT"]["lunchEnd"]

			def compareTime(start,end):
				#is the current time between start and end?
				start = start.split(":")
				actual = datetime.now().strftime('%H:%M').split(":")
				end = end.split(":")
				boolHour = int(start[0]) < int(actual[0]) < int(end[0])
				boolMinute = int(start[1]) < int(actual[1]) < int(end[1])
				return boolHour and boolMinute

			def timeTo(secondValue):
				#how much time is left (in seconds)?
				actual = datetime.now().strftime('%H:%M').split(":")
				secondValue = secondValue.split(":")
				convertedHours = (int(actual[0]) - int(secondValue[0])) * 3600
				convertedMinutes =(int(actual[1]) - int(secondValue[1])) * 60
				result = convertedHours + convertedMinutes
				if(result > 0):
					return result
				else:
					#TODO:implement also for the evening
					raise Exception("Negative interval!")

			def isInPause():
				#If we're working, is it time to take a break?
				actualMinute = datetime.now().strftime('%M')
				actualMinute = int(actualMinute)
				start = workStart.split(":")
				startMinute = int(start[0])
				minuteToCompare = startMinute + 55
				if(actualMinute > minuteToCompare):
					return True

			if compareTime(workStart,lunchStart):
				if isInPause():
					Timer(300.0, timeChecker).start()
					self.notification("Time to take a break!")
				else:
					Timer(3300.0, timeChecker).start()
					self.notification("Time to work now!")

			elif compareTime(lunchStart,lunchEnd):
				self.notification("Time to go eating")
				awayStart = lunchStart.split(":")
				awayEnd = lunchEnd.split(":")
				lunchTimer = (int(awayEnd[0]) - int(awayStart[0])) * 3600
				lunchTimer = lunchTimer + ((int(awayEnd[1]) - int(awayStart[1])) * 60)
				Timer(lunchTimer, timeChecker).start()

			elif compareTime(lunchEnd,workEnd):
				if isInPause():
					Timer(300.0, timeChecker).start()
					self.notification("Time to take a break!")
				else:
					Timer(3300.0, timeChecker).start()
					self.notification("Time to work now! The timer has not started.")

			else:
				self.notification("Now it's not time to work!")
				Timer(timeTo(workStart), timeChecker).start()

		timeChecker() #first call to start the timer

'''
try:
	app = HealthTimer()
	app.clock()
except Exception as gen_error:
	print("Attention, " + str(gen_error))
	input("Press any key to exit..")
'''
app = HealthTimer()
app.clock()
