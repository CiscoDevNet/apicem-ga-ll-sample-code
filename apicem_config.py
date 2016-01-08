# Configure APIC-EM IP, username, password, also create a function to obtain a service ticket
import requests   # We use Python external "requests" module to do HTTP GET query
import json       # External JSON encoder and decode module
import sys        # For system-specific functions

# Please note that you may want install this external module in your working environment
# We just copy source code in here for the convenient
from tabulate import tabulate

# It's used to get rid of certificate warning messages when using Python 3.
# For more information please refer to: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings() # Disable warning message

# Step 1
# Change apic-em IP to the one you are using
apicem_ip = "sandboxapic.cisco.com:9443"

# Step 2
# Eneter user name and password to get a service ticket
# If you assign username, password and version here you don't need to pass parameter when calling
username = "admin"
password = "1vtG@lw@y"
version = "v1"

def get_X_auth_token(ip=apicem_ip,uname = username,pword = password):
    """ 
    This function returns a new service ticket.
    Passing ip, username and password when use as standalone function
    or overwrite the configuration above.
    """
    global version
    
    # JSON input for the post ticket API request 
    r_json = {
    "username": uname,
    "password": pword
    }
    # url for the post ticket API request 
    post_url = "https://"+ip+"/api/"+version+"/ticket"
    # All APIC-EM REST API query and response content type is JSON   
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, data = json.dumps(r_json), headers=headers,verify=False)
        # remove '#' if need to print out response 
        # print (r.text)
        
        # return service ticket
        return r.json()["response"]["serviceTicket"]
    except:
        # Something wrong, cannot get service ticket
        print ("Status: %s"%r.status_code)
        print ("Response: %s"%r.text)
        sys.exit ()
        
