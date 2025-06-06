import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

TOKEN_PICKLE = 'token.pickle'

def get_sheets_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials. Run auth_flow.py first.")
    return build('sheets', 'v4', credentials=creds)
