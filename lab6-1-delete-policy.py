from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}


# policy list
url = "https://"+apicem_ip+"/api/"+version+"/policy"     # API base url
policy = []
try:
    resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
    status = resp.status_code
    print("status: ",status)
    response_json = resp.json() # Get the json-encoded content from response
    policy = response_json["response"] # network-device
except:
    print ("Something wrong, cannot get application information")
    sys.exit()  
    
if status != 200:
    print ("Response status %s,Something wrong !"%status)
    print (resp.text)
    sys.exit()

# Make sure there is at least one policy
if policy != [] :   # if response is not empty 
    policy_list = []
    # Extracting attributes
    for item in policy:
        policy_list.append([item["policyName"],item["instanceUuid"]])
    # Show all policies
    # Pretty print tabular data, needs 'tabulate' module
    print (tabulate(policy_list, headers=['policy','id'],tablefmt="rst"),'\n')
    # Ask user input

print ("!!! BUSINESS_RELEVANT_CVD_Policy,DEFAULT_CVD_Policy,BUSINESS_IRRELEVANT_CVD_Policy !!!")
print ("!!! These are default policies cannot be deleted !!!") 

######## select a policy to delete #######

select = True

# Ask user's input 
# In the loop until 'id' is assigned or user select 'exit'
while select: # at this moment we just want to find out if user's input is matched policy list
    user_input = input('=> Enter policy name(case-sensitive, key name only without "-BR","-IR"or "-D") from above to delete:')
    user_input= user_input.replace(" ","") # ignore space
    if user_input.lower() == 'exit': 
        sys.exit()           
    for item in policy_list:
        if user_input in item or (user_input+"-BR") in item or (user_input+"-IR") in item or (user_input+"-D") in item: # if user_input is matched
            id = item[1] # policy id
            select = False
            break
    if id == "":
        print ("Oops! Policy name not found, please try again or enter 'exit'")
policy_name = user_input
# End of while loop

#### Delete ####

for item in policy_list:
    if policy_name in item: 
        id = item[1] # policy id
        print ("Deleting",policy_name,"....")
        delete_url = "https://"+apicem_ip+"/api/"+version+"/policy/"+id
        resp= requests.delete(delete_url,headers=headers,verify = False)
    if (policy_name+"-D") in item: # if user_input is matched
        id = item[1] # policy id
        print ("Deleting",policy_name+"-D","....")
        delete_url = "https://"+apicem_ip+"/api/"+version+"/policy/"+id
        resp= requests.delete(delete_url,headers=headers,verify = False)
    if (policy_name+"-BR") in item: # if user_input is matched
        id = item[1] # policy id
        print ("Deleting",policy_name+"-BR","....")
        delete_url = "https://"+apicem_ip+"/api/"+version+"/policy/"+id
        resp= requests.delete(delete_url,headers=headers,verify = False)
    if (policy_name+"-IR") in item: # if user_input is matched
        id = item[1] # policy id
        print ("Deleting",policy_name+"-IR","....")
        delete_url = "https://"+apicem_ip+"/api/"+version+"/policy/"+id
        resp= requests.delete(delete_url,headers=headers,verify = False)
    

