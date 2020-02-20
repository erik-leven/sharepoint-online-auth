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