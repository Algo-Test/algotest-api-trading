
# AlgoTest API Trading Examples - 1

This example demonstrates how to build and run trading strategies using the AlgoTest API. It includes sample code for login, fetching option contracts, subscribing to live market data via WebSocket, strategy logic, and trade signal generation — everything you need to get started with automated crypto derivatives trading on AlgoTest.

## File Overview

### 1. main.py
Entry point of the script. It orchestrates:
- User authentication
- Contract data fetch
- WebSocket subscription for live option chain updates
- Strategy execution on live data

### 2. algotest_login.py
Handles login to the AlgoTest API.
- Accepts phone number and password (from `.env`)
- Stores session and JWT tokens
- Returns headers used for authenticated requests

### 3. contracts_fetch.py
Fetches available option contracts for a given underlying (like `DELTA_BTCUSD`).
- Makes authenticated GET requests to AlgoTest prices API
- Parses and stores the contracts available for trading

### 4. option_chain_websocket.py
Maintains a live WebSocket connection to AlgoTest's option chain data.
- Sends a structured subscription request
- Receives real-time candle updates
- Passes each new message to the strategy engine

### 5. strategy.py
Contains the core strategy logic.
- Maintains a sliding window (`deque`) of candles (60 max)
- Computes a simple EMA on the latest candles
- Generates trade signals when entry/exit conditions are met
- Interfaces with `trade_signals.py` to fire trade instructions
- Also persists candle data locally for recovery

### 6. trade_signals.py
Handles trade signal creation using AlgoTest’s `/trade-signal/create` endpoint.
- Sends signals with proper headers and auth cookies
- Abstracts away low-level request logic from the strategy

## How It Works

1. Environment Setup (`.env`)
   You'll need to define:
   ```
   PHONE_NUMBER=your_registered_number
   PASSWORD=your_password
   ACCESS_TOKEN=your_algo_test_access_token
   BROKER_ID=your_broker_id
   ```

2. Login
   `AlgoTestClient` (in `algotest_login.py`) logs in using your phone and password, and returns the headers with required CSRF and session tokens.

3. Fetch Contracts
   `ContractFetcher` retrieves available contracts (e.g., BTCUSD futures) using your auth headers.

4. Subscribe to Live Data
   `OptionChainWebSocketClient` connects to AlgoTest’s live prices feed and subscribes to the instrument's candle data.

5. Run Strategy
   Every new candle received is passed to a `Strategy` object. If conditions match (like EMA crossover, etc.), it:
   - Fires a trade signal via `TradeSignals.create_trade_signals()`
   - Logs and tracks open trades
   - Ensures no duplicate or rapid-fire orders

## Requirements

Install dependencies using:

```
pip install -r requirements.txt
```

Dependencies include:
- requests
- websocket-client
- python-dotenv
- gevent
- etc.

## Strategy Logic

The current strategy (inside `strategy.py`) is a simple EMA-based entry:
- Stores 60 candles in memory
- Calculates EMA over the last 3 candles
- If price breaks above/below EMA and no open trade exists:
  - Sends a signal to AlgoTest for execution

You can easily modify this logic to:
- Add SL/Target/TSL
- Use RSI, SuperTrend, Volume, or custom indicators
- Run multiple strategies in parallel

## Run the Code

1. Fill your `.env` file
2. Run the main script:

```
python main.py
```

You’ll see logs for:
- Successful login
- Contract fetch summary
- WebSocket candle updates
- Strategy entries and signals created

## License
This project is licensed under the MIT License.

## Support

Need help or want to contribute?

- Join the AlgoTest Telegram Community: https://t.me/algotest_in
- Email Contact: https://algotest.in/contact

## Disclaimer

This code is for educational and development purposes only. Trading in derivatives involves risk. Always test your strategies in forward test mode before going live.


Made by the AlgoTest Team
