ROGGER INTELLIGENCE TERMINAL

This is the production-oriented UI shell:
- browser terminal
- TradingView embedded charts
- watchlist
- scanner/AI analysis panel
- market pulse
- news intelligence
- options setup
- TradingView webhook backend
- Pine signal layer

Run:
  pip install flask flask-cors
  python backend.py
Open index.html.

To activate automatic TradingView signals, publish the backend on a public HTTPS server and set TradingView Alert Webhook URL to:
https://YOUR-DOMAIN/api/tradingview

Important:
TradingView chart embedding does not itself expose a generic options-chain API to this page. Real option bid/ask/IV/Greeks/OI still require a permitted options data source. The UI deliberately shows WAIT/— until real data is connected.
