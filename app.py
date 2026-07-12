import streamlit as st
import yfinance as yf

st.title("Stock Price ChatBot")

symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if symbol:
    stock = yf.Ticker(symbol)   
    info = stock.info

    
    data = stock.history(period="1wk")
    if not data.empty:

        # Current Price
        current_price = data['Close'].iloc[-1]
        
        st.metric("Current Price", f"₹{current_price:.2f}")

        # Market Cap
        market_cap_raw = info.get("marketCap", 0)   # Numeric value for calculations

        if market_cap_raw:
            market_cap = f"₹{market_cap_raw/10000000000:.2f} Trillion"  # formatted text
        else:
            market_cap = "N/A"

        pe_ratio = info.get("trailingPE", "N/A")
        high_52 = info.get("fiftyTwoWeekHigh", "N/A")
        low_52 = info.get("fiftyTwoWeekLow", "N/A")
        dividend = info.get("dividendYield", "N/A")
        score = 0       # score will be calculated based on various factors afterwards

        # Company Information
        company_name = info.get("longName")
        sector = info.get("sector")
        industry = info.get("industry")

        st.subheader("Company Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(company_name)
        with col2:
            st.info(sector)
        with col3:
            st.info(industry)

        st.subheader("Stock Metrics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("P/E Ratio", pe_ratio)

        with col2:
            st.metric("Dividend Yield", f"{dividend:.2f}%")
            

        st.write("Market Cap:", f"{market_cap}")
        st.write("52 Week High:", high_52)
        st.write("52 Week Low:", low_52)

        # Investment Recommendation + score
        recommendation = "N/A"
        if pe_ratio != "N/A":

            if pe_ratio < 20:
                recommendation = "BUY"
                score += 40

            elif pe_ratio < 35:
                recommendation = "HOLD"
                score += 25

            else:
                recommendation = "SELL"
                score += 10


        # Dividend Score 
        if dividend != "N/A":
            if dividend > 0:
                score += 30
            

        # Market Cap Score
        if market_cap_raw > 100000000000:
            score += 30
        else:
            score += 15

        # Displaying score
        st.subheader("Financial Health Score")
        st.progress(score)
        st.write(f"Score: {score}/100")


        st.subheader("Investment Recommendation")
        if recommendation == "BUY":
            st.success("BUY")
        elif recommendation == "HOLD":
            st.warning("HOLD")
        elif recommendation == "SELL":
            st.error("SELL")
        else:
            st.info("Recommendation Unavailable")
            

        history = stock.history(period="1mo")
        
        # Volatility Score for Risk Analysis
        volatility = history["Close"].std()

        if volatility < 20:
            risk = "Low Risk"
        elif volatility < 50:
            risk = "Medium Risk"
        else:
            risk = "High Risk"

        
        st.subheader("Risk Analysis")
        if risk == "Low Risk":
            st.success(risk)
        elif risk == "Medium Risk":
            st.warning(risk)
        else:
            st.error(risk)  
        

        st.subheader("Last 1 Month Stock Performance")

        st.line_chart(history['Close'])

    else:
        st.warning("Error: No data found for the given symbol.")
    