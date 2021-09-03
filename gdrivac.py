try:
	import requests, argparse, os, json, random, time, datetime
except:
	print("Hmm... import error. Did you remember to run\n$pip install -r requirements.txt")

#Internal Imports
from subscripts.classes import *

def timeRemaining():
	DEADLINE = datetime.datetime(year=2021,month=9,day=13)
	if datetime.datetime.now() > DEADLINE:
		return "ANY MINUTE NOW"
	else:
		diff = DEADLINE - datetime.datetime.now()
		return str(diff.days) + " days, " + str(diff.seconds//3600) + " hours, " + str((diff.seconds%3600)//60) + " minutes"

def main():

	#CONSTANTS
	COOKIEFILE = 'cookies.json'
	IA = InteractiveAsker()
	IM = Immmunizer()
	CC = CookieChecker()

	HELLOMESSAGE = "\033[93mWelcome to Google-Drivac!\nStarting up...\n\033[90m" + random.choice([
	"TIP: \033[93mGoogle Docs, Sheets, and Slides files are NOT impacted by the security update\033[90m",
	"TIP: \033[93mYou can pass multiple .txt files to GDrivac with\n\033[92m$ gdrivac.py -f file1.txt file2.txt\033[90m",
	"TIP: \033[93mYou can export your browser cookies as cookies.json into the gdrivac folder.\033[90m",
	"TIP: \033[91mApproximate time remaining until September 13:\n{}\033[90m".format(timeRemaining()),
	])

	#PARSE ARGUMENTS

	parser = argparse.ArgumentParser(description="""Google-Drivac: Vaccinate Against Link Rot!
On Sep 13 2021, Google Drive will forcibly private a lot of publicly shared URLs, details are available here:
https://workspaceupdates.googleblog.com/2021/06/drive-file-link-updates.html

Important Note: Google Docs, Sheets, and Slides files are NOT impacted by this change, see https://support.google.com/a/answer/10685032

Luckily, if you access a shared link before that date, your Google account will be able to continue accessing it after the deadline.
Google-Drivac is a tool to associate a Google account with a list of Google Drive links.

Install requirements with $pip install -r requirements.txt
""")

	#ALLOW FOR MULTIPLE URLs
	parser.add_argument("-url",nargs='+',type=str,help="Google Drive URL(s) to immunize against.\nMultiple URLs can be specified in succession.")
	parser.add_argument("-files",nargs='+',type=str,help="Files with Drive URL(s) to immunize against.\nMultiple files can be specified in succession.\nSupported Formats:\n*.txt seperated by newlines.TBA")
	
	parser.add_argument("-sid",type=str,help="Specify cookie value for SID")
	parser.add_argument("-ssid",type=str,help="Specify cookie value for SSID")
	parser.add_argument("-hsid",type=str,help="Specify cookie value for HSID")
	parser.add_argument("-tcount",type=int,help="Thread count (default = 6)")
	parser.add_argument("-ignoreNonDrive",type=int,default=0,help="Requeue non-Google Drive URLs if a failure occurs. Not recommended unless you are repurposing the script.")
	
	args = parser.parse_args()

	#UNPARSE

	files = (args.files or [])
	URLs = (args.url or [])

	for file in files:
		if file[-4:] == '.txt':
			with open(file, 'r') as cookiefile:
				nextline = cookiefile.readline()
				while nextline:
					URLs.append(nextline.strip())
					nextline = cookiefile.readline()

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

	#SHOW TODAY'S HELLO MESSAGE
	print(HELLOMESSAGE)
	time.sleep(5)

	#GET IMMUNIZED
	if len(URLs):
		IM.request(args,URLs,cookie_payload)
	else:
		print("\033[91mNo URLs provided.\nStopped.\033[0m")

if __name__ == '__main__':
	main()