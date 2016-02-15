'''
This file is independent, not associated with apicem_config.py
'''

import requests   # We use Python "requests" module to do HTTP GET query
import json       # Import JSON encoder and decode module
requests.packages.urllib3.disable_warnings() # Disable warnings

# APIC-EM IP
apicem_ip = "sandboxapic.cisco.com:9443"

username = "admin"
password = "C!sc0123"
version = "v1"

# JSON input
r_json = {
    "username": username,
    "password": password
}

# API URL
post_url = "https://"+apicem_ip+"/api/"+version+"/ticket"

# All APIC-EM REST API request and response content type is JSON.
headers = {'content-type': 'application/json'}

# make request and get response - "resp" is the response of this request
resp = requests.post(post_url, json.dumps(r_json), headers=headers,verify=False)
print ("Request Status: ",resp.status_code)

# Get the json-encoded content from response
response_json = resp.json() 
print ("Response:",json.dumps(response_json,indent=4))
