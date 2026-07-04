import streamlit as st
import yfinance as yf

st.title("Stock Price ChatBot")

symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if symbol:
    stock = yf.Ticker(symbol)
    
    data = stock.history(period="1d")
    if not data.empty:

        current_price = data['Close'].iloc[-1]
        st.success(f"Current Price: ₹{current_price:.2f}")

    else:
        st.warning("Error: No data found for the given symbol.")

    history = stock.history(period="1mo")
    st.subheader("Last 1 Month Stock Performance")
    
    st.line_chart(history['Close'])
    