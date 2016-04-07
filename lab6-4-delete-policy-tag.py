from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket,'content-type': 'application/json'}


######## select a policy tag to associate with device ##########

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
# Ask user's input 
# In the loop until tag is selected or user select 'exit'
tag_to_delet=""
while select:
    tag_num = input('=> Enter a number from above to delete policy tag: ')
    tag_num = tag_num.replace(" ","") # ignore space
    if tag_num.lower() == 'exit': 
        sys.exit()           
    if tag_num == "" or int(tag_num) < 1 or int(tag_num) > i:
        print ("Oops! number is out of range, please try again or enter 'exit'")
    else:
        tag_to_delet=tag[int(tag_num)-1]["policyTag"]
        break
    
# End of while loop

if tag_to_delet=="":
    print ("For some reason, tag name is NULL!")
    sys.exit()

#### Delete ####
param={'policyTag':tag_to_delet}
delete_url = "https://"+apicem_ip+"/api/"+version+"/policy/tag/"
resp= requests.delete(delete_url,params=param,headers=headers,verify = False)
print("status: ",resp.status_code)
print ("Response:",json.dumps(resp.json(),indent=4))

    
