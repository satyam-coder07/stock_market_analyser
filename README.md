# Stock_Market AI: Intelligent Investment Advisor

Stock_Market AI is a Streamlit-based application that leverages large language models and real-time financial data to provide intelligent investment insights. It combines Groq-powered LLMs with financial APIs to deliver technical, fundamental, and news-based analysis in a single interface.

---

## Live Features

- Real-time stock data visualization using candlestick charts  
- AI-driven investment recommendations  
- Technical and fundamental analysis  
- Analyst recommendations and latest news integration  
- Interactive and user-friendly dashboard  

---

## Tech Stack

- **Frontend**: Streamlit  
- **LLM Engine**: Groq (Llama 3.1 / 3.3 models via Phidata)  
- **Financial Data**: yFinance  
- **Visualization**: Plotly  
- **Search Tool**: DuckDuckGo  
- **Agent Framework**: Phidata  

---

## Application Overview

The system uses an AI agent that integrates multiple tools:

- Fetches real-time stock prices and historical data  
- Retrieves analyst recommendations and fundamentals  
- Searches latest news using DuckDuckGo  
- Performs combined reasoning using LLM  

---

## Key Features

### AI Investment Analysis
- Combines technical indicators, fundamentals, and news  
- Generates structured and explainable insights  
- Uses tool-calling for accurate financial data retrieval  

### Interactive Dashboard
- Candlestick chart for price trends  
- Key metrics:
  - Current Price  
  - 52-week High  
  - Market Capitalization  

### Smart Retry Logic
- Handles API rate limits using exponential backoff  

---

## Project Structure

```bash
stock-market-ai/
├── app.py                  # Main Streamlit application
├── cache/                  # Cached timezone and data files
└── requirements.txt        # Dependencies
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stock-market-ai.git
cd stock-market-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

You need a Groq API key to run the application.

### Option 1: Using Streamlit Secrets

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your_api_key_here"
```

### Option 2: Enter in UI

- Enter your API key directly in the sidebar when running the app  

Get your API key here: https://console.groq.com/keys

---

## Running the Application

```bash
streamlit run app.py
```

---

## Usage

1. Enter your Groq API key  
2. Input a stock ticker (e.g., `RELIANCE.NS`, `AAPL`)  
3. Select a time period  
4. Click **Analyze Stock**  
5. View:
   - Price chart  
   - Key metrics  
   - AI-generated investment insights  

---

## Example Tickers

- RELIANCE.NS  
- TCS.NS  
- INFY.NS  
- AAPL  
- TSLA  

---

## How It Works

1. User inputs stock ticker  
2. yFinance fetches historical and live data  
3. Plotly renders candlestick chart  
4. AI agent:
   - Calls financial tools  
   - Retrieves news  
   - Performs reasoning  
5. Final structured recommendation is displayed  

---

## Future Improvements

- Portfolio tracking and comparison  
- Risk scoring models  
- Sentiment analysis from social media  
- Multi-stock comparison dashboard  
- Exportable investment reports  

---

## License

This project is intended for educational and experimental purposes. Add a suitable license if needed.

---

## Disclaimer

This application is for informational purposes only and does not constitute financial advice. Always conduct your own research before making investment decisions.
