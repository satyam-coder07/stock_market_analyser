import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import yfinance as yf
import plotly.graph_objects as go
import os

# Setup
st.set_page_config(page_title="Stock_Market AI Pro", layout="wide")
st.title("📊 Stock_Market: AI Investment Advisor")

with st.sidebar:
    st.header("Configuration")
    default_key = st.secrets.get("GROQ_API_KEY", "")
    api_key = st.text_input("Enter Groq API Key", value=default_key, type="password")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

if api_key:
    # Optimized Agent for the 6000 TPM limit
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"), # 70B has higher rate limits than 8B
        tools=[
            YFinanceTools(
                stock_price=True, 
                analyst_recommendations=True, 
                stock_fundamentals=True, 
                historical_prices=False # Crucial: Don't fetch raw history tables
            ),
            DuckDuckGo()
        ],
        show_tool_calls=True,
        description="You are a professional financial analyst specialized in the Indian market.",
        instructions=[
            "Use tables for all financial data.",
            "If DuckDuckGo fails, use your internal knowledge of May 2026 market trends.",
            "Analyze the impact of the Q4 FY26 earnings (Profit: ₹16,971 Cr, Revenue: ₹2.98L Cr).",
            "Identify key support and resistance levels from recent price action.",
            "Limit responses to 400 words to conserve tokens."
        ],
        markdown=True,
    )

    with st.sidebar:
        ticker = st.text_input("Stock Ticker", "RELIANCE.NS")
        period = st.selectbox("Chart Period", ["1mo", "3mo", "6mo", "1y"])
        generate_btn = st.button("Deep Analysis")

    if generate_btn:
        try:
            with st.spinner(f"Accessing Market Terminal for {ticker}..."):
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                info = stock.info
                current_price = hist['Close'].iloc[-1]

                # Metric Row
                c1, c2, c3 = st.columns(3)
                c1.metric("Current Price", f"₹{current_price:.2f}")
                c2.metric("52W High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}")
                c3.metric("PE Ratio", f"{info.get('trailingPE', 'N/A')}")

                # Chart
                fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], 
                                high=hist['High'], low=hist['Low'], close=hist['Close'])])
                fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)

                # AI Analysis
                st.subheader("🤖 Expert AI Insights")
                # We feed the core data into the prompt to PREVENT the agent 
                # from needing to fetch it, saving tokens and avoiding tool errors.
                analysis_prompt = (
                    f"Analyze {ticker} at price {current_price:.2f}. "
                    f"Context: Q4 FY26 net profit was ₹16,971 Cr (down 12.5% YoY). "
                    f"Jio and Retail grew 13%. Mention the ₹1,500 resistance level. "
                    f"If DuckDuckGo news tool fails, provide analysis based on this context."
                )
                
                response = agent.run(analysis_prompt)
                st.markdown(response.content)

        except Exception as e:
            st.error(f"Analysis Interrupted: {str(e)}")
else:
    st.info("Enter your API Key to unlock the AI analyst.")