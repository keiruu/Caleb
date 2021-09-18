from __future__ import print_function
import os.path
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/classroom.announcements.readonly", "https://www.googleapis.com/auth/classroom.courses.readonly"]

courses = []
coursesDict = {}

def getListOfCourses(service):
    try:
        result = service.courses().list(pageSize=10).execute()

        listOfCourses = result.get('courses',[])
        
        #create a dictionary with the courseId and courseName
        #example: course_names = {'courseId': '275433710203', 'name': '2021-2-SS105E-BSIT2A'}
        # A copy of a_dictionary is appended to a_list instead of appending a_dictionary directly 
        # because that would produce a reference to a_dictionary instead of a copy.

        for x in range(len(listOfCourses)):
            coursesDict['courseId'] = listOfCourses[x].get("id")
            coursesDict['name'] = listOfCourses[x].get("name")
            coursesDict_copy = coursesDict.copy()
            courses.append(coursesDict_copy)
            
        if not listOfCourses:
            print("No list of Courses found.")
        else:
            print(listOfCourses)

    except errors.HttpError as error:
        print("An error occured: {error}")

def getAnnouncements(service):
    try:
        #code to get all announcements
        resultDict = {}
        result = service.courses().announcements().list(courseId=courses[9].get("courseId")).execute()
        
        #waay pa ni matapos, basically creating the message for 
        #delivering the announcements to the user
        for x in range(len(listOfCourses)):
            result = service.courses().announcements().list(courseId=courses[x].get("courseId")).execute()
            listOfAnnouncements = result.get('announcements',[])

            if not result:
                print("No announcements")
            else:
                print("Announcement: ", courses[x].get("name"))
                listOfAnnouncements[0].get("text")

        
        if not listOfAnnouncements:
            print("No list of Announcements found.")
        else:
            print(listOfAnnouncements)

    except errors.HttpError as error:
        print("An error occured: {error}")

def getService():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('classroom', 'v1', credentials=creds)    

    return service

service = getService()
