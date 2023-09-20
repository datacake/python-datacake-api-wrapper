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
    
    def login(self, email, password):
        query = """
        mutation LogIn($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                ok
                token
            }
        }
        """
        variables = {
            "email": email,
            "password": password
        }
        return self.run(query, variables)
    
    def signup(self, firstName, lastName, email, password, companyName, confirmPassword, agreeToTerms, language, brand, captchaToken):
        query = """
        mutation Signup($email: String!, $password: String!, $firstName: String!, $lastName: String!, $brand: String, $companyName: String, $language: String, $captchaToken: String!) {
            signup(
                email: $email
                password: $password
                firstName: $firstName
                lastName: $lastName
                brand: $brand
                firstWorkspaceName: $companyName
                language: $language
                captchaToken: $captchaToken
            ) {
                ok
                token
                __typename
            }
        }
        """
        variables = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password": password,
            "companyName": companyName,
            "language": language,
            "brand": brand,
            "captchaToken": captchaToken
        }
        
        # Ensure confirmPassword and agreeToTerms are checked if necessary
        if password != confirmPassword:
            raise ValueError("Password and Confirm Password do not match")
        if not agreeToTerms:
            raise ValueError("You must agree to the terms to proceed")

        return self.run(query, variables)

    def add_particle_devices_into_product(self, workspace, devices, plan_code, plan, datacakeProduct, particleProduct, particleAccount):
        query = """
        mutation ($input: CreateParticleDevicesInputType!) {
          createParticleDevices(input: $input) {
            ok
            error
            devices {
              id
            }
          }
        }
        """
        variables = {
            "input": {
              "workspace":workspace,
              "plan":plan,
              "planCode":plan_code,
              "devices": devices,
              "product":"EXISTING",
              "existingProduct": datacakeProduct,
              "particleProduct": particleProduct,
              "particleAccount": particleAccount,
            }
        }
        return self.run(query, variables)

    
    def add_devices_into_product(self, workspace, devices, plan_code, plan, product):
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
    
    def add_lorawan_devices_into_product(self, workspace, devices, plan_code, plan, product, network_server):
        query = """
        mutation ($input: CreateLoraDevicesInputType!) {
          createLoraDevices(input: $input) {
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
              "productKind":"EXISTING",
              "existingProduct":product,
              "devices": devices,
              "networkServer":network_server
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