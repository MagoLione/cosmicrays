import io
import os
import time

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from scripts.logs import log, Level

from scripts.drive_reader import get_name_by_id

from scripts.MyDrive import MyDrive

from scripts.local_writer import folder

# A function to download a file from Drive.
def download_file(service, file_id: str, file_name: str|None = None):

    # If it's None gets the file name.
    if not file_name:
        file_name = get_name_by_id(service, file_id)
        
    i = 0
    while True:
        try:
            request = service.files().get_media(fileId=file_id) # Getting the request to download the file with the specified id.
            file = io.BytesIO() # Getting a stream of in-memory bytes.
            downloader = MediaIoBaseDownload(file, request) # Getting the downloader.
            done = False
            while done is False:
                _, done = downloader.next_chunk() # Get the next chunk of the download.
            
            break # Exiting from while cycle.

        except HttpError as error:
            log(
                e=f"""
                An error occurred during drive download:
                
                Soon the program will try again automatically.
                
                {error}
                """,
                flag="ddownloader",
                level=Level.M
            )
            time.sleep(20*i)
            if i < 30:
                i += 1
    
    # Writing a file (in folder folder and with file_name file name) in binary mode.
    with open(os.path.join(folder, file_name), "wb") as f:
        f.write(file.getvalue())

    return file.getvalue()