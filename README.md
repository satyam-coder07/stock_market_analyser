# 📈 StockMarket AI (Phidata + Gemini)

I built this project to automate my morning market research. It uses a team of specialized AI agents to scan the news and technicals so I don't have to.

### 🛠 How I Built It
* **Multi-Agent Team:** I used Phidata's `Agent` class to separate concerns. One agent only handles technical charts (yFinance), while another scans the web (DuckDuckGo).
* **Gemini 2.5 Flash:** Chosen for its fast inference speeds and low latency—crucial for real-time data analysis.
* **The "Brain":** A leader agent that takes inputs from the specialists and tries to find contradictions (e.g., "Bullish fundamentals but Bearish RSI").

### 🚧 Challenges I Overcame
* **Dependency Hell:** Had a major conflict between `pyparsing` and `httplib2`. Resolved it by pinning specific versions in `requirements.txt`.
* **Agent Handoffs:** Initially, agents were 'losing' information during transfers. I improved the system prompt to require explicit context sharing in every handoff call.

### 🚀 Getting it Running
1. `pip install -r requirements.txt`
2. Create a `.streamlit/secrets.toml` with your `GOOGLE_API_KEY`.
3. Run: `streamlit run stock_dashboard.py`
