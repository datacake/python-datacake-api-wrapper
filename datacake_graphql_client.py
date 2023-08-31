import requests
import json

class DatacakeGraphQlClient:
    def __init__(self, url, token):
        self.url = url
        self.headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}

    def run(self, query, variables=None):
        data = {"query": query, "variables": variables}
        response = requests.post(self.url, headers=self.headers, json=data)
        return response.json()
    
    def add_device_into_product(self, workspace, devices, plan_code, plan, product):
        query = """
        mutation ($input: CreateApiDevicesInputType!) {
          createApiDevices(input: $input) {
            ok
            error
          }
        }
        """
        variables = {
            "input": {
              "workspace":workspace,
              "plan":plan,
              "planCode":plan_code,
              "devices": devices,
              "productKind":"EXISTING",
              "existingProduct":product
            }
        }
        return self.run(query, variables)
    
    def update_device(self, device, name, claim_code):
        query = """
        mutation ($device: String!, $input: UpdateDeviceInputType) {
          updateDevice(deviceId: $device, input: $input) {
            ok
          }
        }
        """
        variables = {
            "device": device,
            "input": {
              "verboseName":name,
              "claimCode":claim_code,
            }
        }
        return self.run(query, variables)    
    
    def set_claiming_on_device(self, device, claiming=True):
        query = """
        mutation ($device: String!, $input: UpdateDeviceInputType) {
          updateDevice(deviceId: $device, input: $input) {
            ok
          }
        }
        """
        variables = {
            "device": device,
            "input": {
              "canBeClaimed":claiming,
            }
        }
        return self.run(query, variables)

    def create_device_public_link(self, device, dashboard_password):
        query = """
        mutation ($device: String!, $input: DevicePublicLinkInputType!) {
          createDevicePublicLink(device: $device, input: $input) {
            ok
          }
        }
        """
        variables = {
            "device": device,
            "input": {
                "token": dashboard_password,
                "mode": "READ"
            }
        }
        return self.run(query, variables)
    
    def claim_device_into_workspace(self, device, workspace):
        query = """
        mutation ($device: String, $workspace: String!){
          claimDeviceIntoWorkspace(deviceId: $device, workspaceId: $workspace) {
            ok
          }
        }
        """
        variables = {
            "device": device,
            "workspace": workspace
        }
        return self.run(query, variables)

    def get_device_public_link(self, deviceId):
        query = """
        query ($deviceId: String!) {
        device(deviceId: $deviceId) {
            publicLinks {
            id
            }
        }
        }
        """
        variables = {
            "deviceId": deviceId,
        }
        result = self.run(query, variables)
        # post-processing step
        base_url = "https://app.datacake.de/pd/"
        for link in result['data']['device']['publicLinks']:
            link['id'] = base_url + link['id']
        return result['data']['device']['publicLinks'][0]['id']


    def get_all_devices(self, inWorkspace):
        query = """
        query ($inWorkspace: String!) {
        allDevices(inWorkspace: $inWorkspace) {
            id,
            verboseName,
            serialNumber,
            publicLinks {
            id
            }
        }
        }
        """
        variables = {
            "inWorkspace": inWorkspace,
        }
        result = self.run(query, variables)
        # post-processing step
        base_url = "https://app.datacake.de/pd/"
        for device in result['data']['allDevices']:
            device['publicLinks'] = [base_url + link['id'] for link in device['publicLinks']]
        return result

    def get_products_for_token(self):
        query = """
        query {
          allProducts {
            name
            slug
            id
            hardware
          }
        }
        """
        variables = {}
        return self.run(query, variables)

    def get_devices_by_name(self, searchName):
        query = """
        query ($searchName: String!) {
          allDevices(searchName: $searchName) {
            verboseName,
            serialNumber,
            publicLinks {
              id
            }
          }
        }
        """
        variables = {
            "searchName": searchName,
        }
        return self.run(query, variables)
    

if __name__ == '__main__':
    
  DATACAKE_GRAPHQL_API = "https://api.datacake.co/graphql/"
  DATACAKE_TOKEN = "putyourdatacaketokenhere"

  datacake_graphql_client = DatacakeGraphQlClient(
      url=DATACAKE_GRAPHQL_API,
      token=DATACAKE_TOKEN
  )    

  # # Enable claiming on device

  # datacake_graphql_client.set_claiming_on_device(
  #     device="datacake-device-id",
  #     claiming=True
  # )

  # # Claim device into any workspace

  # datacake_graphql_client.claim_device_into_workspace(
  #     device="datacake-device-id",
  #     workspace="datacake-workspace-id"
  # )

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
  r = datacake_graphql_client.add_device_into_product(
      workspace="23ca644f-1ce1-dead-beef-dc6c9915f964", 
      plan="put-your-plan-here", # Put "free", "light", "standard", "plus" if you have no custom plan 
      plan_code="CODE IF YOU HAVE SOME", # Put a code if you have one (enterprise customer, promo, etc.)
      product="5c2700ee-f046-4810-ac01-5d7aa70aff87", # the individual product id
      devices=[
        {
          "name":"My Device 01",
          "serial":"mydevice01",
          "location":"Somewhere in the Cloud",
          "tags":["a","b"],
          "claimCode":"abcdef123456"
        },
        {
          "name":"My Device 02",
          "serial":"mydevice02",
          "location":"Somewhere in the Cloud",
          "tags":["a","b"],
          "claimCode":"123456abcdef"
        },
      ]
  )
  print(r)

  # List all devices

  r = datacake_graphql_client.get_all_devices(
      inWorkspace="23c16441-1ca1-456f-8aa8-dc6c330df964"
  )
  print(r)