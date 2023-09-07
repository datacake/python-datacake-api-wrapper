import sys
sys.path.append("..")
from datacake_graphql_client import DatacakeGraphQlClient

# Version: LoRaWAN Device
# Example on how to add a bunch of devices to an existing LoRaWAN Product

if __name__ == '__main__':

    DATACAKE_GRAPHQL_API = "https://api.datacake.co/graphql/"
    DATACAKE_TOKEN = "yourdatacaketoken"

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

    # Add a bunch of API device to API product

    # You can use the following command to add devices to an existing product
    # This command requires:
    # - Product UUID
    # You can use the previous query to retrieve the product UUID
    r = datacake_graphql_client.add_lorawan_devices_into_product(
        workspace="f63af019-dead-beef-b1bc-35ff546fdead", 
        plan="free", # Put "free", "light", "standard", "plus" if you have no custom plan 
        plan_code="", # Put a code if you have one (enterprise customer, promo, etc.)
        product="your-datacake-product-uuid", # the individual product id
        network_server="TTI", # put "TTI" or "Loriot", etc...
        devices=[
        {
            "name":"My Device 01",
            "devEui":"a726dead900b1635",
            "location":"Somewhere in the Cloud",
            "tags":["a","b"],
            "claimCode":"abcdef123456",
            # "ttiDevId": "eui-a72647f5900b1635" # Optional, when using TTS + Downlinks
            # "deviceClass": "A" # Optional, set Class A or C for managed LNS
            # "appeui": "a72647f5900b1635" # Optional, only for managed LNSs
            # "appkey": "a72647f5900b1635a72647f5900b1635" # Optional, only for managed LNSs
        },
        {
            "name":"My Device 02",
            "devEui":"a72647dead0b1634",
            "location":"Somewhere in the Cloud",
            "tags":["a","b"],
            "claimCode":"abcdef123423",
            # "ttiDevId": "eui-a72647f5900b1623" # Optional, when using TTS + Downlinks
            # "deviceClass": "A" # Optional, set Class A or C for managed LNS
            # "appeui": "a72647f5900b1623" # Optional, only for managed LNSs
            # "appkey": "a72647f5900b1635a72647f5900b1635" # Optional, only for managed LNSs
        },
        ]
    )
    print(r)