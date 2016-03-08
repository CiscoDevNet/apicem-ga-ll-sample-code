from apicem_config import * # apicem_config.py is the central place to change the apic-em IP, username, password ...etc
import threading,time # Need it for delay - sleep() function

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

# Check get flow Analysis status with flowAnalysisId
try:
    flowAnalysisId = response_json["response"]["flowAnalysisId"]
except:
   print ("\n For some reason cannot get flowAnalysisId")
   sys.exit()
else:
    url = "https://"+apicem_ip+"/api/"+version+"/flow-analysis/"+flowAnalysisId
    r = requests.get(url,headers=headers,verify=False)
    response_json = r.json()
    print ("\nGET flow-analysis with flow-analysisId status: ",r.status_code)
    print ("Response from GET /flow-analysis/"+flowAnalysisId,json.dumps(response_json,indent=4))
    status = response_json["response"]["request"]["status"]
#   print (status)

# non-blocking wait
def check_status(arg):
    count = 0
    status = arg
    while status != "COMPLETED":
        if status == "FAILED":
            print("Unable to find full path. No traceroute or netflow information found. Failing path calculation.")
            sys.exit()
        print ("\nTask is not finished yet, sleep 1 second then try again")
        count += 1
        if count > 30:
            print ("\nNo routing path was found. Please try using different source and destination !")
            sys.exit()
        try:
            url = "https://"+apicem_ip+"/api/"+version+"/flow-analysis/"+flowAnalysisId
            r = requests.get(url,headers=headers,verify=False)
            response_json = r.json()
            print ("\nGET flow-analysis with flow-analysisId status: ",r.status_code)
            print ("Response from GET /flow-analysis/"+flowAnalysisId,json.dumps(response_json,indent=4))
            status = response_json["response"]["request"]["status"]
        except:
            # Something is wrong
            print ("\nSomething is wrong when executing get /flow-analysis/{flowAnalysisId}")

thread = threading.Thread(target=check_status, args=(status,))
thread.start()    
print ("\n!!!!!!!!! Non blocking !!!!!!!!!\n")
