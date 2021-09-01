#TODO: REQUIREMENTS FILE
import requests, argparse

def immunize(URL,cookie_payload):
	#TODO: CHECK IF GOOGLE DRIVE LINK
	#TODO: CHECK PAYLOAD
	
	#URL = "https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI"
	r = requests.get(URL,cookies=cookie_payload)

	print("Status for URL {}:".format(URL))
	print(r.status_code)
	#print(r.text)
	#TODO CHECK IF non-200 status

def main():

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
	newCookieSID = (args.sid or "")
	newCookieSSID = (args.ssid or "")
	newCookieHSID = (args.hsid or "")

	#TODO: Check for SESSION COOKIES file cookies.json

	#TODO: If not found make one

	#TODO: If cookies specified in function call arguments, overwrite

	#TODO: Check and ask interactively for MISSING user session cookies

	#TODO: Save cookies file

	#TODO: INIT COOKIE PAYLOAD

	#print(args.sid, args.ssid, args.hsid)
	cookie_payload = {'SID':newCookieSID, 'SSID':newCookieSSID, 'HSID':newCookieHSID}
	#print (cookie_payload)

	#GET IMMUNIZED
	immunize(URL,cookie_payload)

if __name__ == '__main__':
	main()