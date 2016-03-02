from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}

# Ask user's input 
# In the loop until input is not null or is 'exit'
select = True
while select:
    pTag = input('=> Enter policy tag name that you like to create: ')
    pTag = pTag.replace(" ","") # ignore space
    if pTag.lower() == 'exit': 
        sys.exit()  
    if pTag == "":
        print ("Oops! Policy tag name cannot be NULL please try again or enter 'exit'")
    else:
        break

# post policy tag url
post_url = "https://"+apicem_ip+"/api/"+version+"/policy/tag"     # API base url

tag_json = {
  "policyTag": pTag
}

resp = requests.post(post_url, json.dumps(tag_json), headers=headers,verify=False)
status = resp.status_code
print("status: ",status)
print ("Response:",json.dumps(resp.json(),indent=4))
