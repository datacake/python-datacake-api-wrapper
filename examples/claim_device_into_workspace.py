import sys
sys.path.append("..")
from datacake_graphql_client import DatacakeGraphQlClient

if __name__ == '__main__':

    DATACAKE_GRAPHQL_API = "https://api.datacake.co/graphql/"
    DATACAKE_TOKEN = "putyourdatacaketokenhere"

    datacake_graphql_client = DatacakeGraphQlClient(
        url=DATACAKE_GRAPHQL_API,
        token=DATACAKE_TOKEN
    )    

    # Step 1: Enable claiming on device

    datacake_graphql_client.set_claiming_on_device(
        device="datacake-device-id",
        claiming=True
    )

    # Step 2: Claim device into any workspace

    datacake_graphql_client.claim_device_into_workspace(
        device="datacake-device-id",
        workspace="datacake-workspace-id"
    )