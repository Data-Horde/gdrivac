import requests, argparse

def immunize(URL):
	#TODO: CHECK IF GOOGLE DRIVE LINK
	
	#URL = "https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI"
	r = requests.get(URL)

	print("Status for URL: {}".format(URL))
	print(r.status_code)
	#TODO CHECK IF non-200 status

if __name__ == '__main__':
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
	print(args.sid, args.ssid, args.hsid)
	
	immunize(URL)