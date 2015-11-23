from apicem_config import * # apicem_config.py is the central place to change the apic-em IP, username, password ...etc

# Get token - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}
url = "https://"+apicem_ip+"/api/v1/host"   # API base url

try:
    resp= requests.get(url,headers=headers,verify = False)
    response_json = resp.json() # Get the json-encoded content from response
    print ("Status: ",resp.status_code)  # This is the http request status
    print (json.dumps(response_json,indent=4)) # Convert "response_json" object to a JSON formatted string and print it out    
except:
    print ("Something wrong !")

# Now create a list of host IP address
host_ip_list=[]
for item in response_json["response"]:
    host_ip_list.append(item["hostIp"])

print ("\nThis is the list of host ip:\n",host_ip_list)

    

