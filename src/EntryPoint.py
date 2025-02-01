import time
import Main

time_to_process_in_sec = 1 * 60

while(True):
    time_before = time.time()
    Main.mainFunction()
    time_after = time.time()
    
    duration_in_sec = time_after - time_before
    time.sleep(time_to_process_in_sec - time_after)