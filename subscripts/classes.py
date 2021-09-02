#Singleton Class for checking cookie shapes
#TODO: Write functions to check different cookie shapes
class CookieChecker:
	pass
import requests, argparse, os, json

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

class Immmunizer:
	def immunize(self,URL,cookie_payload):
		#TODO: CHECK IF LINK using requests.exceptions.MissingSchema
		#TODO: CHECK IF GOOGLE DRIVE LINK
		#TODO: CHECK PAYLOAD

		#URL = "https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI"
		r = requests.get(URL,cookies=cookie_payload)

		print("Status for URL {}:".format(URL))
		print(r.status_code)
		#print(r.text)
		#TODO CHECK IF non-200 status