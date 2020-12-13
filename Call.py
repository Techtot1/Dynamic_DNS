from subprocess import run
import time
while True:
    run(["./Get_ip.py"])
#Set how often you would like The script to run 
# Default is 5 minutes but because A free IP check api is in use
# you could run this every second for free.   
    time.sleep(300)
        #Time in seconds