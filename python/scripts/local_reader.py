import os
import json
import time

from datetime import datetime

from scripts import paths

from scripts.logs import log, Level

from scripts.Track import Settings
from scripts.local_writer import initialize_settings, reinitialize_active, reinitialize_angle
from scripts.dates import get_todays_file_name

# Search if today's file exists in local folder using date.
def is_there_the_correct_file(date: datetime) -> bool:
    day_name = get_todays_file_name(date) # Getting file name.
        
    return is_there_the_correct_file_by_name(day_name)

# Search if today's file exists in local folder using name.
def is_there_the_correct_file_by_name(day_name: str) -> bool:
    
    for file in os.listdir(paths.data_folder): # For each file in local folder.
        if file == f"{day_name}.csv": # If is equal to the file it's seaching for.
            return True
        
    return False

# Reads the settings file, returns a Settings object.
def read_settings() -> Settings:
    a_data = None
    data = None
    
    a_i = 0
    
    while a_data == None:
        
        try:
            with open(os.path.join(paths.settings_folder, paths.automode_file), "r") as a_f: # Opening file in reading mode.
                json_a_data = a_f.read() # Reading file.
                
                if json_a_data == "": # If the is empty.
                    return initialize_settings() # Initializing settings.
                    
                a_data = json.loads(json_a_data) # Deconding json data.
                
            break # Exiting the while cycle.
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if a_i > 0:
                log(
                    e=f"""
                    An error occurred reading automode.json file:
                            
                    If it only occurred once it isn't a problem.
                    If it repeats check the file status and the users.
                    
                    {e}
                    
                    """,
                    flag="localreader",
                    level=Level.L
                )
        
        a_i += 1
        
        time.sleep(0.2)
            
    is_enabled = a_data.get('enabled') # Getting enabled setting value.
        
    if not is_enabled: # If is None.
        return initialize_settings() # Initializing settings.
    
    
    i = 0
    
    while data == None:
        
        try:
            with open(os.path.join(paths.settings_folder, paths.settings_file), "r") as f: # Opening file in reading mode.
                json_data = f.read() # Reading file.
                
                if json_data == "": # If the is empty.
                    return initialize_settings() # Initializing settings.
                
                data = json.loads(json_data) # Deconding json data.
                
            break # Exiting the while cycle.
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if i > 0:
                log(
                    e=f"""
                    An error occurred reading settings.json file:
                            
                    If it only occurred once it isn't a problem.
                    If it repeats check the file status and the users.
                    
                    {e}
                    
                    """,
                    flag="localreader",
                    level=Level.L
                )
        
        i += 1
        
        time.sleep(0.2)
        
        
    
    active = data.get('active') # Getting active setting value.
    angle = data.get('angle') # Getting angle setting value.

    if active == None or angle == None: # If a setting is None.
        settings = initialize_settings() # Initializing and saving settings.
    else:
        # Saving settings with readed one.
        settings = Settings(
            active = active,
            angle = angle,
            description = data.get('description')
        )
        
        # Handling active invalid values.
        if not isinstance(active, bool):
            print("\nInvalid value in Active field.")
            settings = reinitialize_active(settings)
        
        # Handling angle invalid values.
        if not isinstance(angle, int) or angle < 0 or angle > 180:
            print("\nInvalid value in Angle field.")
            settings = reinitialize_angle(settings)
        
    return settings