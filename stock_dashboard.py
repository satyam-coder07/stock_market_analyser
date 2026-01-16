import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import yfinance as yf
import plotly.graph_objects as go
import os


yf.set_tz_cache_location("cache")

st.set_page_config(page_title="Stock_Market AI", layout="wide")

st.title("📊 Stock_Market: Multi-Agent Investment Advisor")
st.markdown("Powered by Google Gemini 2.5 Flash and Phidata")


if "GOOGLE_API_KEY" in st.secrets:
    google_key = st.secrets["GOOGLE_API_KEY"]
else:
    with st.sidebar:
        st.header("Configuration")
        google_key = st.text_input("Enter Google API Key", type="password")
        st.info("Get your free key at [Google AI Studio](https://aistudio.google.com/)")

if google_key:
    os.environ["GOOGLE_API_KEY"] = google_key

    web_search_agent = Agent(
        name="Web Search Agent",
        role="Search the web for the latest financial news",
        model=Gemini(id="gemini-2.5-flash"),
        tools=[DuckDuckGo()],
        instructions=["Always include sources", "Focus on market impact"],
        markdown=True,
    )

    finance_agent = Agent(
        name="Finance Agent",
        role="Get financial data and analyze stocks",
        model=Gemini(id="gemini-2.5-flash"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, historical_prices=True)],
        instructions=["Use tables to display data"],
        markdown=True,
    )

    technical_agent = Agent(
        name="Technical Analyst",
        role="Analyze technical indicators and chart patterns",
        model=Gemini(id="gemini-2.5-flash"),
        tools=[YFinanceTools(technical_indicators=True, historical_prices=True)],
        instructions=["Identify support/resistance levels", "Check RSI and Moving Average crossovers"],
        markdown=True,
    )

    multi_ai_agent = Agent(
        team=[web_search_agent, finance_agent, technical_agent],
        model=Gemini(id="gemini-2.5-flash"),
        instructions=["Combine data from news, fundamentals, and technicals to give a clear investment summary."],
        markdown=True,
    )


    with st.sidebar:
        st.header("Input")
        ticker = st.text_input("Stock Ticker", "RELIANCE.NS")
        period = st.selectbox("Chart Period", ["1mo", "3mo", "6mo", "1y", "5y"])
        generate_btn = st.button("Analyze Stock")

    if generate_btn:
        try:
            with st.spinner(f"Fetching data for {ticker}..."):
                stock_data = yf.Ticker(ticker)
                hist = stock_data.history(period=period)
            
            if hist.empty:
                st.error(f"Could not find data for {ticker}. Please check the symbol.")
            else:

                col1, col2, col3 = st.columns(3)
                info = stock_data.info
                if info is None:
                    info = {}
                
                current_price = hist['Close'].iloc[-1]
                
                with col1:
                    st.metric("Current Price", f"₹{current_price:.2f}")
                with col2:
                    st.metric("52 Week High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}")
                with col3:
                    mcap = info.get('marketCap')
                    if mcap:

                        fmt_mcap = f"₹{mcap/1e7:.2f} Cr" if mcap < 1e12 else f"₹{mcap/1e12:.2f} T"
                        st.metric("Market Cap", fmt_mcap)
                    else:
                        st.metric("Market Cap", "N/A")


                st.subheader("Price History")
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name='Price'
                ))
                fig.update_layout(xaxis_rangeslider_visible=False, height=500)
                st.plotly_chart(fig, width='stretch')


                st.subheader("AI Investment Analysis")
                with st.spinner("Agents are analyzing market data, news, and technicals..."):
                    response_placeholder = st.empty()

                    full_response = ""

                    response = multi_ai_agent.run(f"Analyze {ticker} stock and give a comprehensive investment recommendation based on technicals, fundamentals, and latest news.")
                    
                    st.markdown(response.content)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

else:
    st.warning("Please enter your Google API Key in the sidebar to proceed.")
