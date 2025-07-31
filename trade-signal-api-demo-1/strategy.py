import json
import os
import time
from datetime import datetime, timedelta
from collections import deque
from trade_signals import TradeSignals

EMA = 3
MAX_NUMBER_OF_CANDLES = 60
QTY = 10
TRADING_SYMBOL = "BTCUSD.P"


class Strategy:
    def __init__(self, underlying : str, main_url : str, order_url : str, access_token :str, 
                 broker_id : str, token : dict, persist_file="candle_store.txt"):
        self.candles = deque(maxlen=MAX_NUMBER_OF_CANDLES)
        self.underlying = underlying
        self.last_timestamp = None
        self.persist_file = persist_file
        self.last_dump_time = time.time()
        self.tradeflag = 0
        self.trade_signal_tag = None
        self.open_trades = []

        self.trade = TradeSignals(main_url=main_url, order_url=order_url, 
                                  access_token=access_token, broker_id=broker_id, token=token )

        self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.persist_file):
            with open(self.persist_file, "r") as f:
                try:
                    lines = f.readlines()
                    for line in lines:
                        data = json.loads(line.strip())
                        self.candles.append(data)
                    if self.candles:
                        self.last_timestamp = datetime.fromisoformat(self.candles[-1]["timestamp"])
                    print(f"Loaded {len(self.candles)} candles from file.")
                except Exception as e:
                    print(f"Failed to load from file: {e}")

    def save_to_file(self):
        with open(self.persist_file, "w") as f:
            for candle in self.candles:
                f.write(json.dumps(candle) + "\n")
        print(f"{len(self.candles)} candles saved at {datetime.now().isoformat()}")

    def calculate_ema(self, period : int):
        if len(self.candles) < period:
            return None
        prices = [c["close"] for c in self.candles]
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        return round(ema, 2)
    
    def check_condition(self): 
        for candle in self.candles:

            if candle["timestamp"] and candle['ema']: 
                
                print()
                print("Timestamp: ", candle['timestamp'])
                print("Candle: ", candle)
                print("Entry Condition Met: ", candle["ema"] < candle["close"] and self.tradeflag == 0)
                print("Exit Condition Met: ", candle["ema"] > candle["close"] and self.tradeflag == 1)
                print()

                if candle["ema"] < candle["close"] and self.tradeflag == 0:
                    trade = str(TRADING_SYMBOL + " " + "buy" + " " + str(QTY) )
                    create_trade_signal_payload = {
                        "signal_name": "Sample Signal - 1",
                        "signal_type": "paper",
                        "brokers": [] 
                    }

                    if not self.trade_signal_tag:
                        self.trade_signal_tag = self.trade.create_trade_signals(create_trade_signal_payload)

                        if not self.trade_signal_tag:
                            raise Exception(f"Failed to create signal can't move forward")
                        
                    trade_completed = self.trade.send_trade_signals(tag=self.trade_signal_tag, payload=trade, execution_type='paper')
                    
                    if trade_completed:
                        self.tradeflag = 1
                        self.open_trades = trade

                if candle["ema"] > candle["close"] and self.tradeflag == 1:
                    trade = TRADING_SYMBOL + " " + "sell" + " " + str(QTY)
                    create_trade_signal_payload = {
                        "signal_name": "Sample Signal - 1",
                        "signal_type": "paper",
                        "brokers": [] 
                    }

                    if not self.trade_signal_tag:
                        self.trade_signal_tag = self.trade.create_trade_signals(create_trade_signal_payload)

                        if not self.trade_signal_tag:
                            raise Exception(f"Failed to create signal can't move forward")
                        
                    trade_completed = self.trade.send_trade_signals(tag=self.trade_signal_tag, payload=trade, execution_type='paper')
                    
                    if trade_completed:
                        self.tradeflag = 0
                        self.open_trades = False

    def handle_price_update(self, raw_message):
        try:
            message = json.loads(raw_message)
            fut_data = message.get("candle", {}).get(self.underlying, {}).get("FUT", {})

            for contract_key, candle in fut_data.items():
                if contract_key is None or contract_key == "null":
                    timestamp = candle.get("timestamp")
                    if not timestamp:
                        return

                    dt = datetime.fromisoformat(timestamp)

                    # Check for missing candle
                    if self.last_timestamp and (dt - self.last_timestamp) > timedelta(minutes=1):
                        print(f"[WARNING] Skipped candle. Last: {self.last_timestamp}, New: {dt}")

                    ema = self.calculate_ema(EMA)
                    ohlc = {
                        "timestamp": timestamp,
                        "open": candle["open"],
                        "high": candle["high"],
                        "low": candle["low"],
                        "close": candle["close"],
                        "ema": ema,
                    }

                    self.candles.append(ohlc)
                    self.last_timestamp = dt

                    self.check_condition()

                    # Save to file every 5 minutes
                    if time.time() - self.last_dump_time >= 300:
                        self.save_to_file()
                        self.last_dump_time = time.time()

        except Exception as e:
            print(f"[ERROR] Failed to process message: {e}")


        
