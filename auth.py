"""This module is for recieving a access token from Devii"""

import json
import os
import requests
import jwt
from datetime import datetime, timezone


AUTH_URL = "https://apidev.devii.io/auth"

# Create a json file to store and load your tokens, please note that is not best 
# practice but a simple exaple to show how to use the tokens.

TOKEN_FILE = 'token.json'


def load_token():
    '''Load the tokens from the token.json file'''
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    else:
        return None
    
def save_token(token):
    '''Save the tokens to the token.json file'''
    with open(TOKEN_FILE, 'w') as file:
        json.dump(token, file)   
    
# Next, a function to login and retrieve your access token from Devii.  
# For this function you will need to have your tenant id, if you need to find it you can find the instructions
#  in https://docs.devii.io/docs/devii_portal/project_details#tenant-id-and-project-id.
                            
def login():
    
    """Retreive tokens for the application"""

    # Create a dictionary to store the form data
    data = {
        "login": "<your Devii user name>",
        "password": "<your Devii Root role password>",
        "tenantid": "<your tenant ID>",
    }

    # Make the POST request to the Devii authentication endpoint with the provided data.
    response = requests.post(AUTH_URL, data=data)

    # Check for a successful response, if status code is 200 parse the JSON response
    if response.status_code == 200:
        json_response = response.json()

        # Extract the access token
        access_token = json_response.get("access_token")
        refresh_token = json_response.get("refresh_token")
        roleid = json_response.get("roleid")
        # Save the refresh token to a file
        save_token({"access_token": access_token, "refresh_token": refresh_token, "roleid": roleid})

    else: 
        print("error in login: ", response.status_code)
        print(response.text)

# The following code provides a mechanism for managing authentication tokens. The refresh_access_token function 
# refreshes the access token using a refresh token, ensuring continued access to resources. If the token file does not 
# exist, it initiates a login process. The is_token_expired function checks whether a token has expired by decoding 
# it and comparing the expiration time with the current time. The ensure_token_exists function ensures valid tokens 
# are present, refreshing or renewing them as necessary. If either the access or refresh token is expired or missing, it 
# either refreshes the tokens or logs in again to obtain new ones.

def refresh_access_token():
    """Refresh the access token using the refresh token"""

    #ensure the token file exists
    if not os.path.exists(TOKEN_FILE):
        print("Token file not found, logging in...")
        login()
        return

    #load the refresh token from the token file
    refresh_token = load_token().get('refresh_token')
    
    #header to send to the Devii authentication endpoint for new tokens using the refresh token
    refresh_headers = {
        "Authorization": f"Bearer {refresh_token}",
        "Content-Type": "application/json",
    }

    # Make the POST request to the Devii authentication endpoint with the provided data.
    response = requests.get(AUTH_URL, headers=refresh_headers)

    # Check for a successful response, if status code is 200 parse the JSON response and extract tokens then save them to the token file
    if response.status_code == 200:
        json_response = response.json()
        access_token = json_response.get("access_token")
        refresh_token = json_response.get("refresh_token")
        roleid = json_response.get("roleid")
        save_token({"access_token": access_token, "refresh_token": refresh_token, "roleid": roleid})
        return access_token
    
    else:
        print("error in refresh access token: ", response.status_code)
        print(response.text)    

    

def is_token_expired(token):
    '''Check if refresh token has expired'''
    
    # Decode the token without verifying the signature
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    expiration_timestamp = decoded_token['exp']

    # Extract expiration time from decoded token
    if expiration_timestamp:
        expiration_datetime = datetime.fromtimestamp(expiration_timestamp, tz=timezone.utc)
        print("Expiration Time:", expiration_datetime)
        return expiration_datetime < datetime.now(timezone.utc)
    return False

def ensure_token_exists():
    '''checking to see if the token exists'''

    if not os.path.exists(TOKEN_FILE):
        print("Token file not found, logging in...")
        login()
        return

    access_token = load_token().get('access_token')
    refresh_token = load_token().get('refresh_token')
    
    if access_token is None or is_token_expired(access_token):
        if refresh_token is None or is_token_expired(refresh_token):
            print("Refresh token expired or not found, logging in...")
            login()
        else:
            print("Access token expired, refreshing token...")
            refresh_access_token()

# This line calls the start of token retrival process 

ensure_token_exists()



# Load the refresh token from the token.json file
access_token = load_token().get('access_token')

# If you would like tot test the access token uncomment the code below to print the access token
# print("ACCESS TOKEN: ", access_token)

# Headers you will need for all http post calls
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
