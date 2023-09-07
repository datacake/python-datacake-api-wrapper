import sys
sys.path.append("..")
from datacake_graphql_client import DatacakeGraphQlClient

# Some examples

if __name__ == '__main__':
    
    DATACAKE_GRAPHQL_API = "https://api.datacake.co/graphql/"
    DATACAKE_TOKEN = ""

    datacake_graphql_client = DatacakeGraphQlClient(
        url=DATACAKE_GRAPHQL_API,
        token=DATACAKE_TOKEN
    )    

    # Login

    response = datacake_graphql_client.login(
        email="user@email.com",
        password="userpassword"
    )
    
    login_status = response['data']['login']['ok']
    token = response['data']['login']['token']

    # Check if login was okay

    if login_status: 
        print("Login successful! Token:", token)
    else:
        print("Login failed!")
        quit()

    # Reinit wrapper to store token

    datacake_graphql_client = DatacakeGraphQlClient(
        url=DATACAKE_GRAPHQL_API,
        token=token
    )   

    # List all devices

    r = datacake_graphql_client.get_all_devices(
        inWorkspace="23c16441-neef-dead-8aa8-dc6c330df964"
    )

    print(r)
 