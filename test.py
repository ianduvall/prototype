#!/usr/bin/env python

# making requests to the umich classes api

import json
import requests


# Trying to request access token
# THIS STILL DOES NOT WORK
# curl -k -d "grant_type=client_credentials&scope=PRODUCTION" -H "Authorization: Basic NnY2UGRoX0s0dW5oanZzSkh1SUlkcUtwRXJBYTpQUTBTRmVNT3pvbVFzU1hTQjBRenpGc213dW9h, Content-Type: application/x-www-form-urlencoded" https://api-km.it.umich.edu/token

key = "uatEnJRH_EDyne8rbD9WEd4IH3Ma"
secret = "skX2k6vTfrz8MHGtfwUdkIoRMRUa"
combined_key = key + ":" + secret
print("combined key: " + combined_key)
encoded_key = combined_key.encode('base64').strip()
print("encoded key: " + encoded_key)

auth_url = "https://api-gw.it.umich.edu/token"
auth_header = {
	"Authorization": "Basic " + encoded_key,
	"Content-Type": "application/x-www-form-urlencoded"
}
auth_data = {
	"grant_type": "client_credentials",
	"scope": "PRODUCTION"
}
auth_response = requests.get(auth_url, params=auth_data, headers=auth_header)
print
print(auth_response.text)
print



# Requests current term (not sure how to get all terms)
# You may need to refresh the auth token manually since the above code doesn't work
# curl -X GET --header "Accept: application/json" --header "Authorization: Bearer 21755e9dfbf737935629d2bf9c39b" "https://api-gw.it.umich.edu/Curriculum/SOC/v1/Terms"
term_code = ""
base_url = "https://api-gw.it.umich.edu/Curriculum/SOC/v1"
headers = {
	"Accept": "application/json",
	"Authorization": "Bearer 21755e9dfbf737935629d2bf9c39b"
}

term_url = base_url + "/Terms"
response = requests.get(term_url, headers=headers)
if response.status_code == 200:
	responseJSON = response.json()
	term_code = responseJSON["getSOCTermsResponse"]["Term"]["TermCode"]
	print("Term Code: {}, Term Description: {}".format(responseJSON["getSOCTermsResponse"]["Term"]["TermCode"], responseJSON["getSOCTermsResponse"]["Term"]["TermDescr"]))

else:
	print(reponse.status_code)
	print(reponse.text)
	exit(1)


# Requests all eecs classes
eecs_classes_url = base_url + "/Terms/{}/Schools/{}/Subjects/{}/CatalogNbrs".format(term_code, "ENG", "EECS")
eecs_classes = requests.get(eecs_classes_url, headers=headers)
if eecs_classes.status_code == 200:
	eecs_classes_json = eecs_classes.json()
	# print eecs_classes_json
	#print(responseJSON["getSOCTermsResponse"]["Term"]["TermDescr"])
	#print(responseJSON["getSOCTermsResponse"]["Term"]["TermCode"])

	for class_obj in eecs_classes_json["getSOCCtlgNbrsResponse"]["ClassOffered"]:
		print("Catalog #: {}, Course Descr: {}".format(class_obj["CatalogNumber"], class_obj["CourseDescr"]))

else:
	print(eecs_classes.status_code)
	print(eecs_classes.text)
	exit(1)


