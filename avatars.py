import auth
import graphql_helper

# PBAC_URL = "https://api.devii.io/roles_pbac"
PBAC_URL = "https://apidev.devii.io/roles_pbac"



# def set_table(table, column):
#     """Set table for file handling"""
#     set_table_mutation = """
#     mutation set_table($table: String!, $column: String!) {
#         set_file_table(table: $table, column: $column) {
#             table
#             column
#         }
#     }
#     """
#     variables = {"table": table, "column": column}
#     return graphql_helper.execute_graphql_query(set_table_mutation, variables)