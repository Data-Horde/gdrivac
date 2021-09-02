#Log function taken from Pyxia's mf-dl tool for bulk-downloading MediaFire links

#https://gitgud.io/Pyxia/mf-dl/-/blob/master/log.py
#This is not only a "Did Not Steal" disclaimar, but also a promotion
#Seriously, check out mf-dl out 

import threading
from colorama import init
init() #This should fix ansi escape codes on windows TODO: test it

def log(msg):
	thread_name = threading.current_thread().name
	if(thread_name != "MainThread"):
		print("\033[90mThread #{}\033[0m ".format(thread_name), end="")
	print(msg)
