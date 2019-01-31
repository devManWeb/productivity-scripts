'''
This script is used to auto save when you are using a program
that supports saving by pressing CTRL and S
if you want to change the interval, edit the function time_counter
'''

from threading import Timer
import time
import pyautogui

def time_counter():
    interval = 3600 #seconds
    return interval

def auto_saver():
    hour_minute = time.strftime("%H:%M")
    print("Autosaving " + hour_minute + "..")
    pyautogui.hotkey('ctrl','s') #key combination to send
    Timer(time_counter(), auto_saver).start()

def start():
    print("Start of the program")
    print("Sending the combination every " + str(time_counter()) + "s")
    Timer(time_counter(), auto_saver).start()

try:
    start()
except Exception as gen_error:
    print("Attention: " + gen_error)
    input("Press any key to exit..")
