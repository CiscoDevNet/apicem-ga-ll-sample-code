from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"content-type" : "application/json","X-Auth-Token": ticket}
try:
    app_json=json.load(open("lab5-03-post-application.json", "r"))
except:
    print ("Something wrong with opening JSON file !")
    sys.exit()
    
########## Ask user enetr application name ##########
# In the loop until input is not null or is 'exit'
select = True
while select:
    pApp = input('=> Enter application name that you like to create: ')
    pApp = pApp.replace(" ","") # ignore space
    if pApp.lower() == 'exit': 
        sys.exit()  
    if pApp == "":
        print ("Oops! tag name cannot be NULL please try again or enter 'exit'")
    else:
        break
    
########## Get category id ##########
url = "https://"+apicem_ip+"/api/"+version+"/category"
try:
    resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET 'category" request
    response_json = resp.json() # Get the json-encoded content from response
    categories = response_json["response"] # category
except:
    print ("Something wrong, cannot get application information")
    sys.exit()
for item in categories:
    if item["name"] == app_json["category"]:
        app_json["categoryId"] = item["id"]    

# populate user input to JSON object
app_json["helpString"] = pApp
app_json["name"] = pApp
app_json["ignoreConflict"] = True
                                
# convert to list -- this API requires that 
app_json = [app_json]

# policy tag url
post_url = "https://"+apicem_ip+"/api/"+version+"/application"     # API base url

resp = requests.post(post_url, json.dumps(app_json), headers=headers,verify=False)
status = resp.status_code
print("status: ",status)
print("Response:",json.dumps(resp.json(),indent=4))

