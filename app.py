"""
📈 Mutual Fund Investment Analytics - Premium FinTech Web Platform
An institutional-grade Business Intelligence, Decision Intelligence, and Portfolio Management system.
Features:
  - Modern FinTech Design System (Inter typography, custom KPI cards, micro-interactions)
  - Tab 1: 🎯 Buy Opportunities (Tactical Dip Engine, Alerts & Spline Trend Analysis)
  - Tab 2: 📊 Portfolio Performance & Asset Allocation (Treemap, Donut, Holdings P&L)
  - Tab 3: ⚡ Management & Operations Hub (1-Click ETL, Scheme Onboarding, Trade Entry)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import pyodbc
import io
import requests
import time
import os

# ==============================================================================
# Page Configuration & Modern FinTech Design System
# ==============================================================================
st.set_page_config(
    page_title="Mutual Fund Investment Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global High-End CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Banner / Hero */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 16px;
        padding: 24px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-top: 6px;
    }

    /* Custom FinTech KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease-in-out;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.08);
        border-color: #CBD5E1;
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-icon-badge {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        font-family: 'Inter', sans-serif;
        line-height: 1.2;
    }
    .kpi-footer {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
    }
    .badge-pill-positive {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .badge-pill-alert {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .badge-pill-neutral {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Buy Signal Banner Cards */
    .signal-card {
        background: #FFFFFF;
        border: 1.5px solid #10B981;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
        transition: transform 0.2s ease;
    }
    .signal-card:hover {
        transform: translateX(4px);
    }
    .badge-buy-glow {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.35);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-wait-soft {
        background: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 22px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #64748B;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    /* Card Containers */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# Database Helper & Dynamic Driver Detection
# ==============================================================================
DEFAULT_SERVER = "localhost"
DEFAULT_DB = "MFInvestmentDB"

def get_installed_driver():
    """Detects best available SQL Server ODBC driver installed on the system."""
    drivers = pyodbc.drivers()
    if "ODBC Driver 18 for SQL Server" in drivers:
        return "ODBC Driver 18 for SQL Server"
    if "ODBC Driver 17 for SQL Server" in drivers:
        return "ODBC Driver 17 for SQL Server"
    sql_drivers = [d for d in drivers if "SQL Server" in d]
    if sql_drivers:
        return sql_drivers[0]
    return "SQL Server"

def get_connection_string(server=DEFAULT_SERVER, database=DEFAULT_DB, driver=None):
    if not driver:
        driver = get_installed_driver()
    extra = ";TrustServerCertificate=yes" if "18" in driver else ""
    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes{extra};"
    )

def test_db_connection(server, database, driver):
    try:
        conn = pyodbc.connect(get_connection_string(server, database, driver), timeout=3)
        conn.close()
        return True, "Connected successfully"
    except Exception as e:
        return False, str(e)


# ==============================================================================
# Benchmark Demo Data (Sample Portfolio Data)
# ==============================================================================
def get_sample_data():
    """Provides sample portfolio data if database instance is offline."""
    funds_data = [
        {"FundID": 1, "SchemeCode": 119551, "FundName": "Nippon India Nifty Bank Index Fund - Direct Plan - Growth Option", "AMC": "Nippon", "FundCategory": "Nifty Bank Index", "AlertThreshold": -2.0, "IsActive": 1},
        {"FundID": 2, "SchemeCode": 120716, "FundName": "UTI Nifty 50 Index Fund - Growth Option- Direct", "AMC": "UTI", "FundCategory": "Nifty 50 Index", "AlertThreshold": -1.0, "IsActive": 1},
        {"FundID": 3, "SchemeCode": 118989, "FundName": "HDFC Flexi Cap Fund - Growth Option - Direct Plan", "AMC": "HDFC", "FundCategory": "Flexi Cap", "AlertThreshold": -2.0, "IsActive": 1},
        {"FundID": 4, "SchemeCode": 118991, "FundName": "HDFC Mid Cap Fund - Growth Option - Direct Plan", "AMC": "HDFC", "FundCategory": "Mid Cap", "AlertThreshold": -2.0, "IsActive": 1},
        {"FundID": 5, "SchemeCode": 120586, "FundName": "ICICI Prudential Gold ETF FOF - Direct Plan - Growth", "AMC": "ICICI", "FundCategory": "Gold ETF", "AlertThreshold": -3.0, "IsActive": 1},
        {"FundID": 6, "SchemeCode": 120503, "FundName": "ICICI Prudential Large Cap Fund (erstwhile Bluechip Fund) - Direct Plan - Growth", "AMC": "ICICI", "FundCategory": "Large Cap", "AlertThreshold": -1.0, "IsActive": 1},
        {"FundID": 7, "SchemeCode": 149301, "FundName": "ICICI Prudential Silver ETF FOF - Direct Plan - Growth", "AMC": "ICICI", "FundCategory": "Silver ETF", "AlertThreshold": -5.0, "IsActive": 1},
        {"FundID": 8, "SchemeCode": 147879, "FundName": "Nippon India Nifty IT Index Fund - Direct Plan - Growth Option", "AMC": "Nippon", "FundCategory": "Nifty IT Index", "AlertThreshold": -2.0, "IsActive": 1},
        {"FundID": 9, "SchemeCode": 118778, "FundName": "Nippon India Small Cap Fund - Direct Plan Growth Plan - Growth Option", "AMC": "Nippon", "FundCategory": "Small Cap", "AlertThreshold": -2.0, "IsActive": 1},
    ]
    funds_df = pd.DataFrame(funds_data)

    base_date = date(2026, 7, 27)
    dates = [base_date - timedelta(days=i) for i in range(11, -1, -1)]

    nav_benchmarks = {
        1: (12.63, 12.32),
        2: (171.05, 168.79),
        3: (2248.74, 2232.42),
        4: (229.28, 229.63),
        5: (44.76, 45.89),
        6: (120.56, 119.44),
        7: (32.83, 34.10),
        8: (8.02, 8.09),
        9: (203.59, 202.32),
    }

    nav_rows = []
    for fid, (start_n, end_n) in nav_benchmarks.items():
        interp = np.linspace(start_n, end_n, len(dates))
        for d, n in zip(dates, interp):
            nav_rows.append({"FundID": fid, "NAVDate": d, "NAV": round(float(n), 4)})
    nav_df = pd.DataFrame(nav_rows)

    tx_data = [
        {"TransactionID": 1, "FundID": 2, "TransactionDate": date(2026, 3, 15), "TransactionType": "BUY", "Amount": 65000.0, "NAV": 167.51, "Units": 388.05},
        {"TransactionID": 2, "FundID": 6, "TransactionDate": date(2026, 3, 15), "TransactionType": "BUY", "Amount": 55000.0, "NAV": 119.17, "Units": 461.51},
        {"TransactionID": 3, "FundID": 4, "TransactionDate": date(2026, 4, 10), "TransactionType": "BUY", "Amount": 50000.0, "NAV": 229.30, "Units": 218.06},
        {"TransactionID": 4, "FundID": 7, "TransactionDate": date(2026, 4, 10), "TransactionType": "BUY", "Amount": 40000.0, "NAV": 33.24, "Units": 1203.19},
        {"TransactionID": 5, "FundID": 3, "TransactionDate": date(2026, 5, 5), "TransactionType": "BUY", "Amount": 35000.0, "NAV": 2212.62, "Units": 15.82},
        {"TransactionID": 6, "FundID": 9, "TransactionDate": date(2026, 5, 5), "TransactionType": "BUY", "Amount": 35000.0, "NAV": 201.43, "Units": 173.76},
        {"TransactionID": 7, "FundID": 1, "TransactionDate": date(2026, 6, 2), "TransactionType": "BUY", "Amount": 34000.0, "NAV": 12.28, "Units": 2769.78},
        {"TransactionID": 8, "FundID": 8, "TransactionDate": date(2026, 6, 2), "TransactionType": "BUY", "Amount": 27000.0, "NAV": 7.83, "Units": 3446.62},
    ]
    tx_df = pd.DataFrame(tx_data)
    return funds_df, nav_df, tx_df


@st.cache_data(ttl=300, show_spinner=False)
def load_db_data(server, database, driver):
    conn_str = get_connection_string(server, database, driver)
    conn = pyodbc.connect(conn_str, timeout=3)
    funds = pd.read_sql("SELECT * FROM dbo.FundMaster WHERE IsActive = 1", conn)
    navs = pd.read_sql("SELECT * FROM dbo.NAVHistory ORDER BY NAVDate ASC", conn)
    txs = pd.read_sql("SELECT * FROM dbo.Transactions ORDER BY TransactionDate ASC", conn)
    conn.close()

    if not navs.empty:
        navs['NAVDate'] = pd.to_datetime(navs['NAVDate']).dt.date
        navs['NAV'] = navs['NAV'].astype(float)
    if not txs.empty:
        txs['TransactionDate'] = pd.to_datetime(txs['TransactionDate']).dt.date
        txs['Amount'] = txs['Amount'].astype(float)
        txs['NAV'] = txs['NAV'].astype(float)
        txs['Units'] = txs['Units'].astype(float)
    if not funds.empty:
        funds['AlertThreshold'] = funds['AlertThreshold'].astype(float)

    return funds, navs, txs


# ==============================================================================
# Sidebar - Data Source & Connection Settings
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="background: #4F46E5; color: white; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold;">📈</div>
        <div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #0F172A; line-height: 1.1;">MF Analytics</div>
            <div style="font-size: 0.75rem; color: #64748B;">Decision Intelligence Hub</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("PLATFORM SETTINGS")
    
    data_mode = st.radio(
        "Data Source Mode",
        options=["Live SQL Server", "Demo / Benchmark Mode"],
        index=0,
        help="Switch to Demo mode to explore full dashboard visuals even when SQL Server is offline."
    )

    with st.expander("Database Configuration", expanded=False):
        detected_drv = get_installed_driver()
        installed_drivers = pyodbc.drivers()
        driver_choice = st.selectbox(
            "ODBC Driver",
            options=installed_drivers if installed_drivers else [detected_drv],
            index=0 if detected_drv in installed_drivers else 0
        )
        server_input = st.text_input("Server", value=DEFAULT_SERVER)
        db_input = st.text_input("Database", value=DEFAULT_DB)

        scol1, scol2 = st.columns(2)
        with scol1:
            if st.button("Test", use_container_width=True):
                is_ok, msg = test_db_connection(server_input, db_input, driver_choice)
                if is_ok:
                    st.success("Connected!")
                else:
                    st.error(f"Failed: {msg[:60]}...")
        with scol2:
            if st.button("Reset", use_container_width=True):
                st.cache_data.clear()
                st.rerun()

    st.markdown("---")
    st.caption("PORTFOLIO SUMMARY")
    st.markdown("""
    - **Total Schemes**: `9 Tracked`
    - **AMCs Active**: `4 Providers`
    - **NAV Frequency**: `Daily Batch`
    """)
    st.markdown("---")
    st.caption("Mutual Fund Investment Analytics v2.0")


# Load Data
funds_df, nav_df, tx_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
is_live_connected = False

if data_mode == "Live SQL Server":
    try:
        funds_df, nav_df, tx_df = load_db_data(server_input, db_input, driver_choice)
        is_live_connected = True
        status_badge = '<span class="badge-pill-positive">🟢 Live SQL Server</span>'
    except Exception as e:
        status_badge = '<span class="badge-pill-alert">⚠️ Demo Mode (SQL Offline)</span>'
        funds_df, nav_df, tx_df = get_sample_data()
else:
    funds_df, nav_df, tx_df = get_sample_data()
    status_badge = '<span class="badge-pill-neutral">🔵 Demo Benchmark Mode</span>'


# ==============================================================================
# Hero Header
# ==============================================================================
st.markdown(f"""
<div class="hero-container">
    <div>
        <div class="hero-title">📈 Mutual Fund Investment Analytics</div>
        <div class="hero-subtitle">Automated NAV Ingestion · Quantitative Dip Detection · Portfolio Performance & Asset Allocation</div>
    </div>
    <div>
        {status_badge}
    </div>
</div>
""", unsafe_allow_html=True)


# Tabs Navigation
tab1, tab2, tab3 = st.tabs([
    "🎯 Buy Opportunities (Decision Engine)",
    "📊 Portfolio Performance & Asset Allocation",
    "⚡ Management & Operations Hub"
])


# ==============================================================================
# TAB 1: BUY OPPORTUNITY DASHBOARD (Decision Intelligence Engine)
# ==============================================================================
with tab1:
    if funds_df.empty or nav_df.empty:
        st.warning("No active funds or historical NAV records found.")
    else:
        latest_date = nav_df['NAVDate'].max()
        current_year = latest_date.year
        current_month = latest_date.month

        # Group and calculate metrics
        eval_records = []
        for _, fund in funds_df.iterrows():
            fid = fund['FundID']
            fund_navs = nav_df[nav_df['FundID'] == fid].sort_values('NAVDate')
            if fund_navs.empty:
                continue

            latest_nav_row = fund_navs.iloc[-1]
            latest_nav = latest_nav_row['NAV']
            latest_nav_date = latest_nav_row['NAVDate']

            # Reference NAV (first NAV of the current month)
            month_navs = fund_navs[
                fund_navs['NAVDate'].apply(lambda d: d.year == current_year and d.month == current_month)
            ]
            ref_nav = month_navs.iloc[0]['NAV'] if not month_navs.empty else fund_navs.iloc[0]['NAV']

            # Change % and recommendation
            change_pct = ((latest_nav - ref_nav) / ref_nav) * 100.0
            threshold = float(fund['AlertThreshold'])
            is_buy = change_pct <= threshold
            recommendation = "Buy" if is_buy else "Wait"

            eval_records.append({
                'FundID': fid,
                'FundName': fund['FundName'],
                'AMC': fund['AMC'],
                'FundCategory': fund['FundCategory'],
                'Latest NAV': latest_nav,
                'Reference NAV': ref_nav,
                'Change %': change_pct,
                'Alert Threshold': threshold,
                'Recommendation': recommendation,
                'IsBuy': is_buy,
                'LatestNAVDate': latest_nav_date
            })

        eval_df = pd.DataFrame(eval_records)
        buy_count = int(eval_df['IsBuy'].sum())

        # Top Metric Cards (Custom HTML FinTech Cards)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-label">Valuation Date</span>
                    <div class="kpi-icon-badge" style="background: #EFF6FF; color: #3B82F6;">📅</div>
                </div>
                <div class="kpi-value">{latest_date.strftime("%d %b %Y")}</div>
                <div class="kpi-footer">
                    <span class="badge-pill-positive">✓ Latest AMFI Feed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-label">Funds Monitored</span>
                    <div class="kpi-icon-badge" style="background: #F5F3FF; color: #8B5CF6;">📋</div>
                </div>
                <div class="kpi-value">{len(eval_df)} Schemes</div>
                <div class="kpi-footer">
                    <span class="badge-pill-neutral">{eval_df['AMC'].nunique()} Asset Managers</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            badge_class = "badge-pill-positive" if buy_count > 0 else "badge-pill-neutral"
            delta_text = f"🚨 {buy_count} Tactical Entry Triggered" if buy_count > 0 else "No threshold breaches"
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {'#10B981' if buy_count > 0 else '#CBD5E1'};">
                <div class="kpi-header">
                    <span class="kpi-label">Buy Opportunities</span>
                    <div class="kpi-icon-badge" style="background: {'#ECFDF5' if buy_count > 0 else '#F8FAFC'}; color: {'#10B981' if buy_count > 0 else '#64748B'};">🎯</div>
                </div>
                <div class="kpi-value" style="color: {'#059669' if buy_count > 0 else '#0F172A'};">{buy_count}</div>
                <div class="kpi-footer">
                    <span class="{badge_class}">{delta_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # Highlight Active Buy Signals Section
        if buy_count > 0:
            st.markdown("### 🚨 Active Tactical Buy Signals")
            st.caption("The following funds have dipped beyond their configured monthly alert thresholds:")
            buy_funds = eval_df[eval_df['IsBuy']]
            for _, b_row in buy_funds.iterrows():
                st.markdown(f"""
                <div class="signal-card">
                    <div>
                        <div style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">{b_row['FundName']}</div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">
                            Category: <b>{b_row['FundCategory']}</b> · AMC: <b>{b_row['AMC']}</b> · Month-Start NAV: <b>₹{b_row['Reference NAV']:.2f}</b> → Current NAV: <b>₹{b_row['Latest NAV']:.2f}</b>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Monthly Dip</div>
                            <div style="font-size: 1.1rem; font-weight: 800; color: #E11D48;">{b_row['Change %']:.2f}%</div>
                            <div style="font-size: 0.75rem; color: #94A3B8;">Threshold: {b_row['Alert Threshold']:.1f}%</div>
                        </div>
                        <div class="badge-buy-glow">✓ BUY SIGNAL</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Filters Toolbar
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        with st.container():
            f1, f2, f3 = st.columns([2, 1, 1])
            with f1:
                search_query = st.text_input("🔍 Search Funds", placeholder="Type fund name or AMC...", label_visibility="collapsed")
            with f2:
                cat_options = ["All Categories"] + sorted(eval_df['FundCategory'].dropna().unique().tolist())
                sel_cat = st.selectbox("Category", cat_options, label_visibility="collapsed")
            with f3:
                amc_options = ["All AMCs"] + sorted(eval_df['AMC'].dropna().unique().tolist())
                sel_amc = st.selectbox("AMC", amc_options, label_visibility="collapsed")

        # Apply Filters
        filtered_df = eval_df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df['FundName'].str.contains(search_query, case=False, na=False)]
        if sel_cat != "All Categories":
            filtered_df = filtered_df[filtered_df['FundCategory'] == sel_cat]
        if sel_amc != "All AMCs":
            filtered_df = filtered_df[filtered_df['AMC'] == sel_amc]

        # Table Display
        st.markdown("### 📋 Watchlist & Decision Matrix")
        table_data = filtered_df[['FundName', 'Latest NAV', 'Reference NAV', 'Change %', 'Alert Threshold', 'Recommendation']].copy()

        def style_decision_table(row):
            styles = [''] * len(row)
            rec_i = row.index.get_loc('Recommendation')
            chg_i = row.index.get_loc('Change %')

            if row['Recommendation'] == 'Buy':
                styles[rec_i] = 'background-color: #DEF7EC; color: #03543F; font-weight: 800; text-align: center; border-radius: 6px;'
            else:
                styles[rec_i] = 'background-color: #FEF3C7; color: #92400E; font-weight: 700; text-align: center; border-radius: 6px;'

            if row['Change %'] < 0:
                styles[chg_i] = 'color: #E11D48; font-weight: 700;'
            else:
                styles[chg_i] = 'color: #059669; font-weight: 700;'
            return styles

        styled_t = table_data.style\
            .format({
                'Latest NAV': '₹{:.2f}',
                'Reference NAV': '₹{:.2f}',
                'Change %': '{:+.2f}%',
                'Alert Threshold': '{:.2f}%'
            })\
            .apply(style_decision_table, axis=1)

        st.dataframe(styled_t, use_container_width=True, height=min(380, 50 + len(table_data) * 36))

        # Interactive Trend Line Chart
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📉 Historical NAV Spline Trend")
        st.caption("Select any mutual fund to plot its historical NAV time-series against the month-start reference benchmark.")

        trend_list = filtered_df['FundName'].tolist()
        if trend_list:
            chosen_fund = st.selectbox("Selected Scheme", trend_list)
            target_row = filtered_df[filtered_df['FundName'] == chosen_fund].iloc[0]
            target_fid = target_row['FundID']
            target_ref = target_row['Reference NAV']

            history_pts = nav_df[nav_df['FundID'] == target_fid].sort_values('NAVDate')

            fig_trend = go.Figure()
            # Gradient Area Fill
            fig_trend.add_trace(go.Scatter(
                x=history_pts['NAVDate'],
                y=history_pts['NAV'],
                mode='lines+markers',
                name='Daily NAV',
                line=dict(color='#4F46E5', width=3, shape='spline'),
                marker=dict(size=7, color='#312E81', symbol='circle'),
                fill='tozeroy',
                fillcolor='rgba(79, 70, 229, 0.08)',
                hovertemplate='<b>%{x|%d %b %Y}</b><br>Closing NAV: ₹%{y:.4f}<extra></extra>'
            ))
            # Reference NAV benchmark line
            fig_trend.add_hline(
                y=target_ref,
                line_dash="dash",
                line_color="#EF4444",
                line_width=2,
                annotation_text=f"Month Start Benchmark: ₹{target_ref:.2f}",
                annotation_position="bottom right",
                annotation_font=dict(color="#B91C1C", size=11, family="Inter")
            )
            fig_trend.update_layout(
                title=dict(text=f"NAV Trajectory — {chosen_fund}", font=dict(family="Inter", size=16, weight="bold")),
                xaxis=dict(title="Valuation Date", gridcolor="#F1F5F9", showgrid=True),
                yaxis=dict(title="Net Asset Value (₹)", gridcolor="#F1F5F9", showgrid=True),
                hovermode="x unified",
                height=400,
                template="plotly_white",
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig_trend, use_container_width=True)


# ==============================================================================
# TAB 2: PORTFOLIO PERFORMANCE DASHBOARD (Valuation & Asset Allocation)
# ==============================================================================
with tab2:
    if tx_df.empty:
        st.info("No transaction history available. Use the Management Hub tab to record your investments.")
    else:
        latest_nav_map = nav_df.sort_values('NAVDate').groupby('FundID').last().reset_index()[['FundID', 'NAV']]
        latest_nav_map.rename(columns={'NAV': 'LatestNAV'}, inplace=True)

        tx_calc = tx_df.copy()
        tx_calc['SignedUnits'] = tx_calc.apply(lambda r: r['Units'] if r['TransactionType'].upper() == 'BUY' else -r['Units'], axis=1)
        tx_calc['SignedAmount'] = tx_calc.apply(lambda r: r['Amount'] if r['TransactionType'].upper() == 'BUY' else -r['Amount'], axis=1)

        holdings = tx_calc.groupby('FundID').agg(
            TotalInvested=('SignedAmount', 'sum'),
            TotalUnits=('SignedUnits', 'sum')
        ).reset_index()

        holdings = holdings.merge(funds_df[['FundID', 'FundName', 'AMC', 'FundCategory']], on='FundID', how='inner')
        holdings = holdings.merge(latest_nav_map, on='FundID', how='left')
        holdings['LatestNAV'] = holdings['LatestNAV'].fillna(0.0)

        holdings['AvgBuyNAV'] = np.where(holdings['TotalUnits'] > 0, holdings['TotalInvested'] / holdings['TotalUnits'], 0.0)
        holdings['CurrentValue'] = holdings['TotalUnits'] * holdings['LatestNAV']
        holdings['UnrealizedGain'] = holdings['CurrentValue'] - holdings['TotalInvested']
        holdings['ReturnPct'] = np.where(
            holdings['TotalInvested'] > 0,
            (holdings['UnrealizedGain'] / holdings['TotalInvested']) * 100.0,
            0.0
        )

        tot_inv = holdings['TotalInvested'].sum()
        tot_val = holdings['CurrentValue'].sum()
        tot_pnl = tot_val - tot_inv
        tot_ret = (tot_pnl / tot_inv * 100.0) if tot_inv > 0 else 0.0

        # Executive FinTech KPI Scorecards
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-label">Capital Invested</span>
                    <div class="kpi-icon-badge" style="background: #F1F5F9; color: #475569;">💰</div>
                </div>
                <div class="kpi-value">₹{tot_inv/1000:,.2f}K</div>
                <div class="kpi-footer">
                    <span class="badge-pill-neutral">₹{tot_inv:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-label">Portfolio Valuation</span>
                    <div class="kpi-icon-badge" style="background: #EEF2FF; color: #4F46E5;">💼</div>
                </div>
                <div class="kpi-value" style="color: #4F46E5;">₹{tot_val/1000:,.2f}K</div>
                <div class="kpi-footer">
                    <span class="badge-pill-neutral">₹{tot_val:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            pnl_badge = "badge-pill-positive" if tot_ret >= 0 else "badge-pill-alert"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-label">Portfolio Return</span>
                    <div class="kpi-icon-badge" style="background: {'#ECFDF5' if tot_ret >= 0 else '#FEF2F2'}; color: {'#10B981' if tot_ret >= 0 else '#EF4444'};">📈</div>
                </div>
                <div class="kpi-value" style="color: {'#059669' if tot_ret >= 0 else '#DC2626'};">{tot_ret:+.2f}%</div>
                <div class="kpi-footer">
                    <span class="{pnl_badge}">{'▲ Positive Alpha' if tot_ret >= 0 else '▼ Underperforming'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-label">Unrealized Gain / Loss</span>
                    <div class="kpi-icon-badge" style="background: {'#ECFDF5' if tot_pnl >= 0 else '#FEF2F2'}; color: {'#10B981' if tot_pnl >= 0 else '#EF4444'};">💵</div>
                </div>
                <div class="kpi-value" style="color: {'#059669' if tot_pnl >= 0 else '#DC2626'};">₹{tot_pnl/1000:+,.2f}K</div>
                <div class="kpi-footer">
                    <span class="{pnl_badge}">Net P&L: ₹{tot_pnl:+,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # Asset Allocation Visualizations (Treemap & Donut)
        c_tree, c_pie = st.columns(2)

        with c_tree:
            st.markdown("#### 📦 Capital Allocation by Category")
            cat_sum = holdings.groupby('FundCategory')['TotalInvested'].sum().reset_index()
            fig_tree = px.treemap(
                cat_sum,
                path=['FundCategory'],
                values='TotalInvested',
                color='TotalInvested',
                color_continuous_scale='Tealgrn'
            )
            fig_tree.update_traces(
                textinfo="label+value+percent root",
                textfont=dict(family="Inter", size=13),
                hovertemplate='<b>%{label}</b><br>Capital: ₹%{value:,.2f}<br>Share: %{percentRoot:.1%}<extra></extra>'
            )
            fig_tree.update_layout(margin=dict(t=20, l=10, r=10, b=10), height=340)
            st.plotly_chart(fig_tree, use_container_width=True)

        with c_pie:
            st.markdown("#### 🏢 Capital Distribution by AMC")
            amc_sum = holdings.groupby('AMC')['TotalInvested'].sum().reset_index()
            fig_donut = px.pie(
                amc_sum,
                names='AMC',
                values='TotalInvested',
                hole=0.6,
                color_discrete_sequence=['#4F46E5', '#06B6D4', '#F59E0B', '#8B5CF6']
            )
            fig_donut.update_traces(
                textinfo='percent+label',
                textfont=dict(family="Inter", size=12),
                hovertemplate='<b>%{label}</b><br>Invested: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>'
            )
            fig_donut.update_layout(
                margin=dict(t=20, l=10, r=10, b=10),
                height=340,
                annotations=[dict(text=f'Total<br><b>₹{tot_inv/1000:.0f}K</b>', x=0.5, y=0.5, font_size=16, font_family="Inter", showarrow=False)]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Holdings Detail Table
        st.markdown("### 📋 Portfolio Holdings Matrix")
        htable = holdings[[
            'FundName', 'TotalInvested', 'TotalUnits', 'AvgBuyNAV',
            'LatestNAV', 'CurrentValue', 'ReturnPct', 'UnrealizedGain'
        ]].copy()

        htable.rename(columns={
            'FundName': 'Fund Name',
            'TotalInvested': 'Invested Capital',
            'TotalUnits': 'Units Held',
            'AvgBuyNAV': 'Avg Buy NAV',
            'LatestNAV': 'Closing NAV',
            'CurrentValue': 'Current Value',
            'ReturnPct': 'Return %',
            'UnrealizedGain': 'Unrealized P&L'
        }, inplace=True)

        def style_holdings_matrix(row):
            styles = [''] * len(row)
            ret_idx = row.index.get_loc('Return %')
            pnl_idx = row.index.get_loc('Unrealized P&L')

            if row['Unrealized P&L'] >= 0:
                styles[ret_idx] = 'background-color: #DEF7EC; color: #03543F; font-weight: 800;'
                styles[pnl_idx] = 'background-color: #DEF7EC; color: #03543F; font-weight: 800;'
            else:
                styles[ret_idx] = 'background-color: #FDE8E8; color: #9B1C1C; font-weight: 800;'
                styles[pnl_idx] = 'background-color: #FDE8E8; color: #9B1C1C; font-weight: 800;'
            return styles

        styled_holdings = htable.style\
            .format({
                'Invested Capital': '₹{:,.2f}',
                'Units Held': '{:,.2f}',
                'Avg Buy NAV': '₹{:.2f}',
                'Closing NAV': '₹{:.2f}',
                'Current Value': '₹{:,.2f}',
                'Return %': '{:+.2f}%',
                'Unrealized P&L': '₹{:+,.2f}'
            })\
            .apply(style_holdings_matrix, axis=1)

        st.dataframe(styled_holdings, use_container_width=True)


# ==============================================================================
# TAB 3: MANAGEMENT & OPERATIONS HUB
# ==============================================================================
with tab3:
    st.markdown("### ⚡ Administrative Control Center")
    st.caption("Manage data pipelines, onboard mutual fund schemes, and execute trades directly from the browser.")

    h_col1, h_col2 = st.columns(2)

    with h_col1:
        st.markdown("""
        <div class="section-card">
            <h4 style="margin: 0 0 8px 0; color: #0F172A;">🔄 Automated Daily NAV Ingestion</h4>
            <p style="font-size: 0.88rem; color: #64748B; margin-bottom: 16px;">
                Fetch daily NAV files published by AMFI, match active schemes in FundMaster, and append updates to NAVHistory.
            </p>
        """, unsafe_allow_html=True)

        if st.button("🚀 Execute Daily ETL Batch", type="primary", use_container_width=True):
            if not is_live_connected:
                st.warning("⚠️ Live SQL Server connection is required to write ETL updates.")
            else:
                p_bar = st.progress(0, text="Requesting AMFI feed...")
                try:
                    amfi_res = requests.get("https://www.amfiindia.com/spages/NAVAll.txt", timeout=30)
                    p_bar.progress(35, text="Parsing semicolon CSV...")
                    amfi_data = pd.read_csv(io.StringIO(amfi_res.text), sep=";", on_bad_lines="skip")
                    amfi_data = amfi_data.dropna(subset=["Net Asset Value"])
                    amfi_data["SchemeCode"] = amfi_data["Scheme Code"].astype(str)

                    p_bar.progress(60, text="Filtering active portfolio...")
                    conn = pyodbc.connect(get_connection_string(server_input, db_input, driver_choice))
                    f_master = pd.read_sql("SELECT FundID, SchemeCode FROM dbo.FundMaster WHERE IsActive = 1", conn)
                    f_master["SchemeCode"] = f_master["SchemeCode"].astype(str)

                    merged = pd.merge(f_master, amfi_data, on="SchemeCode", how="inner")
                    merged["Date"] = pd.to_datetime(merged["Date"], format="%d-%b-%Y").dt.date

                    p_bar.progress(80, text="Loading into SQL Server...")
                    cursor = conn.cursor()
                    ins_q = "INSERT INTO dbo.NAVHistory (FundID, NAV, NAVDate) VALUES (?, ?, ?)"
                    inserted, skipped = 0, 0

                    for _, r in merged.iterrows():
                        try:
                            cursor.execute(ins_q, r["FundID"], float(r["Net Asset Value"]), r["Date"])
                            inserted += 1
                        except pyodbc.IntegrityError:
                            skipped += 1

                    conn.commit()
                    cursor.close()
                    conn.close()

                    p_bar.progress(100, text="Completed!")
                    st.success(f"✅ ETL Batch Finished! Records Inserted: {inserted} | Skipped (Existing): {skipped}")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()

                except Exception as ex:
                    st.error(f"❌ ETL Pipeline Error: {ex}")

        st.markdown("</div>", unsafe_allow_html=True)

    with h_col2:
        st.markdown("""
        <div class="section-card">
            <h4 style="margin: 0 0 8px 0; color: #0F172A;">➕ Onboard New Mutual Fund</h4>
            <p style="font-size: 0.88rem; color: #64748B; margin-bottom: 16px;">
                Enter an AMFI Scheme Code to verify metadata and register the fund for daily tracking.
            </p>
        """, unsafe_allow_html=True)

        with st.form("onboard_fund_form"):
            in_code = st.text_input("AMFI Scheme Code (e.g., 119551):")
            in_cat = st.text_input("Category (e.g., Index, Large Cap, Mid Cap):", value="Index")
            in_sip = st.number_input("Configured Monthly SIP Day (1-31):", min_value=1, max_value=31, value=10)
            in_thresh = st.number_input("Alert Dip Threshold % (e.g. -2.0 for 2% dip):", value=-2.0, step=0.5)

            sub_reg = st.form_submit_button("Verify & Register Scheme")

            if sub_reg:
                if not in_code.strip():
                    st.warning("Please specify a valid Scheme Code.")
                elif not is_live_connected:
                    st.warning("⚠️ Live SQL Server connection is required to register new funds.")
                else:
                    try:
                        st.info("Verifying scheme code with AMFI...")
                        res = requests.get("https://www.amfiindia.com/spages/NAVAll.txt", timeout=30)
                        raw = pd.read_csv(io.StringIO(res.text), sep=";", on_bad_lines="skip")
                        raw["Scheme Code"] = raw["Scheme Code"].astype(str)

                        matched = raw[raw["Scheme Code"] == in_code.strip()]
                        if matched.empty:
                            st.error(f"❌ Scheme Code '{in_code}' not found in AMFI directory.")
                        else:
                            s_name = matched.iloc[0]["Scheme Name"]
                            isin_g = matched.iloc[0]["ISIN Div Payout/ ISIN Growth"]
                            isin_r = matched.iloc[0]["ISIN Div Reinvestment"]

                            if s_name.startswith("HDFC"): amc_name = "HDFC"
                            elif s_name.startswith("ICICI"): amc_name = "ICICI"
                            elif s_name.startswith("Nippon"): amc_name = "Nippon"
                            elif s_name.startswith("UTI"): amc_name = "UTI"
                            else: amc_name = "Other"

                            conn = pyodbc.connect(get_connection_string(server_input, db_input, driver_choice))
                            cur = conn.cursor()
                            cur.execute(
                                """
                                INSERT INTO dbo.FundMaster
                                (SchemeCode, FundName, AMC, FundCategory, ISINGrowth, ISINReinvestment, ConfiguredSIPDay, AlertThreshold)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                """,
                                int(in_code), s_name, amc_name, in_cat, isin_g, isin_r, in_sip, in_thresh
                            )
                            conn.commit()
                            cur.close()
                            conn.close()

                            st.success(f"✅ Scheme Registered: '{s_name}'!")
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()

                    except Exception as ex:
                        st.error(f"❌ Error onboarding fund: {ex}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Record Trade Section
    st.markdown("""
    <div class="section-card">
        <h4 style="margin: 0 0 8px 0; color: #0F172A;">📝 Record Investment Trade</h4>
        <p style="font-size: 0.88rem; color: #64748B; margin-bottom: 16px;">
            Log BUY or SELL transactions. Units allocated will be auto-calculated using the exact closing NAV on trade date.
        </p>
    """, unsafe_allow_html=True)

    if not funds_df.empty:
        fund_lookup = {f"{row['FundID']} - {row['FundName']}": row['FundID'] for _, row in funds_df.iterrows()}
        with st.form("trade_entry_form"):
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                sel_f = st.selectbox("Mutual Fund Scheme", list(fund_lookup.keys()))
                tx_fid = fund_lookup[sel_f]
            with tc2:
                tx_act = st.selectbox("Transaction Type", ["BUY", "SELL"])
            with tc3:
                tx_dt = st.date_input("Execution Date", value=date.today())

            tc4, tc5 = st.columns(2)
            with tc4:
                tx_amount = st.number_input("Invested Capital (₹)", min_value=100.0, value=5000.0, step=500.0)
            with tc5:
                matched_nav = nav_df[(nav_df['FundID'] == tx_fid) & (nav_df['NAVDate'] == tx_dt)]
                if not matched_nav.empty:
                    c_nav = matched_nav.iloc[0]['NAV']
                    st.write(f"**Closing NAV:** ₹{c_nav:.4f}")
                    st.write(f"**Allocated Units:** {tx_amount / c_nav:.6f}")
                else:
                    st.caption("No historical NAV found for date. Enter manual NAV:")
                    c_nav = st.number_input("Closing NAV (₹)", min_value=0.01, value=10.0, step=0.1)
                    st.write(f"**Allocated Units:** {tx_amount / c_nav:.6f}")

            sub_trade = st.form_submit_button("Confirm & Record Order")

            if sub_trade:
                if not is_live_connected:
                    st.warning("⚠️ Live SQL Server connection is required to record trades.")
                else:
                    try:
                        conn = pyodbc.connect(get_connection_string(server_input, db_input, driver_choice))
                        cur = conn.cursor()
                        calc_u = round(tx_amount / c_nav, 6)
                        cur.execute(
                            """
                            INSERT INTO dbo.Transactions
                            (FundID, TransactionDate, TransactionType, Amount, NAV, Units)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            tx_fid, tx_dt, tx_act, tx_amount, c_nav, calc_u
                        )
                        conn.commit()
                        cur.close()
                        conn.close()

                        st.success(f"✅ Trade Recorded! {calc_u:.6f} Units at ₹{c_nav:.4f}")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()

                    except Exception as ex:
                        st.error(f"❌ Error submitting transaction: {ex}")

    st.markdown("</div>", unsafe_allow_html=True)
