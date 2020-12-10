from subprocess import run
import time
while True:
    run(["/home/user/Dynamic_DNS/Get_ip.py"])
    time.sleep(300)