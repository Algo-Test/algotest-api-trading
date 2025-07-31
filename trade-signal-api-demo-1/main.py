from algotest_login import AlgoTestClient
from contracts_fetch import ContractFetcher
from option_chain_websocket import OptionChainWebSocketClient
from strategy import Strategy
from dotenv import load_dotenv
import os

load_dotenv()


PHONE_NUMBER = os.getenv("PHONE_NUMBER")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BROKER_ID = os.getenv("BROKER_ID")

UNDERLYING = "DELTA_BTCUSD"
PRICES_URL = "https://prices.algotest.in"
MAIN_URL = "https://api.algotest.in"
ORDERS_URL = "https://orders.algotest.in"
OPTION_CHAIN_WS = "wss://prices.algotest.in/updates?structured=true"


client = AlgoTestClient(phone_number=PHONE_NUMBER, main_url=MAIN_URL)
contracts = ContractFetcher(token=client.get_tokens(), underlying=UNDERLYING, 
                            prices_url=PRICES_URL)

subscription_message = {
    "msg": {
        "type": "subscribe",
        "datatypes": ["candle"],
        "underlyings": [
            {
                "underlying": UNDERLYING,
                "cash": False,
                "options": [],
                "futures": [],
            }
        ],
        "tokens": ["DELTA_27"],
    }
}

strategy = Strategy(underlying=UNDERLYING, main_url=MAIN_URL, order_url=ORDERS_URL, 
                    access_token=ACCESS_TOKEN, broker_id=BROKER_ID, token=client.get_tokens())

ws_client = OptionChainWebSocketClient(OPTION_CHAIN_WS, client.jwt_token, 
                                       subscription_message, on_data_callback=strategy.handle_price_update)
ws_client.start()



