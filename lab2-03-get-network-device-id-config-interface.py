from apicem_config import * # APIC-EM IP is assigned in apicem_config.py


# Get token - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}

# Prepare network device list
url = "https://"+apicem_ip+"/api/v1/network-device"   # API base url
resp= requests.get(url,headers=headers,verify = False)     # The response (result) from "GET /network-device" query
response_json = resp.json() # Get the json-encoded content from response with "response_json = resp.json()
device = response_json["response"]    # network-device

# **** Please note that some device may not be able to show information due to various reason. ****
    
# Make sure there is at least one network device
if device != [] :   # if response is not empty
    # Ask user's input - What to display ? Interfaces list or IOS config ?
    select = True
    while select:
        user_input = input('=> Please enter \n1: To get list of interfaces for the given device ID\n2: To get IOS configuration for the given device ID\nEnter your selection: ' )
        user_input= user_input.replace(" ","")
        if user_input == '1' or user_input == '2':
            select = False
        else:
            print ('Sorry, wrong selection, please try again to select 1 or 2!')
            
    # Show what devices under this APIC-EM's management 
    device_list = []
    device_show_list = []
    for item in device:
        device_list.append([item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
        device_show_list.append([item["hostname"],item["managementIpAddress"],item["type"]])
      
    #Pretty print tabular data, needs tabulate module
    print (tabulate(device_show_list, headers=['hostname','ip','type'],tablefmt="rst"),'\n')

    print ("\n*** Please note that some devices may not be able to show information. ****")
 
    # Ask user's input - Which network-device to display ?
    user_input1 = input('\n=> Please enter a device ip address or device host name(case-sensitive) from above : ')
    user_input1 = user_input1.replace(" ","")
    # find out network device id for network device with ip or hostname
    # index 0 is the hostname, index 1 is the IP and index 3 is device id
    id = ""
    for item in device_list:
        if item[0] == user_input1 or item[1] == user_input1:
            id = item[3]
            break
    if id !="": 
        if user_input == '1':
             # get interface list
            url  =  "https://"+apicem_ip+"/api/v1/interface/network-device/"+id
        elif user_input == '2':
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
                print ("Response:\n",json.dumps(response_json,indent = 4))
    else:
        print ("Oops! host name or ip not found !")
else:
    print ("No network device found !")
    
