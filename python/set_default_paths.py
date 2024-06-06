import os
import textwrap

def set_default_paths():
    currend_dir = os.getcwd()
    
    data_folder = "data"
    settings_folder = "settings"
    logs_folder = "logs"
    
    paths_file = "scripts\\paths.py"
    
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
    f"""
    data_folder = "{os.path.join(currend_dir, data_folder)}"

    settings_folder = "{os.path.join(currend_dir, settings_folder)}"

    logs_folder = "{os.path.join(currend_dir, logs_folder)}"

    automode_file = "automode.json"
    settings_file = "settings.json"
    """
    )
    
    try:
        with open(os.path.join(currend_dir, paths_file), "w") as f:
            f.write(file_text)
        print("Done.")
            
    except (OSError) as e:
        print("An error occurred setting default paths.")
        print(e)
            
if __name__ == "__main__":
    set_default_paths()