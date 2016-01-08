from apicem_config import * # Including apicem_config.py

# Get service ticket by using function created in apicem_config.py
ticket = get_X_auth_token( )

# X-Auth-Token header
headers = {"X-Auth-Token": ticket}

# API base url
url = "https://"+apicem_ip+"/api/"+version+"/user"

# Request and response (result) of "GET /user" API, "X-Auth-Token" header is in the request
resp= requests.get(url,headers=headers,verify = False)

# Get the json-encoded content from response
response_json = resp.json()

# This is the http request status
print ("Status: ",resp.status_code)

# Convert "response_json" object to a JSON formatted string and print it out    
print (json.dumps(response_json,indent=4),'\n') 

# Parsing raw response to list all users and their role
for item in response_json["response"]:
    for item1 in item["authorization"]:
        print ("User %s, role is the %s."%(item["username"],(item1["role"])[5:]))
