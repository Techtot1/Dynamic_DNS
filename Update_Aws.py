import route53
import json
import os


with open(os.getcwd()+"/ip.json") as Readfile:
    json_ip_check = json.load(Readfile)

with open(os.getcwd()+"/Config.json") as ConfigFile:
    Config = json.load(ConfigFile)

ip_current = json_ip_check['New_ip']

conn = route53.connect(
    aws_access_key_id=Config["aws_access_key"],
    aws_secret_access_key=Config["aws_secret_access_key"],
)

zone = conn.get_hosted_zone_by_id(Config["hosted_zone_ID"])


# Note that this is a fully-qualified domain name.

for record_set in zone.record_sets:
    print(record_set)
    
    if record_set.name == Config["record_name"]:
        record_set.delete()   
        
        # Stopping early may save some additional HTTP requests,         record_set.values  = ['24.150.174.242']
        # since zone.record_sets is a generator.
        break
#print(to_change)


new_record, change_info = zone.create_a_record(
    # Notice that this is a full-qualified name.
    name=Config["record_name"],
    # A list of IP address entries, in the case fo an A record.
    values=[ip_current],
)