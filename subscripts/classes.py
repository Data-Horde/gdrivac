import requests, argparse, os, json, queue, threading, bs4

from subscripts.log import log
#CLASSES!

class GDRIVAC_Exception(Exception): pass
class NAGDError(GDRIVAC_Exception): pass
class DoAError(GDRIVAC_Exception): pass

#Singleton Class for checking cookie shapes
#TODO: Write functions to check different cookie shapes
class CookieChecker:
	pass

#Singleton Class for asking for input
class InteractiveAsker:
	cookieInfoShown = False
	def cookieInfoMessage(self):
		if not self.cookieInfoShown:
			print("""Welcome to G-Drivac, the vaccine that protects your Google Drive account from Link Rot!
On Sep 13 2021, Google Drive will forcibly private a lot of publically shared URLs, details are available here:
https://workspaceupdates.googleblog.com/2021/06/drive-file-link-updates.html

Important Note: Google Docs, Sheets, and Slides files are NOT impacted by this change, see https://support.google.com/a/answer/10685032

To be able to associate your Google account with Drive links, you will need to specify your session cookies.
Don't worry! These are only stored locally, you won't be exposing your account to anyone.

TODO: EXPLAIN HOW TO CHECK COOKIES
TODO: EXPLAIN HOW TO EXPORT COOKIES""")
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

	#OTHER
	HEADERS={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
	}


	def isAccessed(self, HTML):
		#CHECK FOR <meta property="og:site_name" content="Google Docs">
		#print(bs4.BeautifulSoup(HTML,features="lxml").find("meta",  {"property":"og:site_name"})["content"] or False)

		#FOR FILES
		title = bs4.BeautifulSoup(HTML,features="lxml").find("meta",  {"property":"og:site_name"})
		if title and title.get("content") == "Google Docs":
			return True
		#FOR FOLDERS
		return HTML.find('drive_hist_state') != -1

		return False
	def askingForAccount(self, HTML):
		#CHECK FOR https://accounts.google.com/signin/v1/lookup
		return HTML.find("https://accounts.google.com/signin/v1/lookup") != -1

	#Main Function
	def immunize(self,args,visit_queue, cookie_payload):
		while True:
			#GET URL FROM QUEUE
			try:
				URL = visit_queue.get(block=0)
			except queue.Empty:
				with self.print_lock: log("\033[32mQueue is empty\033[0m")
				return

			#URL FROM QUEUE RECEIVED
			try:
				#GOOD NEWS: You should NOT need to thread-lock on URL requests
				#It would be great if I could confirm this

				r = requests.get(URL,stream=True,cookies=cookie_payload, headers=self.HEADERS)

				with self.print_lock: log("\033[93mAccessing {}\nStatus: {}\033[0m".format(URL,r.status_code))

				#print(r.text)
				#CHECK IF non-200 status
				if r.status_code < 200 or r.status_code >= 300:
					with self.print_lock: log("\033[94mRequeuing...\033[0m")
					self.visit_queue.put(URL)
					continue

				#WARNING!
				#ACCESS DENIALS DIRECT TO SIGN-IN PAGE WHICH DOES GIVE STATUS 200
				#WE NEED A WAY TO DETECT THIS

				with open('debug.html', 'w') as f: f.write(r.text)

				if self.isAccessed(r.text):
					with self.print_lock:  log("\033[90mAccount associated with {}\nStatus: {}\033[0m".format(URL,r.status_code))
				elif self.askingForAccount(r.text):
					raise DoAError("\033[91mERROR: File Access Denied for {}\033[0m".format(URL))
				elif not args.ignoreNonDrive:
					raise NAGDError("\033[91mERROR: '{}' is not a Google Drive file URL!\nPass -ignoreNonDrive flag to ignore\033[0m".format(URL))

			#If the URL is invalid
			except requests.exceptions.MissingSchema:
				with self.print_lock: log("\033[91mERROR: '{}' is not a properly formatted URL!\033[0m".format(URL))
				#Do NOT add back into the queue
			#If the Connection is DEAD
			except requests.exceptions.ConnectionError:
				with self.print_lock: log("\033[91mERROR: No Connection\n\033[94mRequeuing {}\033[0m".format(URL))
				self.visit_queue.put(URL)
				#SLEEP
				e = threading.Event()
				e.wait(timeout=0.5) 
			#If the URL is not a GD link, Not A Google Drive Error
			except NAGDError as e:
				with self.print_lock: 
					log(e)
					if args.ignoreNonDrive:
						log("\033[94mRequeuing...\033[0m")
						self.visit_queue.put(URL)
			#If the URL is not accessible for some reason, Denial of Access Error
			except DoAError as e:
				with self.print_lock: 
					log(e)
					#TODO: CHECK PAYLOAD AGAIN
					#MIGHT BE NECESSARY IF COOKIES EXPIRE
					log("\033[94mRequeuing...\033[0m")
				self.visit_queue.put(URL)
			#Other Problems
			except Exception as e:
				with self.print_lock: log("\033[91mERROR: {}\033[0m".format(e))
				#Add back into the queue?
				self.visit_queue.put(URL)
				#SLEEP
				e = threading.Event()
				e.wait(timeout=0.5) 

	def request(self,args,URLs,cookie_payload):

		#TODO: Maybe check for duplicates?
		for URL in URLs:
			self.visit_queue.put(URL)

		THREADCOUNT = args.tcount or 6

		for i in range(THREADCOUNT): #Launch threads
			thread = threading.Thread(target=self.immunize, args=(args, self.visit_queue, cookie_payload ,))
			thread.name = i
			thread.start()
			self.worker_list.append(thread)
