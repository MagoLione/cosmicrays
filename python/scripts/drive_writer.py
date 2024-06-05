import time

from googleapiclient.errors import HttpError

from scripts.logs import log, Level

# Creats a drive folder.
def create_drive_folder(service, folder_name: str, parent_folder_id: str|None = None):
    
    i = 0
    while True:
        try:
            # Setting folder metadata.
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            # If isn't None, sets the parent folder in metadata.
            if parent_folder_id:
                folder_metadata['parents'] = [parent_folder_id]
            
            folder = service.files().create(body=folder_metadata, fields='id').execute() # Creating a folder.
        
            return folder.get('id')
        except HttpError as error:
            log(
                e=f"""
                An error occurred creating a folder:
                
                Soon the program will try again automatically.
                
                {error}
                """,
                flag="dwriter",
                level=Level.M
            )
            time.sleep(20*i)
            if i < 30:
                i += 1