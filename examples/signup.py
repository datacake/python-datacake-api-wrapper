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

    response = datacake_graphql_client.signup(
        firstName="Simmi",
        lastName="Tada",
        email="simon+tada@datacake.de",
        password="Tada2020!",
        confirmPassword="Tada2020!",
        agreeToTerms=True,
        language="en",
        brand="datacake",
        captchaToken="123",
        companyName=""
    )

    print(response)