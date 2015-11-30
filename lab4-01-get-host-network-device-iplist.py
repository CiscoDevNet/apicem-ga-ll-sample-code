from apicem_config import * # apicem_config.py is the central place to change the apic-em IP, username, password ...etc

# Get token - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}
host_ip_list=[]
device_ip_list=[]

# Create a list of host IP address
url = "https://"+apicem_ip+"/api/v1/host"   # API base url
# Create a list of host IP address
try:
    resp= requests.get(url,headers=headers,verify = False)
    print ("Status of GET /host: ",resp.status_code)  # This is the http request status
    response_json = resp.json() # Get the json-encoded content from response
    for item in response_json["response"]: # form host ip list
        host_ip_list.append(item["hostIp"])
except:
    print ("Something wrong, cannot get host IP list !")

# Create a list of network-device IP address
url = "https://"+apicem_ip+"/api/v1/network-device"
try:
    resp= requests.get(url,headers=headers,verify = False)
    print ("Status: of GET /network-device ",resp.status_code)  # This is the http request status 
    response_json = resp.json() # Get the json-encoded content from response
    for item in response_json["response"]: # form network device ip list
        device_ip_list.append(item["managementIpAddress"])
except:
    print ("Something wrong, cannot get network-device IP list !")

print ("---------- host ip ----------")
if host_ip_list== [] :   # if response is not empty
    print ("      There is no host")
else:
    for item in host_ip_list:
        print ('\t',item)
print ("----- network-device ip -----")
if device_ip_list == [] :   # if response is not empty
    print ("      There is no network-device")
else:
    for item in device_ip_list:
       print ('\t',item)
print ("-----------------------------")
    
