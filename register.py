"""This module is for registering for a role Devii"""

import json
import os
import jwt
import requests
from datetime import datetime, timezone
import auth
import graphql_helper

# AUTH_URL = "https://api.devii.io/auth"
ROLES_PBAC_URL = "https://apidev.devii.io/roles_pbac"
ANON_URL = "https://apidev.devii.io/anonauth"
QUERY_URL = "https://apidev.devii.io/query"

# Anonymous logins must be enabled in the tenant settings - see https://docs.devii.io/docs/devii-basics/anonauth_endpoint

def anon_login(tenantid):
    """Log in as an anonymous user before you can have a user sign up"""
    anon_payload = {"tenantid": int(tenantid)}
    anon_login = requests.post(ANON_URL, json=anon_payload)
    print("anon_login: ", anon_login.json().get("access_token"))
    print(type(tenantid))
    response = requests.post(ANON_URL, json=anon_payload)

    # Check for a successful response, if status code is 200 parse the JSON response
    if response.status_code == 200:
        print("success")
        json_response = response.json()
        # Extract the access token
        access_token = json_response.get("access_token")
        return access_token 
    else: 
        print("error in anon_login: ", response.status_code)
        print("response from anon_login: ", response.text)
        return response.status_code


def create_user(data, access_token):
    """Create a user for tenant"""
    create_new_user = """
        mutation create_user($i: roleInput){
            create_role(input: $i){
                name
                login
                tenantid
                roleid
            }
            }
    """ 
    print("data: ", data)   
    print("creating new user")
    # the variables will be retrieved from a form the user will submit
    variables = {"i": data}
    print("variables: ", variables)

    new_user_payload = {"query": create_new_user, "variables": variables}

    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

    new_user = requests.post(ROLES_PBAC_URL, headers=headers, json=new_user_payload)
    print("new_user: ", new_user.json())

    print("new user access token: ", access_token)

    my_new_user = new_user.json()["data"]["create_role"]

    print("my_new_user: ", new_user.status_code)

    if new_user.status_code == 200:
        create_devii_user(my_new_user, access_token)
        print("User created successfully")

    return my_new_user


def create_devii_user(my_new_user, access_token):
    """Return a user from a sign up"""

    roleid = my_new_user["roleid"]
    print("roleid: ", roleid)
    name = my_new_user["name"]
    login = my_new_user["login"]

    return_user_mutation = """
        mutation create_devii_user($i: devii_usersInput){
        create_devii_users(input: $i){
        userid
        name
        devii_roleid
        email
        }
    }
    """

    variables = {"i": {"name": name, "email": login, "devii_roleid": roleid}}

    print("variables: ", variables)
    
    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

    payload = {"query": return_user_mutation, "variables": variables}

    # the query will always receive a return response of data in the same shape as the query
    response = requests.post(QUERY_URL, headers=headers, json=payload)

    print("response: ", response.json())

    # the response is returned in json form
    return response.json()

    
