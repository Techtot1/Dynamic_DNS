import requests
import json
from requests import get
import os
import route53

api_ip = get("https://api.ipify.org").text

try:
    with open('ip.json','r') as Readfile:
        json_ip_check = json.load(Readfile)
except:
    exit()




#AWS Route53 Record updater
with open(os.getcwd()+"/Config.json") as ConfigFile:
    Config = json.load(ConfigFile)
def Update_AWS():




    ip_current = json_ip_check['New_ip']
    conn = route53.connect(
        aws_access_key_id=Config["aws_access_key"],
        aws_secret_access_key=Config["aws_secret_access_key"],
    )

    zone = conn.get_hosted_zone_by_id(Config["hosted_zone_ID"])




    for record_set in zone.record_sets:
        print(record_set)
    
        if record_set.name == Config["record_name"]:
            record_set.delete()   
            break



    new_record, change_info = zone.create_a_record(
        name=Config["record_name"],
        values=[ip_current],
)





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
 
    Update_AWS()

       
  