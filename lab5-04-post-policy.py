from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}

########### Ask user to enter a policy name ##############
# In the loop until input is not null or is 'exit'
select = True
while select:
    policy_name = input('=> Enter policy name that you like to create: ')
    policy_name = policy_name.replace(" ","") # ignore space
    if policy_name.lower() == 'exit': 
        sys.exit()  
    if policy_name == "":
        print ("Oops! Policy name cannot be NULL please try again or enter 'exit'")
    else:
        break
    
########### Ask user to select a policy tag name ##############
url = "https://"+apicem_ip+"/api/"+version+"/policy/tag" # policy tag url
resp = requests.get(url,headers=headers,verify=False)
response_json = resp.json()
tag = response_json["response"] # policy tags
if tag ==[] :
    print ("No policy tag found, create policy tag first !")
    sys.exit()
    
print ("Policy Tag:")
print ("----------------------------")
i = 0
for item in tag:
    i=i+1
    print (i,"-",item["policyTag"])
select = True

# In the loop until tag is selected or user select 'exit'
while select:
    tag_num = input('=> Enter a number above for policy tag: ')
    tag_num = tag_num.replace(" ","") # ignore space

    if tag_num.lower() == 'exit': 
        sys.exit()           
    if tag_num == "" or int(tag_num) < 1 or int(tag_num) > i:
        print ("Oops! number out of range, please try again or enter 'exit'")
    else:
        tag_name = tag[int(tag_num)-1]["policyTag"]
        break 
# End of while loop

    
########## Select an application and retrieve its id #################
url = "https://"+apicem_ip+"/api/"+version+"/application"     # API base url
app = []
try:
    resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
    status = resp.status_code
    print("status: ",status)
    response_json = resp.json() # Get the json-encoded content from response
    app = response_json["response"] # network-device
except:
    print ("Something wrong, cannot get application information")
    sys.exit()  
    
if status != 200:
    print ("Response status %s,Something wrong !"%status)
    print (resp.text)
    sys.exit()

# Make sure there is at least one application
if app == []:
    print ("Something wrong for retrieving applications!")
    sys.exit()

app_list = []
# Extracting attributes
for item in app:
    app_list.append([item["name"],item["instanceUuid"]])
# Show all NBAR2 applications
# Pretty print tabular data, needs 'tabulate' module
print (tabulate(app_list, headers=['application','id'],tablefmt="rst"),'\n')
# Ask user's select application in order to retrieve its id 
# In the loop until 'id' is assigned or user select 'exit'
select = True
app_id = ""
while select:
    app_name = input('=> Enter application name(case-sensitive) from above:')
    app_name = app_name.replace(" ","") # ignore space
    if app_name.lower() == 'exit': 
        sys.exit()           
    for item in app_list:
        if app_name in item: # if user_input is matched
            app_id = item[1]
            select = False
            break
    if app_id == "":
        print ("Oops! application name found, please try again or enter 'exit'")
# End of while loop

########## Creating policy #############
### JSON object for POST /policy
policy_json = [{
    "policyName": policy_name,
    "policyOwner": "admin",
    "policyPriority": 4095,
    "resource": {
      "applications": [   
          {
            "appName": app_name,
            "id": app_id
          }]
    },
    "actions": [
        "SET_PROPERTY"
    ],
    "policyScope": tag_name,
    "actionProperty": {
        "relevanceLevel": "Business-Relevant"
    }
}]

# POST policy url
post_url = "https://"+apicem_ip+"/api/"+version+"/policy"     # API base url
resp = requests.post(post_url, json.dumps(policy_json), headers=headers,verify=False)
status = resp.status_code
print("status: ",status)
print("Response:",json.dumps(resp.json(),indent=4))

