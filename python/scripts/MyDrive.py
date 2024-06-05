import time

from scripts.logs import log, Level

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class MyDrive:
    def __init__(self) -> None:
        self.credentials_file = 'YOUR-CREDENTIALS-FILE'
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file, scopes=['https://www.googleapis.com/auth/drive'])
        i = 0
        while True:
            try:
                self.service = build('drive', 'v3', credentials=self.credentials) # Getting Drive service.
                return
            except HttpError as error:
                log(
                    e=f"""
                    An error occurred creating drive service:
                    
                    Soon the program will try again automatically.
                    
                    {error}
                    """,
                    flag="mydrive",
                    level=Level.M
                )
                time.sleep(20*i)
                if i < 30:
                    i += 1