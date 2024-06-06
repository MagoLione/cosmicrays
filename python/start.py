import os
import threading
import time
import serial
import pytz

from datetime import datetime
from serial import SerialException

from scripts import paths

from scripts.logs import log, Level
from scripts.CosmicRay import CosmicRay
from scripts.Track import Track

from scripts.local_reader import read_settings
from scripts.local_writer import reset_settings
from scripts.coordinator import start_multiple_objects_coordinator

"""
Main Function
"""

def start():
    # Initializing Track object (used to track operations).
    track = Track()
    
    """
    Serial Communication
    """
    try:
        # Setting serial communication for the reciver.
        ser_reciver = serial.Serial(
            port='COM4',
            baudrate=19200,
        )
        
        # Setting serial communication for the servo motor.
        ser_servo = serial.Serial(
            port='COM5',
            baudrate=19200,
        )
    except (PermissionError) as e:
        log(
            e=f"""
            An error occurred establishing the serial connection.
            
            Permission error:
            {e}
            """,
            flag="serialcom",
            level=Level.H
        )
        return
    except (SerialException) as ex:
        log(
            e=f"""
            An error occurred establishing the serial connection.
            
            Serial exception:
            {ex}
            """,
            flag="serialcom",
            level=Level.H
        )
        return
    
    """
    Servo Functions
    """
    
    # A function to update servo to the last data.
    def update_servo():
        
        # Writing in serial (adjusting the servo angle (from 0 to 180) adding 1. Arduino's program support numbers from 1 to 181).
        ser_servo.write(f"{track.servo_angle+1}\n".encode())
        
    # A function to read servo feedback.
    def read_servo():
        start_time = time.time()
        data = None
        
        print("Wait...")
        
        # Waiting servo feedback for 2 seconds.
        while time.time() - start_time < 2:
            
            line = ser_servo.readline() # Reading servo data.
            data = line.decode() # Deconding it.
            
            # The \r\n characters are added by default from arduino, so we have to specify it.
            if data == "0\r\n":
                # The servo was already positioned in the selected angle.
                print("Already positioned.")
                return
            elif data == "1\r\n":
                # The servo was successfully moved.
                print("Done.")
                return
        
        # Once the wait is over, so was impossible to read servo feedback, logging an error.
        log(
            e="""
            An error occurred reading servo response:
            
            It was impossible to read servo response.
            """,
            flag="readservo",
            level=Level.H
        )
        
    """
    Reciver Functions
    """
        
    # A function to read reciver's serial communication.
    def read_serial():
        while track.active or not track.automode: # Verifing the active state when automode is enabled.
            line = ser_reciver.readline() # Reading reciver data.
            data = line.decode() # Decoding it.
            
            if data == "0\r\n": # If the data is 0, the value the reciver communicate when recives a CosmicRay (padded by \r\n, Arduino's default characters).
                threading.Thread(target=safe_run, daemon=False).start() # Starting safe_run in a new thread (so it runs without blocking the main one)
                
    """
    Others Functions
    """
    # A function to ad a new CosmicRay in the to_do_list list and to start safely the saving process.
    def safe_run():
        if track.active or not track.automode: # Verifing the active state when automode is enabled.
            now = datetime.now(pytz.utc)
            cr = CosmicRay(now, track.servo_angle, track.description) # Creating a CosmicRay object using the current time and the settings saved in the track.
            
            track.to_do_list.append(cr) # Adding the CosmicRay to the to_do_list list.
            
            if not track.is_running: # If saving process is not running.
                track.is_running = True # Turning is_running True.
                
                threading.Thread(target=run, daemon=False).start() # Starting run in a new thread.
    
    # A function to start the saving process.
    def run():
        
        while track.to_do_list: # While the list isn't empty.
                            
            start_multiple_objects_coordinator(track) # Starting the multiple objects coordinator and passing track as an argument.
            
        track.is_running = False # When to_do_list list is empty, turning is_running False.
        
    # AutoMode Function
    def auto_mode():
        
        old_settings = track.getSettings() # Saving the current settings.
        
        print("\n[AUTO MODE ENABLED]")
        print("Press enter to quit Auto Mode.", end="\n\n")
            
        while track.automode: # While AutoMode is enabled.
            
            settings = read_settings() # Reading settings file.
            
            on_finish = []
            
            if settings.angle != track.servo_angle: # If the readed angle and the saved one are different.
                on_finish.append(update_servo) # Adding update_servo to on_finish list.
                
            if settings.active and track.active == False: # If the readed active state is True and the saved one is False.
                on_finish.append(threading.Thread(target=read_serial, daemon=False).start) # Adding the starter for a read_serial's new thread to the on_finish list.
                
            track.synchronize(settings) # Updating track with the readed settings.
            
            # Running all the functions in on_finish list.
            for fun in on_finish:
                fun()
            
        # When AutoMode is False.
        reset_settings() # Resetting the settings.
        print(f"\nBack to the old settings...\n{track.synchronize(old_settings)}") # Updating track with the old saved settings.
        
        print("\n[AUTO MODE DISABLED]")
        print("Press enter to quit, the angle you want, \"d\" to set a description or \"a\" to enable Auto Mode.") 
            
    """
    PROGRAM START
    """
    
    update_servo() # Updating servo.
                
    threading.Thread(target=read_serial, daemon=False).start() # Starting reading serial communications.
    
    print("Press enter to quit, the angle you want, \"d\" to set a description or \"a\" to enable Auto Mode.")
    while True:
        obj = input() # Reading user's input.

        if obj == "": # If was pressed enter.
            track.active = False # Turning active state False.
            print("Ending...")
            break # Exiting the while.
        
        elif obj.startswith("-"): # Else, if what was entered starts with -.
            print("The value must be between 0 and 180.")
        
        elif obj.isdigit(): # Else, if was entered a number (without symbol like -, + etc).
            obj_int = int(obj) # From string to int.
            if obj_int <= 180: # If it's minor or equal to 180.
                track.servo_angle = obj_int # Updating servo_angle.
                update_servo() # Updating servo.
                read_servo() # Reading servo feedback.
            else:
                print("The value must be between 0 and 180.")
                
        elif obj == "d": # Else, if was entered d.
            print("Insert the description (if you whant to clear the descripion press enter):")
            des_obj = input() # Reading the new description.
            
            # Updating it.
            if des_obj == "":
                track.description = None
            else:
                track.description = des_obj
                
            print("Done.\n")
            
        elif obj == "a": # Else, if was entered a.
            
            track.automode = True # Turting AutoMode True.
            
            threading.Thread(target=auto_mode, daemon=False).start() # Starting auto_mode in a new thread.
            
            input() # Getting user's input.
                    
            track.automode = False # Turning AutoMode False.
                
        else:
            print("Insert a valid value.")
            
    threads_count = 0
    while threading.active_count() > 1: # If are active more than 1 threads.
        if threads_count != threading.active_count(): # If saved threads count is different from the real one.
            threads_count = threading.active_count() # Updatine threads_count.
            
            l: str = "" # A string to list all the active threads.
            
            i = True # A variable to track if is the first iteration.
            
            for p in threading.enumerate(): # For p in the list of active threads.

                if p.name != "MainThread": # Excluding the MainThread thread.
                    if i: # If is the first iteration.
                        i = False
                    else: # Else.
                        l += ", "
                    l += p.name # Adding this process' name to l.
                        
            
            print(f"\nLeft {threads_count-1} processes to end:")
            print(l)
        
        time.sleep(1)
        
    print("END")

if __name__ == "__main__":
    if not os.path.isdir(paths.data_folder) or not os.path.isdir(paths.settings_folder) or not os.path.isdir(paths.logs_folder):
        print("Paths are not correctly setted. Use set_default_paths.py file to set the default paths or check /scripts/paths.py file.")
    
    start()
