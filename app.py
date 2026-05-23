import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sustainable Portfolio Simulator",
    layout="wide"
)

st.title("Sustainable Multi-Asset Portfolio Simulator")

st.write(
    """
    This project simulates a sustainable multi-asset portfolio by combining
    financial performance, ESG scoring, climate indicators and portfolio reporting.
    """
)

st.header("Project Objective")

st.write(
    """
    The objective is to compare investment decisions using both traditional
    financial metrics and sustainability indicators such as ESG score,
    climate transition exposure and controversy risk.
    """
)

st.header("Portfolio Overview")

data = {
    "Asset": ["Schneider Electric", "Air Liquide", "Sanofi", "ASML", "Green Bond ETF"],
    "Asset Class": ["Equity", "Equity", "Equity", "Equity", "Bond ETF"],
    "Weight": [0.20, 0.20, 0.15, 0.25, 0.20],
    "ESG Score": [88, 82, 76, 84, 80],
    "Climate Score": [90, 78, 70, 75, 85],
}

portfolio = pd.DataFrame(data)

st.dataframe(portfolio)

st.metric("Average ESG Score", round(portfolio["ESG Score"].mean(), 1))
st.metric("Average Climate Score", round(portfolio["Climate Score"].mean(), 1))
