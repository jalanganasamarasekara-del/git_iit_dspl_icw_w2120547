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

st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #0f1f17;
    }

    /* Text color */
    h1, h2, h3, h4, h5, h6, p, div {
        color: #e8f5e9;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #132a1f;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #1b3a2f;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

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
    min_date = df['Dates'].min().to_pydatetime()
    max_date = df['Dates'].max().to_pydatetime()

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
    (df['Dates'] >= pd.to_datetime(date_range[0])) &
    (df['Dates'] <= pd.to_datetime(date_range[1]))
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
                markers=True,
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig.update_layout(
                title="Exchange Rate Over Time",
                title_font_size=20,
                template="plotly_dark",
                hovermode="x unified",
                legend_title="Markets",
                paper_bgcolor="#0f1f17",
                plot_bgcolor="#0f1f17"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")
    
    # TAB 2 — COUNTRY COMPARISON
    with tab2:
        st.subheader("🌍 Latest Exchange Rate Comparison")

        if not filtered_df.empty:
            latest_date = filtered_df['Dates'].max()
            latest_data = filtered_df[filtered_df['Dates'] == latest_date]

            fig = px.bar(
                latest_data,
                x="Market Name",
                y="Exchange_Rate",
                color="Country",
                title=f"Exchange Rate by Market ({latest_date.date()})"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available.")
    
    # KPI SECTION
    st.markdown("---")
    st.subheader("📌 Key Metrics")

    if not filtered_df.empty:
        col1, col2, col3 = st.columns(3)

        latest_rate = filtered_df.sort_values("Dates").iloc[-1]["Exchange_Rate"]
        avg_rate = filtered_df["Exchange_Rate"].mean()
        max_rate = filtered_df["Exchange_Rate"].max()

        col1.metric("Latest Rate", f"{latest_rate:.2f}")
        col2.metric("Average Rate", f"{avg_rate:.2f}")
        col3.metric("Max Rate", f"{max_rate:.2f}")
    else:
        st.info("No data available.")
    
    # TAB 3 — RAW DATA
    with tab3:
        st.subheader("📁 Filtered Dataset")
        st.dataframe(filtered_df.sort_values("Dates"), use_container_width=True)


