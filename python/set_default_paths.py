import os
import textwrap

def set_default_paths():
    currend_dir = os.getcwd()
    
    data_folder = "/data"
    settings_folder = "/settings"
    logs_folder = "/logs"
    
    paths_file = "/scripts/paths.py"
    
    data_path = os.path.join(currend_dir, data_folder)
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
        
    settings_path = os.path.join(currend_dir, settings_folder)
    if not os.path.isdir(settings_path):
        os.mkdir(settings_path)
        
    logs_path = os.path.join(currend_dir, logs_folder)
    if not os.path.isdir(logs_path):
        os.mkdir(logs_path)
    
    file_text = textwrap.dedent(
    """
    data_folder = "YOUR-DATA-FOLDER"

    settings_folder = "YOUR-SETTINGS-FOLDER"

    logs_folder = "YOUR-LOGS-FOLDER"

    automode_file = "automode.json"
    settings_file = "settings.json"
    """
    )
    
    while True:
        try:
            with open(os.path.join(currend_dir, paths_file), "w") as f:
                f.write(file_text)
            
            break
                
        except (OSError) as e:
            print("An error occurred setting default paths.")
            print(e)