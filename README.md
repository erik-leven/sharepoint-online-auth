# Sharepoint authentication for access token via Azure  
Library for receiving access tokens for Azure apps.


## Web-client:
*Create a web-app in Azure Active Directory (ADD)*


1. Enter *New registration* under *App registrations* in ADD and select *Web* under *Redirect URI (optional)*

2. Set credentials

    2.1. Secret:
        Enter your newely registered app. Select *Certificates & secrets* in the *manage* view. Click on *New client secret* and copy the Value.

    2.2. Certificate:

        
            openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
        
        The line above will (on Ubuntu at least) generate 2 files, cert.pem (public key) and key.prm (private key). 

        2.2.2. Setting the certificate credentials
        Save the private key of the certificate (as a string). Upload the public key of your certifcate (.cer-, .pem- or .crt-file) and copy the thumbprint generated as you upload the public key.

3) Configure permissions (scopes) for the new app under the *API permissions* view inside the *manage* view of your app. An admin needs to *Grant admin consent for <app_name> to validate the persmissions* 

*Create a Public-client in Azure Active Directory*:

1. Select *New registration* under *App registrations* in the ADD and select *Public client/native (mobile and desktop)* under *Redirect URI (optional)*
2. Select the permissions of the app
3. Select the permissions of different users 
4. Under *Authentication* in your Azure app, set *Treat application as a public client* to *yes*