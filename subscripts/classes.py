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

				#URL = "https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI"
				r = requests.get(URL,cookies=cookie_payload)

				print("Status for URL {}:".format(URL))
				print(r.status_code)
				#print(r.text)
				#TODO: CHECK IF non-200 status
			#CHECK IF LINK using requests.exceptions.MissingSchema
			except requests.exceptions.MissingSchema:
				print("ERROR: '{}' is not a properly formatted URL!".format(URL))
				#Do NOT add back into the queue
			except Exception as e:
				print("ERROR: {}".format(e))
				#Add back into the queue?
				self.visit_queue.put(URL)

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
