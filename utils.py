'''Utilities module'''

import requests
import auth
import json
import os

# PBAC_URL = "https://api.devii.io/roles_pbac"
PBAC_URL = "https://apidev.devii.io/roles_pbac"

OLD_DICT_FILE = 'old_dict.json' # This file will be used to store the tables and column data prior to introspection

def load_old_dict():
    if os.path.exists(OLD_DICT_FILE):
        with open(OLD_DICT_FILE, "r") as file:
            return json.load(file)
    else:
        return {}


def save_dict(old_dict):
    with open(OLD_DICT_FILE, 'w') as file:
        json.dump(old_dict, file)


def compare(old_dict, new_dict):
    changes_detected = False
    message = ''

    # Check for added and removed tables: 
    # to detect new they must be whitelisted first and deleted tables must be removed from whitelist
    added_tables = set(new_dict.keys()) - set(old_dict.keys())
    removed_tables = set(old_dict.keys()) - set(new_dict.keys())

    if added_tables or removed_tables:
        changes_detected = True
        if added_tables:
            message += f"Added tables: {added_tables}\n"
            for added_table in added_tables:
                message += f"  Fields in {added_table}: {new_dict[added_table]}\n"
        if removed_tables:
            message += f"Removed tables: {removed_tables}\n"


    for tabname, old_fields in old_dict.items():
        new_fields = new_dict.get(tabname, [])
        added_fields = set(new_fields) - set(old_fields)
        removed_fields = set(old_fields) - set(new_fields)

        if added_fields or removed_fields:
            changes_detected = True
            message += f"Changes in {tabname}: \n"
            if added_fields:
                message += f" Added fields: {added_fields}"
            if removed_fields:
                message += f" Removed fields: {removed_fields}"


    if not changes_detected:
        message += 'No changes detected'

    return message


def devii_introspect():
    old_dict = load_old_dict()

    introspect = """{
        Utility {introspect}
        }
    """

    util_introspect = {"query": introspect, "variables": {}}
    response = requests.post(PBAC_URL, headers=auth.headers, json=util_introspect)

    data = response.json()["data"]["Utility"]["introspect"]['json']['__schema']

    qtype = [t for t in data['types'] if t['name']=='Query'][0]

    tabnames = [field['name']for field in qtype['fields'] if field['name'] != 'Aggregates']

    new_dict = {}
    for tabname in tabnames:
        fnames = next((x for x in data['types'] if x['name'] == tabname), None)
        if fnames:
            cnames = [field['name'] for field in fnames['fields']]
            new_dict[tabname] = cnames

    message = compare(old_dict, new_dict)

    # Clear and update the old dictionary with new data
    old_dict.clear()
    old_dict.update(new_dict)

    # Save the updated old dictionary to the file
    save_dict(old_dict)

    return message

# devii_introspect()