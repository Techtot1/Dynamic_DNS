#!/usr/bin/python3
import requests
import json
from requests import get
import os
import route53
from datetime import datetime
import time

#Gets your current WAN-IP 
#Ipify is a free to use API without rate limits and no account/credentials needed

try:
    api_ip = get("https://api.ipify.org").text
except:
    print("No Connection.")
    exit()
#Opens the ip json file as read for checks la
# ter
try:
    with open('ip.json', 'r') as Readfile:
            json_ip_check = json.load(Readfile)
except:
    exit()

#Initializes the current IP variable
ip_current = ""

#Opens your config file with Credentials for use Later
with open(os.getcwd()+"/Config.json") as ConfigFile:
    Config = json.load(ConfigFile)


def Update_AWS():
    #Sets your AWS credentials for connection.
    conn = route53.connect(
        aws_access_key_id=Config["aws_access_key"],
        aws_secret_access_key=Config["aws_secret_access_key"],
                            )
    #Connects to your hosted zone.
    zone = conn.get_hosted_zone_by_id(Config["hosted_zone_ID"])

    #Filters through the records in your hosted zone. 
    #The Route53 API doesn't offer an elegant way of filtering records so this is it.
    for record_set in zone.record_sets:
        print(record_set)

        #When the your record is found it get deleted 
        #And is then recreated down the line.
        if record_set.name == Config["record_name"]:
            record_set.delete()
            break
    #Your record is created with updated IP
    new_record, change_info = zone.create_a_record(
        name=Config["record_name"],
        values=[api_ip]
    )

#Set's the new Ip that was set by the ipify.org API
ip = {
    "New_ip": api_ip

    }
#Sets the Current IP for Checks later
ip_current = json_ip_check['Current_ip']

#Checks if the WAN-IP has changed
if (ip_current == ip["New_ip"]):
    print("Ip has not changed; Ip was last changed "+json_ip_check["Last_Change"])

#if the Ip has changed 
else:
    #Set's all the Values required for the ip.json file
    ip = {
        "New_ip": api_ip,
        "Current_ip": api_ip,
        "Old_ip": ip_current
        "Last_Change": datetime.now().strftime("%H:%M:%S  %d:%m:%Y")
    }
    json_ip = json.dumps(ip, indent=4)

    with open(os.getcwd()+"/ip.json", "w") as outfile:
        outfile.write(json_ip)
        outfile.close()
        print("Ip updated to:", api_ip)
    ip_current = api_ip
        
    Update_AWS()
