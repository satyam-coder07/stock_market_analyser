import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import yfinance as yf
import plotly.graph_objects as go
import os
import time

# Ensure cache directory exists
if not os.path.exists("cache"):
    os.makedirs("cache")
yf.set_tz_cache_location("cache")

st.set_page_config(page_title="Stock_Market AI", layout="wide")

st.title("📊 Stock_Market: AI Investment Advisor")
st.markdown("Optimized to bypass Groq TPM Rate Limits")

with st.sidebar:
    st.header("Configuration")
    default_key = st.secrets.get("GROQ_API_KEY", "")
    api_key = st.text_input("Enter Groq API Key", value=default_key, type="password")
    st.info("Get your free key at [Groq Console](https://console.groq.com/keys)")

if api_key:
    os.environ["GROQ_API_KEY"] = api_key

    # Optimization: Using 70b (higher limits) and restricting tool output
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[
            YFinanceTools(
                stock_price=True, 
                analyst_recommendations=True, 
                stock_fundamentals=True, 
                historical_prices=False # Set to False because we provide the chart via Streamlit
            ),
            DuckDuckGo()
        ],
        show_tool_calls=True,
        description="You are a concise financial analyst.",
        instructions=[
            "Use tables for data comparison.",
            "Always include sources.",
            "DO NOT request historical price tables (TPM limit risk).",
            "Focus on analyst ratings and the latest news summary.",
            "Keep the final response under 300 words."
        ],
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

                # Visual Chart
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
                fig.update_layout(xaxis_rangeslider_visible=False, height=450, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("AI Investment Analysis")
                with st.spinner("Agent analyzing news and fundamentals..."):
                    # We pass the current price into the prompt to reduce the need for the agent to fetch it
                    prompt = (
                        f"The current price for {ticker} is {current_price:.2f}. "
                        f"Summarize the analyst recommendations and find the 3 most recent news "
                        f"headlines that could impact the price. Be very brief to save tokens."
                    )
                    
                    try:
                        response = agent.run(prompt)
                        st.markdown(response.content)
                    except Exception as e:
                        if "413" in str(e) or "rate_limit" in str(e).lower():
                            st.error("The data from Yahoo Finance is too large for the Groq Free Tier. Try a different ticker or wait 60 seconds.")
                        else:
                            st.error(f"Error: {e}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

else:
    st.warning("Please enter your Groq API Key in the sidebar to proceed.")