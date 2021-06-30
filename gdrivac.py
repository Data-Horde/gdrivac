import requests

URL = 'https://docs.google.com/document/d/12pOhaaFh998B0kyc5Sm4IhlhIp1c9t5gDNTVVPaiJgI' 

r = requests.get(URL)

print("Status for URL: {}".format(URL))
print(r.status_code)