from datetime import datetime

from scripts.drive_reader import get_id_by_name
from scripts.drive_writer import create_drive_folder
from scripts.dates import get_parent_folders_names

# Provides parent folders. Creates them if they don't exist.
def get_parent_folders(service, date: datetime):
    month, year = get_parent_folders_names(date) # Getting parent folders names.

    data_id = get_data_id(service) # Getting root folder id.
    
    # Getting ids for each parent folder.
    year_id = get_id_by_name(service, year, data_id)
    month_id = get_id_by_name(service, month, year_id)
    
    if not year_id: # If year folder doesn't exist.
        year_id = create_drive_folder(service, year, data_id) # Creating year folder.
    
    if not month_id: # If year folder doesn't exist.
        month_id = create_drive_folder(service, month, year_id) # Creating year folder.

    return [month_id, year_id, data_id]

# Provides root folder. Creates it if it doesn't exist.
def get_data_id(service):
    data_name = "Data"
    data_id = get_id_by_name(service, data_name) # Getting root folder id or None.
    
    if data_id: # if isn't None.
        return data_id
    else:
        return create_drive_folder(service, data_name) # Creates root folder.