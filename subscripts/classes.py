import requests, argparse, os, json, queue, threading

from subscripts.log import log
#CLASSES!

#Singleton Class for checking cookie shapes
#TODO: Write functions to check different cookie shapes
class CookieChecker:
	pass

#Singleton Class for asking for input
class InteractiveAsker:
	cookieInfoShown = False
	def cookieInfoMessage(self):
		if not self.cookieInfoShown:
			print("""Welcome to G-Drivac, the vaccine that protects your Google Drive account!\n
To continue, please add your session cookies.
TODO: EXPLAIN THIS PART""")
			self.cookieInfoShown = True
	def askFor(self,s):
		self.cookieInfoMessage()
		inp = input("Please enter the value for your "+s+" session cookie:")
		#TODO: Check for cookies shape using CookieChecker
		print(inp)
		return inp

#Immunization Routines
class Immmunizer:

	#IMMUNIZATION QUEUE VARIABLES
	worker_list = []
	visit_queue = queue.Queue()
	print_lock = threading.Lock()

	def immunize(self,args,visit_queue, cookie_payload):
		while True:
			#GET URL FROM QUEUE
			try:
				URL = visit_queue.get(block=0)
			except queue.Empty:
				with self.print_lock:
					log("\033[32mQueue is empty\033[0m")
				return

			#URL FROM QUEUE RECEIVED
			try:
				#TODO: CHECK IF GOOGLE DRIVE LINK OR ADD A PAREMETER TO IGNORE?

				#OPTIONAL: CHECK PAYLOAD AGAIN
				#MIGHT BE NECESSARY IF COOKIES EXPIRE

				#GOOD NEWS: You should NOT need to thread-lock on URL requests
				#It would be great if I could confirm this

				#URL = "https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI"
				r = requests.get(URL,cookies=cookie_payload)

				with self.print_lock:
					log("\033[93mAccessing {}\nStatus: {}\033[0m".format(URL,r.status_code))

				#print(r.text)
				#CHECK IF non-200 status
				if r.status_code < 200 or r.status_code >= 300:
					with self.print_lock:
						log("\033[94mRequeuing...\033[0m")
					self.visit_queue.put(URL)
			#CHECK IF LINK using requests.exceptions.MissingSchema
			except requests.exceptions.MissingSchema:
				with self.print_lock:
					log("\033[91mERROR: '{}' is not a properly formatted URL!\033[0m".format(URL))
				#Do NOT add back into the queue
			#CONNECTION DEAD?
			except requests.exceptions.ConnectionError:
				with self.print_lock:
					log("\033[91mERROR: No Connection\n\033[94mRequeuing {}\033[0m".format(URL))
				self.visit_queue.put(URL)
				#TODO: ADD A SLEEP HERE?
			except Exception as e:
				with self.print_lock:
					log("\033[91mERROR: {}\033[0m".format(e))
				#Add back into the queue?
				self.visit_queue.put(URL)
				#TODO: ADD A SLEEP HERE?

	def request(self,URL,cookie_payload):
		#TODO: ADAPT THIS FOR MULTIPLE URLs
		self.visit_queue.put(URL)

		#TODO: PARAMETERIZE THREAD COUNT
		THREADCOUNT = 3

		#TODO: PASS ARGS FROM FUNCTION CALL
		my_args = None

		for i in range(THREADCOUNT): #Launch threads
			thread = threading.Thread(target=self.immunize, args=(my_args, self.visit_queue, cookie_payload ,))
			thread.name = i
			thread.start()
			self.worker_list.append(thread)
