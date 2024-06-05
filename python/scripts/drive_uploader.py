import os
import time
from datetime import datetime

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from scripts.logs import log, Level

from scripts.dates import get_todays_file_name
from scripts.drive_reader import searching_for_todays_file_id
from scripts.local_writer import folder

from scripts.MyDrive import MyDrive

# Uploads a file to Drive.
def upload_file(service, date: datetime):
    
    day = get_todays_file_name(date) # Getting file's name
        
    day_id, month_id, _, _ = searching_for_todays_file_id(service, date) # Getting file's id or None.
    
    file_path = os.path.join(folder, f"{day}.csv") # Obtaining the file path.
    
    while True:
        try:
            media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True) # Getting media.
            
            if day_id: # If day_id isn't None.
                # Creating the request to update the file.
                request = service.files().update(
                    uploadType="resumable",
                    fileId=day_id,
                    media_body=media
                )
            else: # Else, day_id is None.
                # Creating the request to create a new file.
                request = service.files().create(
                    uploadType="resumable",
                    media_body=media, 
                    body={
                        'name': f'{day}.csv',
                        'parents': [month_id]
                        }
                )
            response = None
            while response is None:
                _, response = request.next_chunk() # Uploads the next chunk of the file.
                
            return
        
        except HttpError as error:
            log(
                e=f"""
                An error occurred during upload:
                
                Soon the program will try again automatically.
                
                {error}
                """,
                flag="dupload",
                level=Level.M
            )
            time.sleep(20*i)
            if i < 30:
                i += 1