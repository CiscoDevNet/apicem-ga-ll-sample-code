from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get token - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}

# Prepare network device list
url = "https://"+apicem_ip+"/api/v1/network-device"   # API base url
resp= requests.get(url,headers=headers,verify = False)     # The response (result) from "GET /network-device" query
response_json = resp.json() # Get the json-encoded content from response with "response_json = resp.json()
device = response_json["response"]    # network-device


# Make sure there is at least one network device
if device != [] :   # if response is not empty 
    # Show what devices under this APIC-EM's management
    device_list = []
    device_show_list = []
    for item in device:
        device_list.append([item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
        device_show_list.append([item["hostname"],item["managementIpAddress"],item["type"]])
        
    #Pretty print tabular data, needs tabulate module
    print (tabulate(device_show_list, headers=['hostname','ip','type'],tablefmt="rst"),'\n')
    # Ask user input
    print ("*** Please note that some devices may not be able to show configuration due to various reason. ***\n")
    user_input = input('=> Please enter a device ip or device host name(case-sensitive) from above to show IOS config: ')
    user_input= user_input.replace(" ","")
    # find out network device id for network device with ip or hostname
    # index 0 is the hostname, index 1 is the IP and index 3 is device id
    id = ""
    for item in device_list:
        if item[0] == user_input or item[1] == user_input:
            id = item[3]
            break
    # get IOS configuration
    if id !="":
        url =  "https://"+apicem_ip+"/api/v1/network-device/"+id+"/config"
        resp = requests.get(url,headers=headers,verify = False)
        status = resp.status_code
        print("status: ",status)
        try:
            response_json = resp.json()
            # replace "\r\n" to "\n" to remove extra space line (Carriage Return)
            print (response_json["response"].replace("\r\n","\n"))
        except:
            if status == 204:
                print ("No Content")
            else:
                print ("Something wrong !")
    else:
        print ("Oops! host name or ip not found !")
else:
    print ("No network device found !")
    
