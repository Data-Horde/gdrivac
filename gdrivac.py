#TODO: REQUIREMENTS FILE
import requests, argparse, os, json

def immunize(URL,cookie_payload):
	#TODO: CHECK IF LINK using requests.exceptions.MissingSchema
	#TODO: CHECK IF GOOGLE DRIVE LINK
	#TODO: CHECK PAYLOAD
	
	#URL = "https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI"
	r = requests.get(URL,cookies=cookie_payload)

	print("Status for URL {}:".format(URL))
	print(r.status_code)
	#print(r.text)
	#TODO CHECK IF non-200 status

def main():

	#CONSTANTS
	COOKIEFILE = 'cookies.json'

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
		with open(COOKIEFILE, 'w') as f:
			f.write('{}')
	
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

	#TODO: Check and ask interactively for MISSING user session cookies
	if not cookie_payload.get('SID'): print('uh oh SID is missing')
	if not cookie_payload.get('SSID'): print('uh oh SSID is missing')
	if not cookie_payload.get('HSID'): print('uh oh HSID is missing')

	#TODO: Save cookies file

	#print(args.sid, args.ssid, args.hsid)
	#cookie_payload = {'SID':newCookieSID, 'SSID':newCookieSSID, 'HSID':newCookieHSID}
	#print (cookie_payload)

	#GET IMMUNIZED
	
	immunize(URL,cookie_payload)

if __name__ == '__main__':
	main()