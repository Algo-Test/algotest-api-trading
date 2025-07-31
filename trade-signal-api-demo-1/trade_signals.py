import requests

class TradeSignals:
    def __init__(self, main_url : str, order_url : str, access_token :str, 
                 broker_id : str, token : dict):
        self.main_url = main_url
        self.order_url = order_url
        self.access_token = access_token
        self.broker_id = broker_id

        self.headers = {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN-ACCESS": token.get('X-CSRF-TOKEN-ACCESS'),
            "Cookie": f"access_token_cookie={token.get('Authorization')}"
        }

    def create_trade_signals(self, payload : dict):
        response = requests.post(f"{self.main_url}/trade-signal/create", json=payload, headers=self.headers)

        if response.status_code == 200:
            content = response.json() 
            print(f"Signal created successfully: {content}")
            return content.get("id")
        else:
            raise Exception(f"Failed to create signal {response.status_code}, {response.text}")
        
    def send_trade_signals(self, tag : str, payload: dict, execution_type: str = "paper"):
        if execution_type == "paper":
            url = f"{self.order_url}/webhook/tv/tk-trade?token={self.access_token}&tag={tag}"
        elif execution_type == "live":
            url = f"{self.order_url}/webhook/tv/tk-trade?token={self.access_token}&tag={tag}&brokers={self.broker_id}"
        
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            print(f"Signal sent successfully: {response.json()}")
            return True
        else:
            raise Exception(f"Failed to Send Signal {response.status_code}, {response.text}")
            


        



        