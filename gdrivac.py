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
	parser = argparse.ArgumentParser(description="I NEED A DESCRIPTION")
	#TODO: ADD A DESCRIPTION
	
	parser.add_argument("url",type=str,help="Google Drive URL to immunize against")
	#TODO: ALLOW FOR FILE INPUT INSTEAD OF URL
	
	parser.add_argument("-sid",type=str,help="SID session ID")
	parser.add_argument("-ssid",type=str,help="SSID session ID")
	parser.add_argument("-hsid",type=str,help="HSID session ID")
	#TODO: Read SESSION COOKIES from a file
	
	args = parser.parse_args()

	URL = (args.url or "")

	#print(args.sid, args.ssid, args.hsid)
	cookie_payload = {'SID':(args.sid or ""), 'SSID':(args.ssid or ""), 'HSID':(args.hsid or "")}
	#print (cookie_payload)
	immunize(URL,cookie_payload)

if __name__ == '__main__':
	main()