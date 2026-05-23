import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Sustainable Portfolio Simulator",
    layout="wide"
)

# ------------------------------------------------------------
# Title and introduction
# ------------------------------------------------------------

st.title("Sustainable Multi-Asset Portfolio Simulator")

st.write(
    """
    This dashboard simulates a sustainable multi-asset portfolio by combining
    financial performance, ESG scoring, climate indicators and investment recommendations.
    
    The objective is to show how portfolio management decisions can integrate both
    traditional financial metrics and sustainability criteria.
    """
)

# ------------------------------------------------------------
# Portfolio data
# ------------------------------------------------------------

data = {
    "Asset": [
        "Schneider Electric",
        "Air Liquide",
        "Sanofi",
        "ASML",
        "Veolia",
        "BNP Paribas",
        "TotalEnergies",
        "Green Bond ETF",
        "Climate ETF",
        "Euro Government Bond ETF"
    ],
    "Ticker": [
        "SU.PA",
        "AI.PA",
        "SAN.PA",
        "ASML.AS",
        "VIE.PA",
        "BNP.PA",
        "TTE.PA",
        "GREEN_BOND",
        "CLIMATE_ETF",
        "EU_GOV_BOND"
    ],
    "Asset Class": [
        "Equity",
        "Equity",
        "Equity",
        "Equity",
        "Equity",
        "Equity",
        "Equity",
        "Bond ETF",
        "ETF",
        "Bond ETF"
    ],
    "Sector": [
        "Industrials",
        "Industrials",
        "Healthcare",
        "Technology",
        "Utilities",
        "Financials",
        "Energy",
        "Fixed Income",
        "Multi-sector",
        "Sovereign Bonds"
    ],
    "Weight": [
        0.10,
        0.08,
        0.08,
        0.10,
        0.07,
        0.07,
        0.05,
        0.15,
        0.15,
        0.15
    ],
    "Expected Return": [
        0.085,
        0.070,
        0.055,
        0.095,
        0.060,
        0.065,
        0.075,
        0.035,
        0.070,
        0.030
    ],
    "Volatility": [
        0.22,
        0.20,
        0.16,
        0.28,
        0.18,
        0.24,
        0.30,
        0.07,
        0.19,
        0.05
    ],
    "ESG Score": [
        88,
        82,
        76,
        84,
        80,
        68,
        52,
        78,
        85,
        72
    ],
    "Climate Score": [
        90,
        78,
        70,
        75,
        82,
        62,
        45,
        84,
        88,
        70
    ],
    "Controversy Risk": [
        "Low",
        "Low",
        "Medium",
        "Low",
        "Low",
        "Medium",
        "High",
        "Low",
        "Low",
        "Low"
    ]
}

portfolio = pd.DataFrame(data)

# ------------------------------------------------------------
# Recommendation logic
# ------------------------------------------------------------

def get_recommendation(row):
    if row["ESG Score"] >= 80 and row["Climate Score"] >= 80:
        return "Overweight"
    elif row["ESG Score"] >= 65 and row["Climate Score"] >= 60:
        return "Hold"
    elif row["ESG Score"] >= 50:
        return "Watchlist"
    else:
        return "Underweight"

portfolio["Recommendation"] = portfolio.apply(get_recommendation, axis=1)

# ------------------------------------------------------------
# Weighted portfolio indicators
# ------------------------------------------------------------

weighted_return = (portfolio["Weight"] * portfolio["Expected Return"]).sum()
weighted_volatility = (portfolio["Weight"] * portfolio["Volatility"]).sum()
weighted_esg_score = (portfolio["Weight"] * portfolio["ESG Score"]).sum()
weighted_climate_score = (portfolio["Weight"] * portfolio["Climate Score"]).sum()

risk_free_rate = 0.03
sharpe_ratio = (weighted_return - risk_free_rate) / weighted_volatility

# ------------------------------------------------------------
# Dashboard KPIs
# ------------------------------------------------------------

st.header("Portfolio Key Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Expected Return", f"{weighted_return:.2%}")
col2.metric("Volatility", f"{weighted_volatility:.2%}")
col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
col4.metric("ESG Score", f"{weighted_esg_score:.1f}/100")
col5.metric("Climate Score", f"{weighted_climate_score:.1f}/100")

# ------------------------------------------------------------
# Portfolio table
# ------------------------------------------------------------

st.header("Portfolio Composition")

display_portfolio = portfolio.copy()
display_portfolio["Weight"] = display_portfolio["Weight"].map("{:.1%}".format)
display_portfolio["Expected Return"] = display_portfolio["Expected Return"].map("{:.1%}".format)
display_portfolio["Volatility"] = display_portfolio["Volatility"].map("{:.1%}".format)

st.dataframe(display_portfolio, use_container_width=True)

# ------------------------------------------------------------
# Charts
# ------------------------------------------------------------

st.header("Portfolio Visual Analysis")

left_col, right_col = st.columns(2)

with left_col:
    allocation_chart = px.pie(
        portfolio,
        names="Asset Class",
        values="Weight",
        title="Portfolio Allocation by Asset Class"
    )
    st.plotly_chart(allocation_chart, use_container_width=True)

with right_col:
    sector_chart = px.pie(
        portfolio,
        names="Sector",
        values="Weight",
        title="Portfolio Allocation by Sector"
    )
    st.plotly_chart(sector_chart, use_container_width=True)

left_col, right_col = st.columns(2)

with left_col:
    esg_chart = px.bar(
        portfolio,
        x="Asset",
        y="ESG Score",
        title="ESG Score by Asset",
        text="ESG Score"
    )
    st.plotly_chart(esg_chart, use_container_width=True)

with right_col:
    climate_chart = px.bar(
        portfolio,
        x="Asset",
        y="Climate Score",
        title="Climate Score by Asset",
        text="Climate Score"
    )
    st.plotly_chart(climate_chart, use_container_width=True)

# ------------------------------------------------------------
# Analysis section
# ------------------------------------------------------------

st.header("Investment Interpretation")

st.write(
    """
    The portfolio combines listed equities, green bond exposure, climate-themed ETFs
    and sovereign bond exposure. The allocation aims to balance growth opportunities,
    defensive exposure, ESG quality and climate transition alignment.
    """
)

st.subheader("Main Observations")

st.write(
    """
    - The portfolio has a diversified exposure across equities, bonds and climate-related instruments.
    - Schneider Electric, ASML and the Climate ETF contribute positively to the ESG and climate profile.
    - TotalEnergies remains in the portfolio as a transition-risk case study but receives a Watchlist recommendation.
    - Bond ETFs reduce the overall volatility of the portfolio.
    - The ESG and climate scores help complement traditional risk-return analysis.
    """
)

st.subheader("Methodology Note")

st.write(
    """
    The ESG scoring methodology is inspired by market-standard frameworks such as MSCI ESG Ratings
    and Morningstar Sustainalytics ESG Risk Ratings. The current version uses simplified public-data-based
    assumptions for educational and portfolio demonstration purposes.
    """
)
