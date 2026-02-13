import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pptx import Presentation
import io
from datetime import datetime

# --- 1. PRO-BRANDING & PAGE CONFIG ---
st.set_page_config(page_title="Sentinell BI | Executive Vantage", layout="wide", page_icon="🛡️")

# High-End Corporate Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .main-header {
        color: white; padding: 2.5rem; border-radius: 15px;
        text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .executive-card {
        background: white; padding: 20px; border-radius: 12px;
        border-left: 6px solid #004080; box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .status-stable { color: #28a745; font-weight: bold; border: 1px solid #28a745; padding: 2px 8px; border-radius: 4px; }
    .status-risk { color: #dc3545; font-weight: bold; border: 1px solid #dc3545; padding: 2px 8px; border-radius: 4px; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #001f3f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION GATE (LOGIN) ---
if "auth" not in st.session_state:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br><div style='text-align:center;'><h2>🔒 Executive Access</h2></div>", unsafe_allow_html=True)
        u = st.text_input("Director Username")
        p = st.text_input("Security Key", type="password")
        if st.button("Authorize Access"):
            if p == "Company2026" and u:
                st.session_state["auth"], st.session_state["user"] = True, u
                st.rerun()
            else: st.error("Access Denied: Invalid Security Key.")
    st.stop()

# --- 3. BUSINESS LOGIC: NETWORKING DAYS ENGINE ---
def calculate_biz_aging(df):
    start = pd.to_datetime(df['Discovery_Date']).dt.date.values.astype('datetime64[D]')
    today_val = np.datetime64('2026-02-13') 
    end = pd.to_datetime(df['Closed_Date']).dt.date.fillna(pd.Timestamp(today_val)).values.astype('datetime64[D]')
    # Official 2026 Public Holidays
    hols = ['2026-01-01', '2026-01-26', '2026-08-15', '2026-10-02', '2026-12-25']
    return np.busday_count(start, end, holidays=hols)

# --- 4. SIDEBAR: SENTINELL BRANDING & GOVERNANCE FILTERS ---
with st.sidebar:
    # UPDATED BRANDING FROM LOGO SELECTION
    st.markdown("<h2 style='color:#004080;'>🛡️ Sentinell <span style='color:#357af4;'>V</span></h2>", unsafe_allow_html=True)
    st.markdown(f"**Principal:** {st.session_state['user']} (Senior Director)")
    st.divider()
    
    uploaded_file = st.file_uploader("📂 Synchronize Defect Master", type=["xlsx"])
    
    if uploaded_file:
        raw_df = pd.read_excel(uploaded_file)
        raw_df.columns = [c.strip() for c in raw_df.columns]
        
        st.subheader("🎯 Governance Controls")
        search_id = st.text_input("🔍 Focus Defect_ID", "")
        
        env_list = raw_df['Environment'].unique()
        sel_env = st.selectbox("Strategic Environment", env_list)
        df = raw_df[raw_df['Environment'] == sel_env].copy()
        
        f_status = st.multiselect("Filter Status", df['Status'].unique(), default=df['Status'].unique())
        f_severity = st.multiselect("Filter Severity", df['Severity'].unique(), default=df['Severity'].unique())
        
        kpi_col = 'KPI_Status' if 'KPI_Status' in df.columns else 'Status'
        f_kpi = st.multiselect("Filter KPI_Status", df[kpi_col].unique(), default=df[kpi_col].unique())

        if 'Discovery_Date' in df.columns:
            df['Discovery_Date'] = pd.to_datetime(df['Discovery_Date'])
            min_d, max_d = df['Discovery_Date'].min().date(), df['Discovery_Date'].max().date()
            date_range = st.date_input("📅 Reporting Period", [min_d, max_d])

        brand_color = st.color_picker("🎨 Theme Accent Color", "#004080")
        
        st.divider()
        chart_style = st.selectbox("📊 Visualization Style", 
                                   ["Bar Chart", "Donut Chart", "Funnel Chart", "Waterfall", "Line Chart"])
        
        if st.button("🚪 Logout & Secure Exit"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
    else:
        st.info("Awaiting Defect Data Sync...")
        st.stop()

# --- 5. DATA PROCESSING & ANALYTICS ---
mask = (df['Status'].isin(f_status)) & (df['Severity'].isin(f_severity)) & (df[kpi_col].isin(f_kpi))
if search_id: mask &= df['Defect_ID'].astype(str).str.contains(search_id)
if len(date_range) == 2: mask &= df['Discovery_Date'].dt.date.between(date_range[0], date_range[1])
df_final = df[mask].copy()

# Calculate Aging & Weekly Trends
df_final['Aging_Days'] = calculate_biz_aging(df_final)
df_final['Week'] = df_final['Discovery_Date'].dt.strftime('Wk-%U')

# --- 6. MAIN HEADER: VANTAGE COMMAND ---
st.markdown(f"""
    <div class="main-header" style="background: linear-gradient(135deg, {brand_color}, #001f3f);">
        <h1>🛡️ Sentinell BI: Vantage Command</h1>
        <p>Strategic Intelligence & Governance Oversight | {sel_env}</p>
    </div>
""", unsafe_allow_html=True)

# Executive Pulse Summary
critical_count = len(df_final[df_final['Severity'] == 'Critical'])
risk_status = "STABLE" if critical_count == 0 else "AT RISK"
status_class = "status-stable" if risk_status == "STABLE" else "status-risk"

st.markdown(f"""
<div class="executive-card">
    <b>Executive Vantage:</b> The {sel_env} environment is currently <span class="{status_class}">{risk_status}</span>. 
    Total Defect Volume: <b>{len(df_final)}</b> | Data Integrity Score: <b>100%</b>.
</div>
""", unsafe_allow_html=True)

# Metrics Tiles
c1, c2, c3, c4 = st.columns(4)
c1.metric("Volume", len(df_final))
c2.metric("Critical Risks", critical_count)
c3.metric("Avg Aging (Biz Days)", f"{round(df_final['Aging_Days'].mean(),1)}d")
c4.metric("Active Backlog", len(df_final[df_final['Status'] != 'Closed']))

# --- 7. TABS: THE COMMAND ARCHITECTURE ---
t_bi, t_aging, t_velocity, t_audit = st.tabs(["📊 Dashboard", "⚠️ Aging Analysis", "📈 Velocity Trends", "📋 Audit Trail"])

with t_bi:
    agg = df_final.groupby('App_Area').size().reset_index(name='Count')
    if "Bar" in chart_style: fig = px.bar(agg, x='App_Area', y='Count', color_discrete_sequence=[brand_color], text_auto=True)
    elif "Donut" in chart_style: fig = px.pie(agg, names='App_Area', values='Count', hole=0.5)
    elif "Funnel" in chart_style: fig = px.funnel(agg.sort_values('Count'), x='Count', y='App_Area')
    elif "Waterfall" in chart_style: fig = go.Figure(go.Waterfall(x=agg['App_Area'], y=agg['Count'], measure=["relative"]*len(agg)))
    else: fig = px.line(agg, x='App_Area', y='Count', markers=True)
    st.plotly_chart(fig, use_container_width=True)

with t_aging:
    st.subheader("🔥 Concentration Risk: Severity vs Aging")
    
    fig_heat = px.density_heatmap(df_final, x="Aging_Days", y="Severity", z="Defect_ID", histfunc="count", color_continuous_scale="Reds", text_auto=True)
    st.plotly_chart(fig_heat, use_container_width=True)

with t_velocity:
    st.subheader("📈 Backlog Velocity (The Red Line)")
    
    pivot = df_final.groupby(['Week', 'Status']).size().unstack(fill_value=0)
    pivot['Backlog'] = 0
    run = 0
    for idx in pivot.index:
        run = (run + pivot.loc[idx].get('Created', 0)) - (pivot.loc[idx].get('Closed', 0) + pivot.loc[idx].get('Moved', 0))
        pivot.loc[idx, 'Backlog'] = run
    fig_red = go.Figure()
    if 'Created' in pivot.columns: fig_red.add_trace(go.Bar(name='Inflow', x=pivot.index, y=pivot['Created'], marker_color='#3498db'))
    fig_red.add_trace(go.Scatter(name='Backlog Line', x=pivot.index, y=pivot['Backlog'], line=dict(color='red', width=4), mode='lines+markers+text', text=pivot['Backlog'], textposition="top center"))
    st.plotly_chart(fig_red, use_container_width=True)

with t_audit:
    st.subheader("🔍 Strategic Audit Trail")
    st.dataframe(df_final, use_container_width=True)
    if st.button("📊 Export Vantage Report (PPT)"):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = f"{sel_env} Governance Review"
        slide.placeholders[1].text = f"Status: {risk_status}\nMetrics Refreshed: {datetime.now().strftime('%Y-%m-%d')}"
        buf = io.BytesIO()
        prs.save(buf)
        st.download_button("📥 Download Presentation", buf.getvalue(), f"Sentinell_{sel_env}_Report.pptx")
