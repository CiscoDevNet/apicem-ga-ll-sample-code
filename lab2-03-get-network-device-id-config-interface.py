from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}

# Prepare network device list
url = "https://"+apicem_ip+"/api/v1/network-device"    # API base url
resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
response_json = resp.json() # Get the json-encoded content from response 
device = response_json["response"] # network-device

# **** Please note that some device may not be able to show information due to various reason. ****
    
# Make sure there is at least one network device
if device != [] :   # if response is not empty
    # Ask user's input - What to display ? Interfaces list(1) or IOS config(2) ?
    select = True
    while select:
        user_input = input('=> Please enter \n1: To get list of interfaces for the given device ID\n2: To get IOS configuration for the given device ID\nEnter your selection: ' )
        user_input= user_input.replace(" ","")
        if user_input.lower() == 'exit': 
            sys.exit()     
        if user_input == '1' or user_input == '2':
            select = False
        else:
            print ("Sorry, wrong selection, please try again to select 1 or 2 or enter 'exit'!")
    # End of while loop
    
    device_list = []
    device_show_list = []
    # Extracting attributes
    for item in device:
        device_list.append([item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
        # Not showing id to user, it's just a hex string
        device_show_list.append([item["hostname"],item["managementIpAddress"],item["type"]])
    # Show all network devices under this APIC-EM's management      
    # Pretty print tabular data, needs tabulate module
    print (tabulate(device_show_list, headers=['hostname','ip','type'],tablefmt="rst"),'\n')
    print ("\n*** Please note that some devices may not be able to show information. ****")
 
    # Ask user's input 
    # Find out network device id for network device with ip or hostname, index 3 is device id
    # In the loop until 'id' is assigned or user select 'exit'
    id = ""
    select = True
    while select:
        if user_input == '1':
            user_input1 = input('=> Enter a device ip or host name(case-sensitive) from above to show Interface:')
        else :
            user_input1 = input('=> Enter a device ip or host name(case-sensitive) from above to show IOS config:')
        user_input1 = user_input1.replace(" ","") # ignore space
        if user_input1.lower() == 'exit': 
            sys.exit()           
        for item in device_list:
            if user_input1 in item: # if user_input is matched
                id = item[3]
                select = False
                break
        if id == "":
            print ("Oops! host name or ip not found, please try again or enter 'exit'")
    # End of while loop
    
    if user_input == '1':
        # get interface list
        url  =  "https://"+apicem_ip+"/api/v1/interface/network-device/"+id
    else:
        # get IOS configuration
        url =  "https://"+apicem_ip+"/api/v1/network-device/"+id+"/config"
    resp = requests.get(url,headers=headers,verify = False)
    status = resp.status_code
    print("status: ",status)
    try:
        response_json = resp.json()
        if user_input == '1': # interface list
            print ("Response:\n",json.dumps(response_json,indent = 4))
        if user_input == '2': # IOS configuration
            # replace "\r\n" to "\n" to remove extra space line (Carriage Return)
            print (response_json["response"].replace("\r\n","\n"))
    except:
        if status == 204:
            print ("No Content")
        else:
            print ("Something wrong !\n")
            print ("Response:\n",json.dumps(response_json,indent = 4))
else:
    print ("No network device found !")
    
