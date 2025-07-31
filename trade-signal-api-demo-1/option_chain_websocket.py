import json
import ssl
from websocket import WebSocketApp

class OptionChainWebSocketClient:
    def __init__(self, url, jwt_token, subscription_payload, on_data_callback=None):
        self.url = url
        self.jwt_token = jwt_token
        self.subscription_payload = subscription_payload
        self.ws = None
        self.on_data_callback = on_data_callback

    def on_message(self, ws, message):
        print(message)
        if self.on_data_callback:
            self.on_data_callback(message) 

    def on_open(self, ws):
        print("WebSocket connection opened, sending subscription…")
        ws.send(json.dumps(self.subscription_payload))
        print("Subscription sent")

    def on_close(self, ws, *args):
        print("WebSocket connection closed:")

    def on_error(self, ws, error):
        print("[ERROR]", error)

    def start(self):
        ssl_context = ssl._create_unverified_context()

        self.ws = WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            header=[f"Cookie: access_token_cookie={self.jwt_token}"],
        )
        print("Starting WebSocket loop")
        self.ws.run_forever(sslopt={"context": ssl_context})
