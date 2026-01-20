import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import yfinance as yf
import plotly.graph_objects as go
import os
import time

yf.set_tz_cache_location("cache")

st.set_page_config(page_title="Stock_Market AI", layout="wide")

st.title("📊 Stock_Market: AI Investment Advisor")
st.markdown("Powered by Groq (Llama 3.3 70B) and Phidata")

with st.sidebar:
    st.header("Configuration")
    default_key = st.secrets.get("GROQ_API_KEY", "")
    api_key = st.text_input("Enter Groq API Key", value=default_key, type="password")
    st.info("Get your free key at [Groq Console](https://console.groq.com/keys)")

if api_key:
    os.environ["GROQ_API_KEY"] = api_key

    agent = Agent(
        model=Groq(id="llama-3.1-8b-instant"),
        tools=[
            YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, historical_prices=True),
            DuckDuckGo()
        ],
        show_tool_calls=True,
        description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
        instructions=["Use tables to display data.", "Always include sources.", "Analyze technicals and fundamentals.", "Do not generate text before calling a tool.", "Directly call the relevant tools."],
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
                with st.spinner("Agent is analyzing market data, news, and fundamentals..."):
                    retry_count = 0
                    while True:
                        try:
                            response = agent.run(f"Analyze {ticker} stock and give a comprehensive investment recommendation based on technicals, fundamentals, and latest news.")
                            break
                        except Exception as e:
                            if "Too Many Requests" in str(e) and retry_count < 5:
                                time.sleep(2 ** retry_count)
                                retry_count += 1
                            else:
                                raise e
                    
                    st.markdown(response.content)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

else:
    st.warning("Please enter your Groq API Key in the sidebar to proceed.")