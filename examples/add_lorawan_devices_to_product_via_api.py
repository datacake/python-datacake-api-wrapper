from datacake_graphql_client import DatacakeGraphQlClient

# Version: LoRaWAN Device
# Example on how to add a bunch of devices to an existing LoRaWAN Product

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

    # Add a bunch of API device to API product

    # You can use the following command to add devices to an existing product
    # This command requires:
    # - Product UUID
    # You can use the previous query to retrieve the product UUID
    r = datacake_graphql_client.add_lorawan_devices_into_product(
        workspace="23ca644f-1ce1-dead-beef-dc6c9915f964", 
        plan="put-your-plan-here", # Put "free", "light", "standard", "plus" if you have no custom plan 
        plan_code="CODE IF YOU HAVE SOME", # Put a code if you have one (enterprise customer, promo, etc.)
        product="5c2700ee-f046-4810-ac01-5d7aa70aff87", # the individual product id
        devices=[
        {
            "name":"My Device 01",
            "devEui":"a72647f5900b1635",
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
            "devEui":"a72647f5900b1634",
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