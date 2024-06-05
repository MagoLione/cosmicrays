from scripts.logs import log, Level

from scripts.MyDrive import MyDrive
from scripts.Track import Track

from scripts.dates import from_date_to_string

from scripts.local_reader import is_there_the_correct_file
from scripts.local_writer import write_csv, delete_useless_files

from scripts.drive_uploader import upload_file
from scripts.drive_reader import searching_for_todays_file_id
from scripts.drive_downloader import download_file

# Multiple objects coordinator function.        
def start_multiple_objects_coordinator(track: Track):
    error_flag = "coortinator"
    
    service = MyDrive().service # Getting drive service.
    
    while track.to_do_list: # While to_do_list isn't empty.
        crs = track.to_do_list # Getting a static to_do_list list.
        
        while crs: # While crs isn't empty.
            date = None
            date_s = None
            
            items = []
            
            index1 = 0
            index2 = 0
            
            for cr in crs:
                track.count += 1
                
                index1 += 1
                
                string = from_date_to_string(cr.date, "d") # Format the date to a string.
                if date == None:
                    
                    index2 += 1
                    
                    date = cr.date # Updating date with the cr's date.
                    date_s = string # Updating date_s with the formatted cr's date.
                    items.append(cr) # Adding cr to items list.
                    continue # Goes to the next for iteration.
                
                if string == date_s: # If the formatted date is equal to the saved one.
                    index2 += 1
                    items.append(cr) # Adding cr to items list.
                            
            if index1 != index2:
                log(
                    e = f"""
                    An error occurred during measurement coordination: 
                                        
                    Measurements of some cosmic rays may be lost.
                    If this error occurs from one day to the next, this may not be a real problem.
                    
                    Measurements: {index1}, May be not handled: {index1-index2}
                    """,
                    flag=error_flag,
                    level=Level.L
                )
            
            index3 = 0
            
            # Removing already measured CosmicRays from items list.
            for i in items:
                index3 += 1
                crs.remove(i)
                
            if index2 > index3:
                log(
                    e=f"""
                    An error occurred during measurement coordination:
                                        
                    Some measurements were recorded multiple times.
                    
                    Multiplied measurements: {index2-index3}
                    
                    """,
                    flag=error_flag,
                    level=Level.M
                )
            elif index2 < index3:
                log(
                    e=f"""
                    An error occurred during measurement coordination:
                    
                    I don't know how this error is possible.
                    Some measurements were lost.
                    
                    Lost measurements: {index3-index2}
                    
                    """,
                    flag=error_flag,
                    level=Level.WTF
                )

            
            if not is_there_the_correct_file(date):
                delete_useless_files(date) # Deleting useless files (like an old csv).
                day_id, _, _, _ = searching_for_todays_file_id(service, date) # Getting today's file name or None.
                if day_id: # If isn't None.
                    download_file(service, day_id) # Downloading the file.
                
            for i in items: # For each CosmicRay measured.
                write_csv(i) # Writing CosmicRay data in csv.
            upload_file(service, date) # Uploading the file.
                
        # Removing already measured CosmicRays from crs list.
        for cr in crs:
            track.to_do_list.remove(cr)