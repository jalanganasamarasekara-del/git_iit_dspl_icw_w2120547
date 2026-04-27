# IMPORT LIBRARIES
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Global Exchange Rate Dashboard",
    page_icon="💱",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("global_currency_2026_processed.csv")

    # Clean column names 
    df.columns = df.columns.str.strip()

    # Convert date
    df['Dates'] = pd.to_datetime(df['Dates'])

    return df

df = load_data()

# SIDEBAR NAVIGATION
page = st.sidebar.selectbox("📌 Navigation", ["About", "Dashboard"])

# ABOUT PAGE
if page == "About":
    st.title("📚 About this Dashboard")

    st.markdown("""
    ## 🌍 Global Exchange Rate Dashboard

    This dashboard analyses unofficial exchange rates across countries and markets using real-time data.

    ### 🔍 Key Features:
    - 📈 Time-series trend analysis  
    - 🌍 Country-level comparison  
    - 📍 Market-level insights  
    - 📊 Interactive filtering  

    ### 📊 Dataset:
    - Source: Humanitarian Data Exchange (World Bank RTP)
    - Focus: Exchange Rate (RTFX)
    - Year: 2026

    ### 🎯 Purpose:
    To help decision-makers understand currency fluctuations and regional variations.

    ### 🛠 Tools:
    Streamlit, Plotly, Pandas
    """)

# DASHBOARD PAGE
elif page == "Dashboard":

    st.title("💱 Global Exchange Rate Dashboard")
    st.markdown("Explore exchange rate trends across countries and markets.")
    
    # SIDEBAR FILTERS
    st.sidebar.header("🔎 Filters")
    
    # Country filter
    countries = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select Country:",
        options=countries,
        default=countries[:2]
    )
