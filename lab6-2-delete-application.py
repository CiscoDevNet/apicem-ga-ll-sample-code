from apicem_config import * # APIC-EM IP is assigned in apicem_config.py

# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}

#### list all custom applications and return the list for further use ####
def list_custom_app(api="",key="",value='',name="",uid=""):
    url = "https://"+apicem_ip+"/api/"+version+api     # API base url
    app = []
    try:
        resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
        status = resp.status_code
        # print("status: ",status)
        response_json = resp.json() # Get the json-encoded content from response
        app = response_json["response"] # application list
    except:
        print ("Something wrong, cannot get application information")
        sys.exit()  
    
    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()
    # Make sure there is at least one application
    if app != [] :   # if response is not empty 
        app_list = []
        app_show_list = []
        # Extracting attributes
        idx = 0
        for item in app:
            app_list.append([item[name],item[uid]])
            if item[key] == value:
                idx=idx+1
                app_show_list.append([idx,item[name],item[uid]])
        # Show all custom applications
        # Pretty print tabular data, needs 'tabulate' module
        if app_show_list == []:
            print ("No custom NBAR2 application found !")
            sys.exit()
        else:
            print (tabulate(app_show_list, headers=['number','custom application','id'],tablefmt="rst"),'\n')
            return app_show_list
# End of function

print ("Processing custom application list, please wait......\n")
custom_app=list_custom_app("/application","longDescription","custom application","name","instanceUuid")

######## select an application and delete it #######
select = True
id = ""
# Ask user's input 
# In the loop until 'id' is assigned or user select 'exit'

while select:
    user_input = input('=> Enter a number to select an application to delete:' )
    user_input= user_input.replace(" ","") # ignore space
    if user_input.lower() == 'exit': 
        sys.exit()
    if user_input == "" or int(user_input) < 1 or int(user_input) > len(custom_app):
        print ("Oops! number out of range, please try again or enter 'exit'")
    else:
        id = custom_app[int(user_input)-1][2]
        break
# End of while loop
            
#### Delete ####
delete_url = "https://"+apicem_ip+"/api/"+version+"/application/"+id
resp= requests.delete(delete_url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
print("status: ",resp.status_code)
print ("Response:",json.dumps(resp.json(),indent=4))
