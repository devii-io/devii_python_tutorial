"""This module is for recieving a access token from Devii"""

import requests

AUTH_URL = "https://api.devii.io/auth"


def get_access_token():
    """this is to get the access token for the application"""

    # Create a dictionary to store the form data
    data = {
        "login": "--login--",
        "password": "--password--",
        "tenantid": "--tennentid--",
    }

    # Make the POST request
    response = requests.post(AUTH_URL, data=data)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the access token
        access_token = json_response.get("access_token")
        if access_token:
            # uncomment the line below if you would like to test the retrival of the access token
            # print("this is your access token:", access_token)
            return access_token
        else:
            print("Access token not found in the response.")
    else:
        print("Error:", response.status_code)
        print(response.text)


access_token = get_access_token()

# Headers you will need for all http post calls
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
