#!/usr/bin/env python

# making requests to the umich classes api

import json
import requests


# Trying to request access token
# THIS STILL DOES NOT WORK
# curl -k -d "grant_type=client_credentials&scope=PRODUCTION" -H "Authorization: Basic NnY2UGRoX0s0dW5oanZzSkh1SUlkcUtwRXJBYTpQUTBTRmVNT3pvbVFzU1hTQjBRenpGc213dW9h, Content-Type: application/x-www-form-urlencoded" https://api-km.it.umich.edu/token

key = "ojLHnLN3a6Ma6Rn_fk2niTFlr7Ea"
secret = "YEqiqUlJtL4EQdSBhf_Sh43zrf0a"
access_token = "439ce028ab2e8d4619c9223e9f8bec5"


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
	"Authorization": "Bearer " + access_token
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
# eecs_classes_url = base_url + "/Terms/{}/Schools/{}/Subjects/{}/CatalogNbrs".format(term_code, "ENG", "EECS")
# eecs_classes = requests.get(eecs_classes_url, headers=headers)
# if eecs_classes.status_code == 200:
# 	eecs_classes_json = eecs_classes.json()

# 	for class_obj in eecs_classes_json["getSOCCtlgNbrsResponse"]["ClassOffered"]:
# 		print("Catalog #: {}, Course Descr: {}".format(class_obj["CatalogNumber"], class_obj["CourseDescr"]))

# else:
# 	print(eecs_classes.status_code)
# 	print(eecs_classes.text)
# 	exit(1)



def get_all_courses_for_subject(term_c, school_c, subject_c):
	courses_url = base_url + "/Terms/{}/Schools/{}/Subjects/{}/CatalogNbrs".format(term_c, school_c, subject_c)
	courses = requests.get(courses_url, headers=headers)
	if courses.status_code != 200:
		print(courses.status_code)
		print(courses.text)
		exit(1)

	courses_json = courses.json()

	if "getSOCCtlgNbrsResponse" not in courses_json or \
	"ClassOffered" not in courses_json["getSOCCtlgNbrsResponse"]:
		print("\t\t- Empty")
		return
		
	# loop through classes
	for course in courses_json["getSOCCtlgNbrsResponse"]["ClassOffered"]:
		if type(course) is dict:
			print("\t\t- {}".format(course["CatalogNumber"]))
		else:
			if course == "CatalogNumber":
				print("\t\t- {}".format(courses_json["getSOCCtlgNbrsResponse"]["ClassOffered"][course]))

	return # get_all_classes_for_subject


# Requests all classes
schools_url = base_url + "/Terms/{}/Schools".format(term_code)
schools = requests.get(schools_url, headers=headers)
if schools.status_code != 200:
	print(schools.status_code)
	print(schools.text)
	exit(1)

schools_json = schools.json()

# loop through schools
for school in schools_json["getSOCSchoolsResponse"]["School"]:
	school_code = school["SchoolCode"]
	print(school_code)

	subjects_url = base_url + "/Terms/{}/Schools/{}/Subjects".format(term_code, school_code)
	subjects = requests.get(subjects_url, headers=headers)
	if subjects.status_code == 200:
		subjects_json = subjects.json()

		# loop through subjects
		for subject in subjects_json["getSOCSubjectsResponse"]["Subject"]:
			if school_code == "INF" or \
			school_code == "LAW" or \
			school_code == "NRE" or \
			school_code == "IPP" or \
			school_code == "SW":
				if subject == "SubjectCode":
					subject_code = subjects_json["getSOCSubjectsResponse"]["Subject"]["SubjectCode"]
					print("\t- {}".format(subject_code))
				else:
					continue
			else:
				if "SubjectCode" in subject:
					subject_code = subject["SubjectCode"]
					print("\t- {}".format(subject_code))
				else:
					print("SubjectCode not in Subject")
					continue

			# gets all courses for subject code, prints for now
			get_all_courses_for_subject(term_code, school_code, subject_code)


