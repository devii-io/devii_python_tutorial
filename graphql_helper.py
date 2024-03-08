"""helper functions for GraphQL queries and mutations"""

import requests
import auth


# This URL is for both queries and mutations within the Devii enivorment
QUERY_URL = "https://api.devii.io/query"


def execute_graphql_query(query, variables=None):
    """helper function for all queries and mutations"""
    # This will load the query or mutation and variable if there are any into the GraphQL query or mutation
    payload = {"query": query, "variables": variables}

    # the query will always recieve a return response of data in the same shape as the query
    response = requests.post(QUERY_URL, headers=auth.headers, json=payload)

    # the response is returned in json form
    return response.json()


def get_list_data():
    # query that will be sent to Devii to retrieve all the data from the list and item tables
    list_name_query = """
    {
        list {
            listid
            listname
            statusid
            item_collection {
                itemid
                itemname
                statusid
            }
        }
    }
    """
    # creates the payload that will be used by Devii to return the data
    list_name_payload = {"query": list_name_query, "variables": {}}

    # sends the query payload and authorization token to devii
    list_name_response = requests.post(
        QUERY_URL, headers=auth.headers, json=list_name_payload
    )

    # returns the response from GraphQL in a json nested dictionary, it retrieves the values from the keys, data and list
    return list_name_response.json()["data"]["list"]

def get_status_name():
    query_status_name="""
        {
            status_value{
                statusid
                statusname
            }
        }
    """

    # creates the payload that will be used by Devii to return the data
    status_name_payload = {"query": query_status_name, "variables": {}}

    # sends the query payload and authorization token to devii
    status_name_response = requests.post(
        QUERY_URL, headers=auth.headers, json=status_name_payload
    )

    # returns the response from GraphQL in a json nested dictionary, it retrieves the values from the keys, data and status
    return status_name_response.json()["data"]["status_value"]

def add_item(item_name, list_id, status_id):
    # to add an item to the item table with a listid FK and statusid FK
    add_item_mutation = """
        mutation ($i: itemInput){
            create_item(input: $i){
                itemid
                itemname
                status_value {
                    statusname
                }
                list {
                    listname
                }
            }
        }
    """
    # the variables will be retrieved from a form the user will submit
    variables = {"i": {"itemname": item_name, "listid": int(list_id), "statusid": int(status_id)}}

    # the GraphQL mutation run by the helper function
    return execute_graphql_query(add_item_mutation, variables)


# Each one of the following functions has the same format as the add_item

def add_list(listname, status_id):
    add_list_mutation = """
    mutation($i:listInput){
        create_list(input:$i){
            listid
            listname
            status_value{
                statusid
                statusname
            }
        }
    }
    """
    variables = {"i": {"listname": listname, "statusid": int(status_id)}}
    return execute_graphql_query(add_list_mutation, variables)

# Editing items requires identifying the Primary Key of the item you want to edit/change
# In this case the PK is the itemid that will be the varible $j 
# The varible $i will be the changes to the item


def edit_item(itemid, new_name, list_id, status_id):
    edit_item_mutation = """
        mutation ($i: itemInput, $j: ID!) {
            update_item(input: $i, itemid: $j) {
                itemid 
                itemname
                status_value{
                    statusid
                    statusname
                }
                list {
                    listid
                    listname
                }
            }
        }
        """

    variables = {
        "j": itemid, 
        "i": {"itemname": new_name, "listid": int(list_id), "statusid": int(status_id)},
    }
    return execute_graphql_query(edit_item_mutation, variables)

# Each one of the following edit functions has the same format as the edit_item

def edit_list(listid, new_list_name, status_id):
    edit_list_mutation = """
    mutation($i:listInput, $j:ID!){
        update_list(input:$i, listid: $j){
            listid
            listname
            status_value{
                statusname
                statusid
            }
        }
    }
    """

    variables = {"j": int(listid), "i": {"listname": new_list_name, "statusid": int(status_id)}}
    return execute_graphql_query(edit_list_mutation, variables)

# Deleting objects will only require the Primary Key of the object to be deleted

def delete_item(itemid):
    delete_item_mutation = """
    mutation($i:ID!){
        delete_item(itemid:$i){
            itemid
            itemname
        }
    }
    """
    variables = {"i": itemid}
    return execute_graphql_query(delete_item_mutation, variables)

# Each one of the following delete functions has the same format as the delete_item

def delete_list(listid):
    delete_list_mutation = """
    mutation($i:ID!){
        delete_list(listid:$i){
            listid
            listname
        }
    }
    """
    variables = {"i": listid}
    return execute_graphql_query(delete_list_mutation, variables)