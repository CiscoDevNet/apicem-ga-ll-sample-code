from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

######## select a policy tag to associate with device ##########
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket,'content-type': 'application/json'}

url = "https://"+apicem_ip+"/api/"+version+"/policy/tag"
resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /policy" request
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
    tag_num = input('=> Enter a number from above to delete policy tag association: ')
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


# policy tag association list
p_tag_association= []
url = "https://"+apicem_ip+"/api/"+version+"/policy/tag/association"
try:
    resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /policy" request
    status = resp.status_code
    print("status: ",status)
    response_json = resp.json() # Get the json-encoded content from response
    p_tag_association = response_json["response"] # network-device
except:
    print ("Something wrong, cannot get policy information")
    sys.exit()  
    
if status != 200:
    print ("Response status %s,Something wrong !"%status)
    print (resp.text)
    sys.exit()

# Make sure there is at least one network device
if p_tag_association == "":
    print ("No Tag Association found !")
    sys.exit()


# if response is not empty 
device=[]
# Extracting attributes

for item in p_tag_association:
    if item["policyTag"] == tag_to_delet:
        i=0
        if item["networkDevices"] == []:
            print ("Tag is not associated with any device")
            sys.exit()
        else:    
            for item1 in item["networkDevices"]:
                i=i+1
                device.append([i,item1["deviceName"],item1["deviceIp"],item1["deviceId"]])

print (tabulate(device, headers=['number','Device Name','device IP','Device ID'],tablefmt="rst"),'\n')

while select:
    num = input('=> Enter a number from above to delete policy tag association: ')
    num = num.replace(" ","") # ignore space
    if tag_num.lower() == 'exit': 
        sys.exit()           
    if tag_num == "" or int(tag_num) < 1 or int(tag_num) > i:
        print ("Oops! number is out of range, please try again or enter 'exit'")
    else:
        device_id_to_delet=device[int(num)-1][3]
        break   
# End of while loop


delete_url = "https://"+apicem_ip+"/api/"+version+"/policy/tag/association"
params={"policyTag":tag_to_delet,"networkDeviceId":device_id_to_delet}

resp= requests.delete(delete_url,params=params,headers=headers,verify = False)
print("status: ",resp.status_code)
print ("Response:",json.dumps(resp.json(),indent=4))




