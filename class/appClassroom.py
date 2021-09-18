from __future__ import print_function
import os.path
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

def getLsitOfCourses(service):
    try:
        result = service.courses().list(pageSize=10).execute()
        listOfCourses = result.get('courses',[])
        
        if not listOfCourses:
            print("No list of Courses found.")
        else:
            for course in listOfCourses:
                print("CourseId : "+ course['name'] + "\nid : " + course['id'])
                

    except errors.HttpError as error:
        print(f"An error occured: {error}")

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