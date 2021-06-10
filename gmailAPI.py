from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

# if modifying these scopes, delete token.pickle
scopes = ['https://www.googleapis.com/auth/gmail.modify']

global messages, msg, sender, subject
global info


def checkemail():
    info = "You don\'t have any unread messages"
    creds = None
    fname1 = 'token.pickle'
    fname2 = 'credentials.json'
    # The file token.pickles stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(fname1):
        with open(fname1, 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(fname2, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credential for the next run
        with open(fname1, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Get Unread email from the inbox
    result = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = result.get('messages', [])

    # Display Messages
    if not messages:
        print(info)
    else:
        msg_count = 0
        for message in messages:
            msg_count = msg_count + 1
        print('You have ' + str(msg_count) + " messages. ")
        if msg_count != 0:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                data = msg['payload']['headers']
                for values in data:
                    name = values["name"]
                    if name == "From":
                        sender = values["value"]

                for values in data:
                    name = values["name"]
                    if name == "Subject":
                        subject = values["value"]

                print("From: " + sender + ":")
                print("Subject: " + subject)
                print("     " + msg['snippet'][:50])
                print("\n")
                time.sleep(1)

# checkemail()
