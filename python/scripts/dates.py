from datetime import datetime

def get_parent_folders_names(date: datetime):
    month = date.strftime("%m") # Gets month number zero-padded for two numbers.
    year = date.strftime("%Y") # Gets year number.

    return [month, year]

def get_todays_file_name(date: datetime):
    day = date.strftime("%d") # Gets day number zero-padded for two numbers.
    
    return day

def from_date_to_string(date: datetime, type: str):
    if type == "D": # Gets a fully formatted date.
        microsecond = date.microsecond

        centisecond = str(microsecond // 10000).zfill(2) # Getting centiseconds.

        formatted_date = date.strftime("%d/%m/%Y %H:%M:%S") + "." + centisecond
        return formatted_date
    
    elif type == "d": # Gets a formatted date.
        formatted_date = date.strftime("%d/%m/%Y")
        return formatted_date
    
    elif type == "t": # Gets a formatted time.
        microsecond = date.microsecond

        centisecond = str(microsecond // 10000).zfill(2) # Getting centiseconds.

        formatted_date = date.strftime("%H:%M:%S") + "." + centisecond
        return formatted_date
    else:
        None