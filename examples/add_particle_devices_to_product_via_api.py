import sys
sys.path.append("..")
from datacake_graphql_client import DatacakeGraphQlClient

# Some examples

if __name__ == '__main__':

    DATACAKE_GRAPHQL_API = "https://api.datacake.co/graphql/"
    DATACAKE_TOKEN = "putyourdatacaketokenhere"

    datacake_graphql_client = DatacakeGraphQlClient(
        url=DATACAKE_GRAPHQL_API,
        token=DATACAKE_TOKEN
    )    

    # Get list of products for token

    # NOTE: This command lists all products for give token
    # Please don't run this with your personal api token as
    # that would return lots of products probably...
    r = datacake_graphql_client.get_products_for_token()
    print(r)

    # You can use the following command to add devices to an existing product
    # This command requires:
    # - Product UUID
    # You can use the previous query to retrieve the product UUID
    r = datacake_graphql_client.add_particle_devices_into_product(
        workspace="23ca644f-1ce1-dead-beef-dc6c9915f964", 
        plan="put-your-plan-here", # Put "free", "light", "standard", "plus" if you have no custom plan 
        plan_code="CODE IF YOU HAVE SOME", # Put a code if you have one (enterprise customer, promo, etc.)
        product="5c2700ee-f046-4810-ac01-5d7aa70aff87", # the individual product id
        particleProduct="",
        particleAccount="",
        devices=[
            {
                "name":"Device 01",
                "particleId":"particle device id",
                "location":"A basic location description", # Optional
                "tags":["group-a","group-b"], # Optional
                "claimCode":"123456", # Optional
                "claimSerialNumber":"mycustomserial001" # Optional
            }
        ]
    )
    print(r)