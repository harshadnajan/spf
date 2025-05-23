import streamlit as st

st.set_page_config(
    page_title= "Trading App",
    page_icon= "💲",
    layout = "wide"
)

st.title("📊 Trading Guide App")

st.header("📈 Stock Trading and Analysis Dashboard")

st.image("img.jpg", use_container_width = True)

st.markdown("## We provide the following services :")

st.markdown("#### 💹 Stock Information Dashboard ")
st.write("Through this page, you can see all the information about stock")

st.markdown("#### 🔮 Stock Price Prediction ")
st.write("You can explore closing prices for the next 30 days based on historical stock data and advanced forecasting models.")
