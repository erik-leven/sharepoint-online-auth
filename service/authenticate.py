# Generate an access token for the SPO-RestAPI

import requests
import json
import logging
import msal

logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('Sharepoint online auth')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

def get_access_token_basic_auth(client_id, tenant_id, target_host, username, password, scopes = None):
    if client_id == None:
        logger.error("Missing client_id. Can be found in 'App registrations' in Azure Active Directory. Exiting..")
        AssertionError
    if tenant_id == None:
        logger.error("Missing tenant_id. Can be found in 'Overview' in Azure Active Directory. Exiting..")
        AssertionError
    if target_host == None:
        logger.error("Missing target_host. I.e. <mycompany.sharepoint.com>. Exiting..")
        AssertionError
    if username == None:
        logger.error("Missing username. I.e. <first_name.last_name@<my_company.onmicrosoft.com>. Exiting..")
        AssertionError
    if password == None:
        logger.error("Missing password. Exiting..")
        AssertionError
    if scopes == None:
        logger.info("Using default scope")
        scopes = ["https://" + target_host + "/.default"]
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
        logger.error("Missing client_id. Can be found in 'App registrations' in Azure Active Directory. Exiting..")
        AssertionError
    if tenant_id == None:
        logger.error("Missing tenant_id. Can be found in 'Overview' in Azure Active Directory. Exiting..")
        AssertionError
    if client_secret == None:
        logger.error("Missing client_secret. Exiting..")
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


def get_access_token_oath2_certificate(client_id, tenant_id, target_host, private_key, thumbprint, scopes = None):
    if client_id == None:
        logger.error("Missing client_id. Can be found in 'App registrations' in Azure Active Directory. Exiting..")
        AssertionError
    if tenant_id == None:
        logger.error("Missing tenant_id. Can be found in 'Overview' in Azure Active Directory. Exiting..")
        AssertionError
    if target_host == None:
        logger.error("Missing target_host. Exiting..")
        AssertionError
    if private_key == None:
        logger.error("Missing private_key. Exiting..")
        AssertionError
    if thumbprint == None:
        logger.error("Missing thumbprint. Exiting..")
        AssertionError
    if scopes == None:
        logger.info("Using default scope")
        scopes = ["https://" + target_host + "/.default"]
    if type(scopes) != list:
        logger.error("The variable 'scopes' much be a list")
        AssertionError

    authority = "https://login.microsoftonline.com/" + tenant_id
    client_credential = {"private_key": private_key, "thumbprint": thumbprint}
    app = msal.ConfidentialClientApplication(client_id = client_id, client_credential=client_credential, authority=authority, validate_authority=True, token_cache=None, verify=True, proxies=None, timeout=None, client_claims=None, app_name=None, app_version=None)
    result = app.acquire_token_for_client(scopes)
    try:
        result['access_token']
    except KeyError:
        logger.error("Unexpected response text: {}".format(result))
        raise AssertionError    
    return result