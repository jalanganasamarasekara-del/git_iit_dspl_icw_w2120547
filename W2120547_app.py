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
    
    # Market filter 
    filtered_markets = df[df['Country'].isin(selected_countries)]['Market Name'].unique()

    selected_markets = st.sidebar.multiselect(
        "Select Market:",
        options=filtered_markets,
        default=filtered_markets[:3]
    )
    
    # Date filter
    min_date = df['Dates'].min()
    max_date = df['Dates'].max()

    date_range = st.sidebar.slider(
        "Select Date Range:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )
    
    # FILTER DATA
    filtered_df = df[
        (df['Country'].isin(selected_countries)) &
        (df['Market Name'].isin(selected_markets)) &
        (df['Dates'] >= date_range[0]) &
        (df['Dates'] <= date_range[1])
    ]
    
    # TABS
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🌍 Comparison", "📁 Data"])
    
    # TAB 1 — TREND ANALYSIS
    with tab1:
        st.subheader("📈 Exchange Rate Trends")

        if not filtered_df.empty:
            fig = px.line(
                filtered_df,
                x="Dates",
                y="Exchange_Rate",
                color="Market Name",
                title="Exchange Rate Over Time",
                markers=True
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")


