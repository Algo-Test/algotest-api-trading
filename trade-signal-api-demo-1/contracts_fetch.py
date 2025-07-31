import requests

class ContractFetcher:
    def __init__(self, token, underlying : str, prices_url : str):
        self.underlying = underlying
        self.contracts_url = f"{prices_url}/contracts?underlying={underlying}"
        self.contracts = None
        self.contract_count = 0

        self.headers = {"Content-Type": "application/json"}
        self.headers.update(token)

        self.fetch_contracts()

    def fetch_contracts(self):
        response = requests.get(self.contracts_url, headers=self.headers)

        if response.status_code == 200:
            self.contracts = response.json()
            self.contract_count = len(self.contracts)
        else:
            raise Exception(f"Failed to fetch contracts: {response.status_code}, {response.text}")

