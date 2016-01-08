from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}

# Prepare network device list
url = "https://"+apicem_ip+"/api/"+version+"/network-device"     # API base url
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

# Make sure there is at least one network device
if device != [] :   # if response is not empty 
    device_list = []
    device_show_list = []
    # Extracting attributes
    for item in device:
        device_list.append([item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
        #Not showing id to user, it's just a hex string
        device_show_list.append([item["hostname"],item["managementIpAddress"],item["type"]])
    # Show all network devices under this APIC-EM's management
    # Pretty print tabular data, needs 'tabulate' module
    print (tabulate(device_show_list, headers=['hostname','ip','type'],tablefmt="rst"),'\n')
    # Ask user input
    print ("*** Please note that some devices may not be able to show configuration due to various reason. ***\n")
   
    select = True
    id = ""
    # Ask user's input 
    # Find out network device id for network device with ip or hostname, index 3 is device id
    # In the loop until 'id' is assigned or user select 'exit'
    while select:
        user_input = input('=> Enter a device ip or host name(case-sensitive) from above to show IOS config:')
        user_input= user_input.replace(" ","") # ignore space
        if user_input.lower() == 'exit': 
            sys.exit()           
        for item in device_list:
            if user_input in item: # if user_input is matched
                id = item[3]
                select = False
                break
        if id == "":
            print ("Oops! host name or ip not found, please try again or enter 'exit'")
    # End of while loop
            
    # get IOS configuration API
    url =  "https://"+apicem_ip+"/api/v1/network-device/"+id+"/config"
    resp = requests.get(url,headers=headers,verify = False)
    status = resp.status_code
    print("status: ",status)
    try:
        response_json = resp.json()
        # replace "\r\n" to "\n" to remove extra space line (Carriage Return)
        print (response_json["response"].replace("\r\n","\n"))
    except:
    # for some reason IOS configuration is not returned
        if status == 204:
            print ("No Content")
        else:
            print ("Something wrong !\n")
            print ("Response:\n",json.dumps(response_json,indent = 4))
else:
    print ("No network device found !")
    
