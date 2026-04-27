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
