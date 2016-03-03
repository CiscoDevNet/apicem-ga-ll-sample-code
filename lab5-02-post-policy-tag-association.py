from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}

############# Prepare network device list #############
url = "https://"+apicem_ip+"/api/"+version+"/network-device"    # API base url
device = []
try:
    resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
    status = resp.status_code
    print("status: ",status)
    response_json = resp.json() # Get the json-encoded content from response
    device = response_json["response"] # network-device
except:
    print ("Something wrong, cannot get network device information")
    sys.exit()  
    
if status != 200:
    print ("Response status %s,Something wrong !"%status)
    print (resp.text)
    sys.exit()

if device == []:
    print ("Oops! No device was found ! Discover network device first.")
    sys.exit()
    
############# select a device for taging #############   
device_list = []
device_show_list = []
# Extracting attributes
idx = 0
for item in device:
    idx = idx +1
    device_list.append([item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
    #Not showing id to user, it's just a hex string
    device_show_list.append([idx,item["hostname"],item["managementIpAddress"],item["type"]])
    # Show all network devices under this APIC-EM's management
    # Pretty print tabular data, needs 'tabulate' module
print (tabulate(device_show_list, headers=['Number','hostname','ip','type'],tablefmt="rst"),'\n')

# Ask user's selection
    
select = True
id = ""
# Ask user's input 
# Find out network device id for network device with ip or hostname, index 3 is device id
# In the loop until 'id' is assigned or user select 'exit'

while select:
    user_input = input('=> Enter number on the list for policy tag: ')
    user_input= user_input.replace(" ","") # ignore space
    if user_input.lower() == 'exit': 
        sys.exit()
    if user_input == "" or int(user_input) < 1 or int(user_input) > idx:
        print ("Oops! number out of range, please try again or enter 'exit'")
    else:
        id = device_list[int(user_input)-1][3]
        break
     # End of while loop
else:
    print ("Oops! No device was found ! Discover network device first.")
    sys.exit() 

    
######## select a policy tag to associate with device ##########

url = "https://"+apicem_ip+"/api/"+version+"/policy/tag" # policy tag url
resp = requests.get(url,headers=headers,verify=False)
response_json = resp.json()
tag = response_json["response"] # policy tags
if tag ==[] :
    print ("No policy tag was found, create policy tag first !")
    sys.exit()
    
print ("Policy Tag:")
print ("----------------------------")
i = 0
for item in tag:
    i=i+1
    print (i,"-",item["policyTag"])
select = True
# Ask user's input 
# In the loop until tag is selected or user select 'exit'
while select:
    tag_num = input('=> Enter a number above for policy tag: ')
    tag_num = tag_num.replace(" ","") # ignore space

    if tag_num.lower() == 'exit': 
        sys.exit()           
    if tag_num == "" or int(tag_num) < 1 or int(tag_num) > i:
        print ("Oops! number out of range, please try again or enter 'exit'")
    else:
        break
    
    # End of while loop

#JSON for POST /policy/tag/association 
r_json = {
    "policyTag":tag[int(tag_num)-1]["policyTag"],
    "networkDevices":[{"deviceId":(id)}]
}

# post API
post_url = "https://"+apicem_ip+"/api/"+version+"/policy/tag/association" 
resp = requests.post(post_url, json.dumps(r_json), headers=headers,verify=False)
status = resp.status_code
print("status: ",status)
print ("Response:",json.dumps(resp.json(),indent=4))
