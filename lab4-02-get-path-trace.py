from apicem_config import * # apicem_config.py is the central place to change the apic-em IP, username, password ...etc
import time # Need it for delay - sleep() function

# Get token - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}
host_ip_list=[]
device_ip_list=[]

# Create a list of host IP address
url = "https://"+apicem_ip+"/api/"+version+"/host"   # API base url
# Create a list of host IP address
try:
    resp= requests.get(url,headers=headers,verify = False)
    print ("Status of GET /host: ",resp.status_code)  # This is the http request status
    response_json = resp.json() # Get the json-encoded content from response
    for item in response_json["response"]:
        host_ip_list.append(item["hostIp"])
except:
    print ("Something wrong, cannot get host IP list !")

# Create a list of network-device IP address
url = "https://"+apicem_ip+"/api/"+version+"/network-device"
try:
    resp= requests.get(url,headers=headers,verify = False)
    print ("Status: of GET /network-device ",resp.status_code)  # This is the http request status
    response_json = resp.json() # Get the json-encoded content from response
    for item in response_json["response"]:
        device_ip_list.append(item["managementIpAddress"])
except:
    print ("Something wrong cannot get network-device IP list !")

# print out a IP list for user to select
print ("\n---------- host ip ----------")
if host_ip_list== [] :   # if response is empty
    print ("\n      There is no host")
else:
    for item in host_ip_list:
        print ('\t',item)
print ("----- network-device ip -----")
if device_ip_list == [] :   # if response is empty
    print ("      There is no network-device")
else:
    for item in device_ip_list:
       print ('\t',item)
print ("-----------------------------")

# Don't bother to go further if there is no any host and network device
if host_ip_list== [] and device_ip_list == []:
    print ("There is no any host or network device !!!")
    sys.exit()

print ("*** Please note that not all source/destination ip pair will return a path - no route. ! *** \n")

# Select source ip
select = True
while select:
    s_ip = input('=> Please select a source ip address from above list: ')
    s_ip = s_ip.replace(" ","")
    if s_ip in host_ip_list or s_ip in device_ip_list:
        select = False
    else:
        print ("IP address you entered is NOT on the list !")

# Select destination ip
select = True
while select:
    d_ip = input('=> Please select a destination ip address from above list: ')
    d_ip = d_ip.replace(" ","")
    if d_ip in host_ip_list or d_ip in device_ip_list:
        select = False
    else:
        print ("IP address you entered is NOT on the list !")

# JSON input for POST /flow-analysis
path_data = {"sourceIP": s_ip, "destIP": d_ip}

post_url = "https://"+apicem_ip+"/api/"+version+"/flow-analysis"
r = requests.post(post_url, json.dumps(path_data), headers=headers,verify=False)
response_json = r.json()
print ("\nPOST flow-analysis Status: ",r.status_code)
print ("Response from POST /flow-analysis:\n",json.dumps(response_json,indent=4))

# Check get flow-path task status with taskId
try:
    taskId = response_json["response"]["taskId"]
except:
   print ("\n For some reason cannot get taskId")
   sys.exit()
else:
    url = "https://"+apicem_ip+"/api/"+version+"/task/"+taskId
    r = requests.get(url,headers=headers,verify=False)
    response_json = r.json()
    print ("\nGET task with taskId status: ",r.status_code)
    print ("Response from GET /task/taskId:\n",json.dumps(response_json,indent=4))

# When see the endTime field from response above means that get flow-path task is completed
pathId = ""
while pathId =="":
    try:
        # Can we see endTime ?
        response_json["response"]["endTime"]
    except:
        # No endTime, no pathId yet
        print ("\nTask is not finished yet, sleep 1 second then try again")
        time.sleep(1)
        url = "https://"+apicem_ip+"/api/"+version+"/task/"+taskId
        r = requests.get(url,headers=headers,verify=False)
        response_json = r.json()
        print ("\nGET task with taskId status: ",r.status_code)
        print ("Response from GET /task/taskId:\n",json.dumps(response_json,indent=4))
    else:
        # endTime exist,can get pathId now
        # pathId is the value of "progress" attribute
        if response_json["response"]["isError"] == "true":
            print ("\nSomething not right, here is the response:\n")
            print ("\n*** Response from GET /flow-analysis/pathId.- Trace path information. ***\n",json.dumps(response_json,indent=4))
        else:
            pathId = response_json["response"]["progress"]
            print ("\nPOST flow-analysis task is finished now, here is the pathId: ",pathId)
            url = "https://"+apicem_ip+"/api/"+version+"/flow-analysis/"+pathId
            r = requests.get(url,headers=headers,verify=False)
            response_json = r.json()
            print ("\nGET /flow-analysis/pathId Status: ",r.status_code)
            print ("\n*** Response from GET /flow-analysis/pathId.- Trace path information. ***\n",json.dumps(response_json,indent=4))


