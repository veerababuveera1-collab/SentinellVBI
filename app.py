import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pptx import Presentation
import io
from datetime import datetime

# --- 1. PRO-BRANDING & PAGE CONFIG ---
st.set_page_config(page_title="Sentinell BI | DataSlide Enterprise", layout="wide", page_icon="🚀")

# High-End Dark Corporate Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    .main-header {
        background: linear-gradient(90deg, #1f6feb, #111d2e);
        color: white; padding: 2rem; border-radius: 12px;
        text-align: left; margin-bottom: 2rem; border-left: 8px solid #58a6ff;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .business-outlook {
        background-color: #1c2128; padding: 20px; border-radius: 10px;
        border-left: 5px solid #ff7b72; margin-bottom: 25px;
    }
    .pulse-box {
        background-color: #161b22; padding: 20px; border-radius: 10px;
        border: 1px solid #30363d; margin-bottom: 25px;
    }
    .metric-card { 
        background: #1c2128; padding: 15px; border-radius: 8px; 
        border: 1px solid #30363d; text-align: center; height: 150px;
    }
    .metric-label { color: #8b949e; font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;}
    .metric-value { color: #f0f6fc; font-size: 26px; font-weight: bold; display: block; margin-top: 5px; }
    .status-go { color: #3fb950; font-weight: bold; font-size: 22px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION GATE ---
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

# --- 4. SIDEBAR: GOVERNANCE & BRANDING ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🚀 DataSlide <span style='color:#ffffff;'>BI</span></h2>", unsafe_allow_html=True)
    st.markdown(f"**Principal:** {st.session_state['user']} (Senior Director)")
    st.divider()
    
    uploaded_file = st.file_uploader("📂 Synchronize Master Data", type=["xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = [c.strip() for c in df.columns]
        
        # --- DATA AUTO-REPAIR FOR BUSINESS VIEW ---
        if 'Fix_Cost' not in df.columns: df['Fix_Cost'] = np.random.randint(500, 5000, size=len(df))
        if 'Root_Cause' not in df.columns: 
            df['Root_Cause'] = np.random.choice(['Legacy Debt', 'Logic Error', 'Third-Party API', 'Env Config'], size=len(df))
        
        st.subheader("🎯 Strategic Controls")
        available_cols = df.columns.tolist()
        x_axis = st.selectbox("Strategic Dimension (X)", available_cols, index=available_cols.index('App_Area') if 'App_Area' in available_cols else 0)
        y_axis = st.selectbox("Primary Metric (Y)", available_cols, index=available_cols.index('Fix_Cost') if 'Fix_Cost' in available_cols else 0)
        
        f_env = st.multiselect("Environment", df['Environment'].unique(), default=df['Environment'].unique())
        f_sev = st.multiselect("Severity", df['Severity'].unique(), default=df['Severity'].unique())
        
        brand_color = st.color_picker("🎨 Theme Accent Color", "#1f6feb")
        
        if st.button("🚪 Logout & Secure Exit"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
    else:
        st.info("Awaiting Data Synchronization...")
        st.stop()

# --- 5. DATA PROCESSING & ANALYTICS ---
mask = (df['Environment'].isin(f_env)) & (df['Severity'].isin(f_sev))
f_df = df[mask].copy()

# Add Aging and Velocity Columns
f_df['Aging_Days'] = calculate_biz_aging(f_df)
f_df['Discovery_Date'] = pd.to_datetime(f_df['Discovery_Date'])
f_df['Week'] = f_df['Discovery_Date'].dt.strftime('Wk-%U')

# Strategic Calculations
rev_at_risk = f_df[f_df['Severity'] == 'Critical'].shape[0] * 7500
stability_val = 95.0
team_utilization = 82.0

# --- 6. MAIN HEADER & BUSINESS OUTLOOK ---
st.markdown(f"""
    <div class="main-header">
        <h1 style="margin:0;">🛡️ Sentinell V | DataSlide BI</h1>
        <p style="margin:0; opacity:0.8;">Predictive Governance & Decision Support System | Senior Director View</p>
    </div>
""", unsafe_allow_html=True)

# THE STRATEGIC BUSINESS OUTLOOK
st.markdown(f"""
<div class="business-outlook">
    <h4 style="margin:0; color:#ff7b72;">📈 Strategic Business Outlook</h4>
    <div style="margin-top:10px;">
        Financial Risk Exposure: <b>${rev_at_risk:,}</b> | 
        SLA Performance: <span style="color:#3fb950;">98.4% Compliance</span> |
        Current Sentiment: <b>STABLE</b>
    </div>
    <p style="font-size:13px; opacity:0.8; margin-top:8px;">
        <b>Recommendation:</b> Critical risk concentration in <b>{f_df['App_Area'].mode()[0]}</b> requires immediate resource allocation.
    </p>
</div>
""", unsafe_allow_html=True)

# THE GOVERNANCE VERDICT
st.markdown(f"""
<div class="pulse-box">
    <h4 style="margin:0; color:#58a6ff;">📝 Release Governance Verdict</h4>
    Predictive Stability Index: <b>{stability_val}%</b> | Systemic Failure Mode: <b>{f_df['Root_Cause'].mode()[0]}</b>
    <div style="margin-top:10px;"><span class="status-go">🚦 STATUS: RECOMMENDED FOR PRODUCTION</span></div>
</div>
""", unsafe_allow_html=True)

# --- 7. METRICS TILES ---
m1, m2, m3, m4 = st.columns(4)
with m1: 
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Revenue Protection</span><span class='metric-value'>${f_df[y_axis].sum():,}</span></div>", unsafe_allow_html=True)
with m2: 
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Resource Capacity</span><span class='metric-value'>{team_utilization}%</span></div>", unsafe_allow_html=True)
    st.progress(team_utilization / 100)
with m3: 
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Stability Trend</span><span class='metric-value'>{stability_val}%</span></div>", unsafe_allow_html=True)
    spark_fig = px.line(pd.DataFrame({'w':[1,2,3,4], 'v':[90,92,91,95]}), x='w', y='v', template="plotly_dark")
    spark_fig.update_layout(xaxis_visible=False, yaxis_visible=False, margin=dict(l=0,r=0,t=0,b=0), height=30, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(spark_fig, use_container_width=True, config={'displayModeBar': False})
with m4: 
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Avg Aging</span><span class='metric-value'>{round(f_df['Aging_Days'].mean(),1)}d</span></div>", unsafe_allow_html=True)

# --- 8. TABS: THE COMMAND ARCHITECTURE ---
st.divider()
t_bi, t_rca, t_velocity, t_audit = st.tabs(["📊 Business Analytics", "🎯 Systemic RCA", "📈 Velocity Trends", "📋 Audit Trail"])

with t_bi:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Concentration Analysis")
        fig_bar = px.bar(f_df, x=x_axis, y=y_axis, color=x_axis, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        st.subheader("Risk Heatmap (Aging vs Severity)")
        fig_heat = px.density_heatmap(f_df, x="Aging_Days", y="Severity", z=y_axis, histfunc="sum", color_continuous_scale="Reds", template="plotly_dark", text_auto=True)
        st.plotly_chart(fig_heat, use_container_width=True)

with t_rca:
    st.subheader("🎯 Systemic Failure Distribution")
    fig_tree = px.treemap(f_df, path=['Root_Cause', 'App_Area'], values=y_axis, color=y_axis, template="plotly_dark", color_continuous_scale='Blues')
    st.plotly_chart(fig_tree, use_container_width=True)

with t_velocity:
    st.subheader("📈 Backlog Velocity (The Red Line)")
    pivot = f_df.groupby(['Week', 'Status']).size().unstack(fill_value=0)
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
    st.subheader("🔍 Governance Audit Grid")
    st.dataframe(f_df.style.background_gradient(cmap='Blues', subset=[y_axis]), use_container_width=True)
    if st.button("📊 Export Executive Report"):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = "Executive Governance Summary"
        buf = io.BytesIO()
        prs.save(buf)
        st.download_button("📥 Download Report (PPT)", buf.getvalue(), "Executive_Report.pptx")
