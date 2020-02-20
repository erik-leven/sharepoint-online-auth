
"""
Web-client:
create a web-app in Azure Active Directory" (ADD)
1.1) Select "New registration" under "App registrations" in the ADD and select "Web" under "Redirect URI (optional)"
1.2) Create a secret or upload a certificate for authentication to azure
1.3.1) Secret: Enter your newely registered app. Select "Certificates & secrets" in the "manage" view. Click on "New client secret" and copy the Value.
1.3.2) Certificate: Save the private key of the certificate (the whole file). Upload the public key of your certifcate (.cer-, .pem- or .crt-file) and copy the thumbprint generated as you upload the public key.
1.3.2.1) Example of generating a certificate: 
		openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
		The line above will (on Ubuntu at least) generate 2 files, cert.pem (public key) and key.prm (private key).

1.4) Configure permissions (scopes) for the new app under the "API permissions" view inside the "manage" view of your app. An admin needs to "Grant admin consent for <app-name>" to validate the persmissions" 

Public-client:
create a web-app in Azure Active Directory" (ADD)
1.1) Select "New registration" under "App registrations" in the ADD and select "Public client/native (mobile and desktop)" under "Redirect URI (optional)"
1.2) Select the permissions of the app
1.3) Select the permissions of different users 

"""

# Generate an access token for the SP-RestAPI

import requests
import json
import logging
import msal
from cryptography import x509
from cryptography.hazmat.backends import default_backend

logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('Sharepoint online auth')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


#client_id           = "be546248-254d-4a0b-8a3d-2520228b4657"
#tenant_id           = "f2716ff5-b2ec-46c4-a1e7-fa482bf4b365"  # Also known as Bearer realm. If not available, it can be found by looking at the headers from a get request to https://<target_host>/_vti_bin/client.svc with headers={"Authorization":"Bearer"}
#client_secret       = "J_/-wn6z?nnM7Ztsdi1rqK6KD_fTUx2Y"
#target_host         = "sesaminternaltesting.sharepoint.com"        # The sharepoint host connected to your Azure app
#thumbprint          = "80B094282DC306E0FB4F4328107B957271051954"


def cert2string(cert_location):

    backend = default_backend()
    with open(cert_location, 'rb') as f:
        crt_data = f.read()
    return crt_data

def get_access_token_basic_auth(client_id, tenant_id, target_host, username, password, scopes = None):
    import msal
    if client_id == None:
        logger.error("Missing client_id. Exiting..")
        AssertionError
    if tenant_id == None:
        logger.error("Missing tenant_id. Exiting..")
        AssertionError
    if target_host == None:
        logger.error("Missing target_host. Exiting..")
        AssertionError
    if username == None:
        logger.error("Missing username. Exiting..")
        AssertionError
    if password == None:
        logger.error("Missing password. Exiting..")
        AssertionError
    if scopes == None:
        scopes = "https://" + target_host + "/.default"
    if type(scopes) != list:
        logger.error("The variable 'scopes' much be a list")
        AssertionError
    
    authority = "https://login.microsoftonline.com/{}".format(tenant_id)
    app = msal.PublicClientApplication(client_id = client_id, authority = authority)
    result = app.acquire_token_by_username_password(username, password, scopes=scopes)
    try:
        result['access_token']
    except KeyError:
        logger.error("Unexpected response text: {}".format(result))
        raise AssertionError  
    return result

    


def get_access_token_oath2_secret(client_id, client_secret, tenant_id, target_host):
    if client_id == None:
        logger.error("Missing client_id. Exiting..")
        AssertionError
    if client_secret == None:
        logger.error("Missing client_secret. Exiting..")
        AssertionError
    if tenant_id == None:
        logger.error("Missing tenant_id. Exiting..")
        AssertionError
    if target_host == None:
        logger.error("Missing target_host. Exiting..")
        AssertionError

    grant_type          = "client_credentials"
    target_identifier   = "00000003-0000-0ff1-ce00-000000000000" # Always the same for Sharepoint
    SO_client_id        = client_id + "/" + target_identifier + "@" + tenant_id
    url = "https://accounts.accesscontrol.windows.net/" + tenant_id + "/tokens/OAuth/2"
    resource = target_identifier + "/" + target_host + "@" + tenant_id
    data = {"client_id": SO_client_id, "client_secret": client_secret, "resource": resource,"grant_type": grant_type} 

    req = requests.post(url, headers={'accept': 'application/x-www-form-urlencoded'}, data=data)
    if req.status_code != 200:
        logger.error("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
        raise AssertionError    
    return req.json()


def get_access_token_oath2_certificate(client_id, tenant_id, target_host, private_key_location, thumbprint, scopes):
    if client_id == None:
        logger.error("Missing client_id. Exiting..")
        AssertionError
    if tenant_id == None:
        logger.error("Missing tenant_id. Exiting..")
        AssertionError
    if target_host == None:
        logger.error("Missing target_host. Exiting..")
        AssertionError
    if private_key_location == None:
        logger.error("Missing private_key_location. Exiting..")
        AssertionError
    if thumbprint == None:
        logger.error("Missing thumbprint. Exiting..")
        AssertionError
    if scopes == None:
        scopes = "https://" + target_host + "/.default"
    if type(scopes) != list:
        logger.error("The variable 'scopes' much be a list")
        AssertionError

    key  = cert2string(private_key_location)
    authority = "https://login.microsoftonline.com/" + tenant_id
    client_credential = {"private_key": key, "thumbprint": thumbprint}
    app = msal.ConfidentialClientApplication(client_id = client_id, client_credential=client_credential, authority=authority, validate_authority=True, token_cache=None, verify=True, proxies=None, timeout=None, client_claims=None, app_name=None, app_version=None)
    result = app.acquire_token_for_client(scopes)
    try:
        result['access_token']
    except KeyError:
        logger.error("Unexpected response text: {}".format(result))
        raise AssertionError    
    return result

#y = get_access_token_basic_auth("erik.leven@sesaminternaltesting.onmicrosoft.com", "Bibbla87")
#print(get_access_token_oath2_certificate(client_id, "key.pem", thumbprint, tenant_id, target_host))

#access_token = get_access_token_oath2_secret(client_id, client_secret, tenant_id, target_host)
#print(access_token)

