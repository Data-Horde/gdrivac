#TODO: REQUIREMENTS FILE
import requests, argparse, os, json

#Internal Imports
from subscripts.classes import *

def main():
	#CONSTANTS
	COOKIEFILE = 'cookies.json'
	IA = InteractiveAsker()
	IM = Immmunizer()
	CC = CookieChecker()

	#PARSE ARGUMENTS

	parser = argparse.ArgumentParser(description="I NEED A DESCRIPTION")
	#TODO: ADD A DESCRIPTION
	
	parser.add_argument("url",type=str,help="Google Drive URL to immunize against")
	#TODO: ALLOW FOR FILE INPUT INSTEAD OF URL
	
	parser.add_argument("-sid",type=str,help="Specify cookie value for SID")
	parser.add_argument("-ssid",type=str,help="Specify cookie value for SSID")
	parser.add_argument("-hsid",type=str,help="Specify cookie value for HSID")
	
	args = parser.parse_args()

	#UNPARSE

	URL = (args.url or "")
	#newCookies = (args.sid, args.ssid, args.hsid)

	#COOKIE PAYLOAD
	if not os.path.exists(COOKIEFILE):
		with open(COOKIEFILE, 'w') as cookiefile:
			cookiefile.write('{}')
	
	#Read Cookies
	cookie_payload = {}
	try:
		with open(COOKIEFILE, 'r') as cookiefile:
			cookie_payload = json.load(cookiefile)
	except:
		print("{} is corrupted, resetting cookie payload".format(COOKIEFILE))

	#Update Session Cookies
	if args.sid: cookie_payload['SID'] = args.sid
	if args.ssid: cookie_payload['SSID'] = args.ssid
	if args.hsid: cookie_payload['HSID'] = args.hsid

	#Check and ask interactively for MISSING user session cookies
	if not cookie_payload.get('SID'): cookie_payload['SID']= IA.askFor('SID')
	if not cookie_payload.get('SSID'): cookie_payload['SSID'] =  IA.askFor('SSID')
	if not cookie_payload.get('HSID'): cookie_payload['HSID'] =  IA.askFor('HSID')

	#TODO: Check for cookies shape using CookieChecker CC
	#CC.()

	#Save cookies file
	with open(COOKIEFILE, "w") as cookiefile:
		json.dump(cookie_payload, cookiefile)

	#print(args.sid, args.ssid, args.hsid)
	#print (cookie_payload)

	#GET IMMUNIZED

	IM.immunize(URL,cookie_payload)

if __name__ == '__main__':
	main()