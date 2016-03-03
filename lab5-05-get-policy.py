from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}

# policy list
url = "https://"+apicem_ip+"/api/"+version+"/policy"     # API base url
policy = []
try:
    resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /policy" request
    status = resp.status_code
    print("status: ",status)
    response_json = resp.json() # Get the json-encoded content from response
    policy = response_json["response"] # network-device
except:
    print ("Something wrong, cannot get policy information")
    sys.exit()  
    
if status != 200:
    print ("Response status %s,Something wrong !"%status)
    print (resp.text)
    sys.exit()

# Make sure there is at least one network device

if policy == [] :
    print ("No policy found !")
    sys.exit()
# if response is not empty 
policy_list = []
# Extracting attributes
for item in policy:
    policy_list.append([item["policyName"],item["instanceUuid"]])
# Show all policies
# Pretty print tabular data, needs 'tabulate' module
print (tabulate(policy_list, headers=['policy','id'],tablefmt="rst"),'\n')
    
 

