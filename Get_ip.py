import requests

import json
from requests import get
import os

api_ip = get("https://api.ipify.org").text

try:
    with open('ip.json','r') as Readfile:
        json_ip_check = json.load(Readfile)
except:
    exit()




ip = {
    "New_ip": api_ip
    
}

ip_current = json_ip_check['Current_ip']

if (ip_current == ip["New_ip"] ):
    print("Ip has not changed")
    exit()

else:
    ip = {
        "New_ip": api_ip,
        "Current_ip": api_ip,
        "Old_ip": ip_current
    }
    json_ip = json.dumps(ip, indent = 4) 

    with open(os.getcwd()+"/ip.json", "w") as outfile: 
        outfile.write(json_ip) 
        outfile.close()
        print("Ip updated to:",api_ip)