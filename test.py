#!/usr/bin/env python

# making requests to the umich classes api

import json
import requests


# Trying to request access token
# curl -k -d "grant_type=client_credentials&scope=PRODUCTION" -H "Authorization: Basic NnY2UGRoX0s0dW5oanZzSkh1SUlkcUtwRXJBYTpQUTBTRmVNT3pvbVFzU1hTQjBRenpGc213dW9h, Content-Type: application/x-www-form-urlencoded" https://api-km.it.umich.edu/token

key = "uatEnJRH_EDyne8rbD9WEd4IH3Ma"
secret = "skX2k6vTfrz8MHGtfwUdkIoRMRUa"
combined_key = key + ":" + secret
encoded_key = combined_key.encode('base64').strip()
# print encoded_key

auth_url = "https://api-gw.it.umich.edu/token"
auth_header = {
	"Authorization": encoded_key,
	"Content-Type": "application/x-www-form-urlencoded"
}
auth_data = {
	"grant_type": "client_credentials&scope=PRODUCTION"
}
auth_response = requests.get(auth_url, params=auth_data, headers=auth_header)
print
print(auth_response.text)
print



# Trying to access terms using given auth token
# curl -X GET --header "Accept: application/json" --header "Authorization: Bearer 21755e9dfbf737935629d2bf9c39b" "https://api-gw.it.umich.edu/Curriculum/SOC/v1/Terms"

url = "https://api-gw.it.umich.edu/Curriculum/SOC/v1/Terms"
headers = {
	"Accept": "application/json",
	"Authentication": "Bearer fad88c2ed53326d5696a4b9c65de11"
}
response = requests.get(url, headers=headers)
print
print(response.text)
print