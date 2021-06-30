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
	parser.add_argument("URL",type=str,help="Google Drive URL to immunize against")
	#TODO: ALLOW FOR FILE INPUT INSTEAD OF URL
	#TODO: SESSION COOKIES
	args = parser.parse_args()

	URL = (args.URL or -1)
	immunize(URL)