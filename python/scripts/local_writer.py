import os
import time
import json

from scripts import paths

from datetime import datetime

from CosmicRay import CosmicRay
from scripts.logs import log, Level
from scripts.dates import get_todays_file_name, from_date_to_string
from scripts.Track import Settings

error_flag = "localwriter"

index1 = 0
index2 = 0

def write_binary_file(file_name: str, data: bytes):
    with open(file_name, "wb") as f:
        f.write(data)

# Deletes useless files in local data folder, like old CSVs.
def delete_useless_files(date: datetime):
    
    day_name = get_todays_file_name(date) # Getting name of the only usefull file.
    
    for file in os.listdir(paths.data_folder): # For each file in local folder.
        if file != f"{day_name}.csv": # If is named different.
            os.remove(os.path.join(paths.data_folder, file)) # Removing file.
            
# Append CosmicRay's data to the csv.
def write_csv(cr: CosmicRay):
    global index1
    global index2
    
    index1 += 1
        
    file = f"{get_todays_file_name(cr.date)}.csv" # Getting file name.
    file_path = os.path.join(paths.data_folder, file) # Getting file path.
    
    formatted_date = from_date_to_string(cr.date, "D") # Getting fully formatted date.
    
    with open(file_path, "a") as f: # Opening file in append mode.
        f.write(f"{formatted_date},{cr.angle},{cr.description}\n") # Writing the file.
        
    index2 += 1
    
    if index1 > index2:        
        log(
            e=f"""
            An error occurred while writing measurements to the file:
            
            Some measurements were lost.
            If it repeats, check if other programs are using the file.
            
            Total number of missed measurements' estimate: {index1-index2}
            
            """,
            flag=error_flag,
            level=Level.H
        )
    elif index1 < index2:
        log(
            e=f"""
            An error occurred while writing measurements to the file:
            
            Some measurements were write multiple times.
            It hasn't explanation.
            
            Total number of multipled measurements' estimate: {index2-index1}
            
            """,
            flag=error_flag,
            level=Level.WTF
        )

# Initialize settings files.
def initialize_settings() -> Settings:
    print("Initializing settings...")
    
    enabled = True
        
    while True:
        try:
            with open(os.path.join(paths.settings_folder, paths.automode_file), "w") as a_f: # Opening automode file in writing mode.
        
                a_data = {'enabled': enabled}
                
                a_f.write(json.dumps(a_data, indent=4)) # Writing data in json format.
                
            break
        except (OSError) as e:
            log(
                e=f"""
                An error occurred initializing automode.json file:
                
                Check file's users.
                
                {e}
                """,
                flag=error_flag,
                level=Level.M
            )
            
            time.sleep(0.2)
    
    active = True
    angle = 0
    description = None
        
    while True:
        try:
            with open(os.path.join(paths.settings_folder, paths.settings_file), "w") as f: # Opening settings file in writing mode.
        
                data = {'active': active, 'angle': angle, 'description': description}
                
                f.write(json.dumps(data, indent=4)) # Writing data in json format.
                
            break
        except (OSError) as e:
            log(
                e=f"""
                An error occurred initializing settings.json file:
                
                Check file's users.
                
                {e}
                """,
                flag=error_flag,
                level=Level.M
            )
            
            time.sleep(0.2)
    
        
    print("Done.")
        
    return Settings(active, angle, description) # Returning a Settings object.

# Resets settings.
def reset_settings():
    print("Resetting settings...")
    
    enabled = False
    
    with open(os.path.join(paths.settings_folder, paths.automode_file), "w") as a_f: # Opening automode file in writing mode.
        
        a_data = {'enabled': enabled}
        
        a_f.write(json.dumps(a_data, indent=4)) # Writing data in json format.
    
    active = None
    angle = None
    description = None
    
    with open(os.path.join(paths.settings_folder, paths.settings_file), "w") as f: # Opening settings file in writing mode.
        
        data = {'active': active, 'angle': angle, 'description': description}
        
        f.write(json.dumps(data, indent=4)) # Writing data in json format.
        
    print("Done.")
    
# Reinitialize the active setting.
def reinitialize_active(settings: Settings) -> Settings:
    print("Reinitializing active...")
    
    with open(os.path.join(paths.settings_folder, paths.settings_file), "w") as f: # Opening file in writing mode.
        
        data = {'active': True, 'angle': settings.angle, 'description': settings.description}
        
        f.write(json.dumps(data, indent=4)) # Writing data in json format.
        
    settings.angle = 0
    
    print("Active is set to True.")
    
    return settings
    
# Reinitialize the angle setting.
def reinitialize_angle(settings: Settings) -> Settings:
    print("Reinitializing angle...")
    with open(os.path.join(paths.settings_folder, paths.settings_file), "w") as f: # Opening file in writing mode.
        
        data = {'active': settings.active, 'angle': 0, 'description': settings.description}
        
        f.write(json.dumps(data, indent=4)) # Writing data in json format.
        
    settings.angle = 0
    
    print("Angle is set to 0.")
    
    return settings