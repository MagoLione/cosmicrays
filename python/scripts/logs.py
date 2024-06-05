import os
import pytz
import threading
import textwrap

from datetime import datetime

from scripts import paths

# A class usefull to classificate errors by gravity level.
class Level():
    L = 1
    M = 2
    H = 3
    WTF = 0
    
    # Getting a string that represent the gravity level.
    def getString(level: int):
        plus = "+"
        
        if level >= Level.L and level <= Level.H:
            string = plus*level
        elif level == Level.WTF:
            string = "WTF"
            
        return f"Level:{string}"
    
    # Gettings error prefix.
    def getPrefix(level: int):
        if level == Level.WTF:
            return "WTF ERROR:"
        else:
            return "ERROR:"

# A function to print an error in console and to store it in a log file.
def log(
    e: str, 
    flag: str, 
    level: int, 
    short: str = "An error occurred, see more in logs."
    ):
    # Printing error string in console.
    print(f"{Level.getPrefix(level)} {short} {Level.getString(level)} [{flag}]")
    
    # Preparing error string.
    error = f"{Level.getPrefix(level)} {Level.getString(level)}\n {textwrap.dedent(e)}"
    
    # Writing error in a log file.
    threading.Thread(target=create_log, args=[error, flag]).start()

# A function to create a new log file and write it.
def create_log(e, flag: str):
    file_name = get_log_name(flag)
    
    file_path = os.path.join(paths.logs_folder,file_name)
    
    with open(file_path, "a") as file:
        file.write(e+"\n")

# A function to get the log file name.
def get_log_name(flag):
    date = datetime.now(pytz.utc)
    microsecond = date.microsecond

    centisecond = str(microsecond // 10000).zfill(2)

    formatted_date = date.strftime("%Y%m%d_%H%M%S") + f"{centisecond}_{flag}.txt"
    return formatted_date