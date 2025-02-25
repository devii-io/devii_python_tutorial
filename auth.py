"""This module is for receiving a access token from Devii"""

import json
import os
import requests
import jwt
from datetime import datetime, timezone


AUTH_URL = "https://apidev.devii.io/auth"

# Create a json file to store and load your tokens, please note that is not best 
# practice but a simple example to show how to use the tokens.

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

def login(data):
    
    """Retreive tokens for the application"""
    print("logging in...")
        # Make the POST request to the Devii authentication endpoint with the provided data.
    response = requests.post(AUTH_URL, data=data)

    print("data: ", data)

    # Check for a successful response, if status code is 200 parse the JSON response
    if response.status_code == 200:
        json_response = response.json()

        # Extract the access token
        access_token = json_response.get("access_token")
        refresh_token = json_response.get("refresh_token")
        roleid = json_response.get("roleid")
        message = json_response.get("message")
        # Save the refresh token to a file
        save_token({"access_token": access_token, "refresh_token": refresh_token, "roleid": roleid, "message": message})
        print("message: ", message)
        
    else: 
        print("error in login: ", response.status_code)
        print("response from login: ", response.text)

    return {"status_code": response.status_code, "message": response.text}


# The following code provides a mechanism for managing authentication tokens. The refresh_access_token function 
# refreshes the access token using a refresh token, ensuring continued access to resources. If the token file does not 
# exist, it initiates a login process. The is_token_expired function checks whether a token has expired by decoding 
# it and comparing the expiration time with the current time. The ensure_token_exists function ensures valid tokens 
# are present, refreshing or renewing them as necessary. If either the access or refresh token is expired or missing, it 
# either refreshes the tokens or logs in again to obtain new ones.

def refresh_access_token(data):
    """Refresh the access token using the refresh token"""
    #ensure the token file exists
    if not os.path.exists(TOKEN_FILE):
        print("Token file not found, logging in...")
        login(data)
        return

    #load the refresh token from the token file
    refresh_token = load_token().get('refresh_token')
    print("refresh_token: ", refresh_token)
    
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
    return {"status_code": response.status_code, "message": response.text}

    

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

def ensure_token_exists(data):
    '''Check if the token exists and return appropriate response code'''

    if not os.path.exists(TOKEN_FILE):
        print("Token file not found, logging in...")
        response = login(data)
        if response and response.get("status_code") == 200:  # Safeguard added
            return {"status_code": 200, "message": "Logged in successfully"}
        else:
            return {"status_code": response.get("status_code", 500), "message": "Login failed"}  # Fallback to 500 if None

    # Load the tokens from the token file

    username = data.get('login').strip().lower()    

    # Check if the token file exists and the user is already logged in
    if os.path.exists(TOKEN_FILE):
        token_message = load_token().get('message')
        print("token_message: ", token_message)
        print("username: ", username)
        print(f'Logged in as {username}.')
        print("Token file found, checking token...")
        with open(TOKEN_FILE, 'r') as file:
            token_data = json.load(file)
            token_message = token_data.get('message', '').strip().lower()
            expected_message = f"logged in as {username}.".strip().lower()

            if token_message == expected_message:
                print("User is already logged in.")
                return {"status_code": 200, "message": "Logged in successfully"}
            else:
                print("Token file found, but user is not logged in.")
                return login(data)
            


    access_token = load_token().get('access_token')
    print("access_token enure exits: ", access_token)
    refresh_token = load_token().get('refresh_token')

    # Check if the access token is missing or expired
    if access_token is None or is_token_expired(access_token):
        # If the refresh token is also expired or missing, log in again
        if refresh_token is None or is_token_expired(refresh_token):
            print("Refresh token expired or not found, logging in...")
            response = login(data)
            if response and response.get("status_code") == 200:  # Safeguard added
                return {"status_code": 200, "message": "Logged in successfully"}
            else:
                return {"status_code": response.get("status_code", 500), "message": "Login failed"}  # Fallback to 500 if None
        else:
            print("Access token expired, refreshing token...")
            new_access_token = refresh_access_token(data)
            if new_access_token:
                return {"status_code": 200, "message": "Access token refreshed"}
            else:
                return {"status_code": 401, "message": "Token refresh failed"}


    # If the access token is still valid, return success code
    # print("Access token is valid.")
    # return {"status_code": 200, "message": "Access token is valid"}
    # return { "status_code": response.status_code, "message": response.text}
    

# Load the access token from the token.json file
def get_access_token():
    '''Get the access token from the token file'''
    access_token = load_token().get('access_token')
    print("access_token get access token: ", access_token)
    return access_token

# Function to get headers with the latest access token
def get_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
    }

# Function to logout the user and remove the token file
def logout():
    '''Logout the user and remove the token file'''
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return {"status": "success", "message": "User logged out successfully"}
    return {"status": "error", "message": "User not logged in"}
