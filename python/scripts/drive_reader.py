import time

from datetime import datetime

from googleapiclient.errors import HttpError

from scripts.logs import log, Level
from scripts.dates import get_todays_file_name

error_flag = "dreader"

# Gets file id by file name.
def get_id_by_name(service, name: str, parent_folder_id: str = None ):
    
    query = f"name = '{name}'" # Creating a query.
    if parent_folder_id: # If is setted.
        query += f" and '{parent_folder_id}' in parents" # Modifing the query.
        
    i = 0
    while True:
        try:
            results = service.files().list(q=query).execute() # Executing the request.
            items = results.get('files', []) # Getting the files.

            if items: # If items isn't empty.
                return items[0]['id']
            else:
                return None
        except HttpError as error:
            log(
                e=f"""
                An error occurred getting drive file id from the name:
                
                Soon the program will try again automatically.
                
                {error}
                """, 
                flag=error_flag,
                level=Level.M
            )
            time.sleep(20*i)
            if i < 30:
                i += 1
    
# Gets file name by file id.
def get_name_by_id(service, id: str):
    
    i = 0
    while True:
        try:
            file = service.files().get(fileId=id).execute() # Executing the request.
            return file['name']

        except HttpError as error:
            log(
                e=f"""
                An error occurred getting drive file name from the id:
                
                Soon the program will try again automatically.
                
                {error}
                """, 
                flag=error_flag,
                level=Level.M
            )
            time.sleep(20*i)
            if i < 30:
                i += 1

# Gets today's file's id or None.
def searching_for_todays_file_id(service, date: datetime):
    from scripts.drive_provider import get_parent_folders
    
    day = get_todays_file_name(date) # Getting file name.
    month_id, year_id, data_id = get_parent_folders(service, date) # Getting parent folders.
    
    day_id = get_id_by_name(service, f"{day}.csv", month_id) # Getting file id.
    
    return [day_id, month_id, year_id, data_id]
        