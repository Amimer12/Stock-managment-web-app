import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_sheets_service():
    service_account_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)
    return service
