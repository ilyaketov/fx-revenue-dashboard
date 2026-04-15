import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from datetime import datetime

st.set_page_config(
    page_title="FX Revenue Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* Canvas */
  --bg:        #EEF0F5;
  --bg2:       #FFFFFF;
  --bg3:       #F5F6FA;

  /* Ink */
  --ink:       #1A2333;
  --ink2:      #2D3A4A;
  --ink3:      #3D4E62;
  --ink4:      #8B99AB;
  --ink5:      #C0CAD4;

  /* Teal accent — main positive color (like the +2.3% in the reference) */
  --teal:      #13C9C2;
  --teal-dk:   #0DA8A2;
  --teal-bg:   #E6FAF9;
  --teal-bdr:  #9DE6E3;

  /* Blue — charts, primary interactive */
  --blue:      #4A9EF8;
  --blue-dk:   #2D82E0;
  --blue-bg:   #EBF4FF;
  --blue-bdr:  #A8CFFB;

  /* Purple — secondary chart color */
  --purple:    #9B74F5;
  --purple-dk: #7A54D8;
  --purple-bg: #F0EBFF;
  --purple-bdr:#C8B4FA;

  /* Sidebar */
  --sb-bg:     #243040;
  --sb-bg2:    #2E3D52;
  --sb-bdr:    rgba(255,255,255,0.08);
  --sb-tx:     #BDC9D8;
  --sb-tx2:    #7A8FA3;
  --sb-tx3:    #485E74;

  /* Semantic */
  --green:     #0DA89E;
  --green-bg:  #E6F9F8;
  --green-bdr: #9DE3DF;
  --red:       #EF4A6B;
  --red-bg:    #FEEAEE;
  --red-bdr:   #F9A8BC;
  --amber:     #F5A524;
  --amber-bg:  #FFF5E0;
  --amber-bdr: #FAD58A;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(26,35,51,0.06), 0 1px 2px rgba(26,35,51,0.04);
  --shadow:    0 2px 8px rgba(26,35,51,0.08), 0 1px 3px rgba(26,35,51,0.05);
  --shadow-md: 0 4px 16px rgba(26,35,51,0.10), 0 2px 6px rgba(26,35,51,0.06);
}

html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, sans-serif !important;
  background: var(--bg) !important;
  color: var(--ink) !important;
  -webkit-font-smoothing: antialiased !important;
}
.main .block-container {
  padding: 1.75rem 2.25rem 3rem !important;
  max-width: 1440px !important;
  background: var(--bg) !important;
}
.stApp { background: var(--bg) !important; }
h1,h2,h3,h4,h5,h6 { color: var(--ink) !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--sb-bg) !important;
  border-right: none !important;
  box-shadow: 2px 0 16px rgba(26,35,51,0.15) !important;
}
[data-testid="stSidebar"] * { color: var(--sb-tx) !important; }
[data-testid="stSidebar"] .stMarkdown h3 {
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: .16em !important;
  text-transform: uppercase !important;
  color: var(--sb-tx3) !important;
  margin: 1.4rem 0 .5rem !important;
  padding-bottom: 5px !important;
  border-bottom: 1px solid var(--sb-bdr) !important;
}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
  background: var(--sb-bg2) !important;
  border: 1px solid var(--sb-bdr) !important;
  border-radius: 6px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: rgba(74,158,248,0.3) !important;
  border-color: rgba(74,158,248,0.5) !important;
  color: #B0D8FD !important;
  border-radius: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
  border: 1.5px dashed var(--sb-bdr) !important;
  background: var(--sb-bg2) !important;
  border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
  border-color: rgba(74,158,248,0.5) !important;
  background: rgba(74,158,248,0.07) !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color: var(--sb-tx) !important; }
[data-testid="stSidebar"] hr { border-color: var(--sb-bdr) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg2) !important;
  border-bottom: 1px solid #E4E8EF !important;
  border-radius: 10px 10px 0 0 !important;
  padding: 0 4px !important;
  gap: 0 !important;
  box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -1px !important;
  border-radius: 0 !important;
  color: var(--ink3) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  padding: 14px 22px !important;
  transition: color .15s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink) !important; }
.stTabs [aria-selected="true"] {
  background: transparent !important;
  border-bottom: 2px solid var(--teal) !important;
  color: var(--teal-dk) !important;
  font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: transparent !important;
  padding: 1.5rem 0 !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--ink2) !important;
  color: #EEF3F8 !important;
  border: none !important;
  border-radius: 7px !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  padding: 8px 18px !important;
  box-shadow: var(--shadow-sm) !important;
  transition: background .15s, box-shadow .15s !important;
}
.stButton > button:hover {
  background: var(--ink) !important;
  box-shadow: var(--shadow) !important;
}
[data-testid="stDownloadButton"] > button {
  background: var(--bg2) !important;
  color: var(--blue-dk) !important;
  border: 1px solid var(--blue-bdr) !important;
  border-radius: 7px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  box-shadow: var(--shadow-sm) !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: var(--blue-bg) !important;
  border-color: var(--blue) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: var(--bg2) !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 20px 22px 16px !important;
  box-shadow: var(--shadow) !important;
}
[data-testid="stMetric"] > div:first-child {
  font-size: 10px !important;
  font-weight: 600 !important;
  letter-spacing: .08em !important;
  text-transform: uppercase !important;
  color: var(--ink3) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
  font-size: 30px !important;
  font-weight: 600 !important;
  color: var(--ink) !important;
  letter-spacing: -.03em !important;
}
/* Delta — green when positive */
[data-testid="stMetricDelta"] { font-size: 13px !important; font-weight: 600 !important; }
[data-testid="stMetricDelta"] svg { display: none !important; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
  background: var(--bg2) !important;
  border: none !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  box-shadow: var(--shadow) !important;
}

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid #E4E8EF !important; margin: .75rem 0 !important; }

/* ── Expanders ── */
details {
  background: var(--bg2) !important;
  border: 1px solid #E4E8EF !important;
  border-radius: 10px !important;
  padding: 4px 14px !important;
  box-shadow: var(--shadow-sm) !important;
}
summary { color: var(--ink3) !important; font-size: 13px !important; font-weight: 500 !important; }

/* ── Alerts ── */
[data-testid="stInfo"] {
  background: var(--blue-bg) !important; border: 1px solid var(--blue-bdr) !important;
  border-left: 3px solid var(--blue) !important; border-radius: 8px !important;
  color: var(--ink2) !important;
}
[data-testid="stSuccess"] {
  background: var(--green-bg) !important; border: 1px solid var(--green-bdr) !important;
  border-left: 3px solid var(--green) !important; border-radius: 8px !important;
  color: var(--green) !important;
}
[data-testid="stWarning"] {
  background: var(--amber-bg) !important; border: 1px solid var(--amber-bdr) !important;
  border-left: 3px solid var(--amber) !important; border-radius: 8px !important;
  color: var(--amber) !important;
}
[data-testid="stError"] {
  background: var(--red-bg) !important; border: 1px solid var(--red-bdr) !important;
  border-left: 3px solid var(--red) !important; border-radius: 8px !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg3); }
::-webkit-scrollbar-thumb { background: var(--ink5); border-radius: 3px; }

/* ── Cards ── */
.dash-card {
  background: var(--bg2);
  border-radius: 12px;
  padding: 20px 22px;
  margin-bottom: 1rem;
  box-shadow: var(--shadow);
}
.dash-card-teal {
  background: var(--bg2);
  border-radius: 12px;
  padding: 18px 22px;
  margin-bottom: 1rem;
  box-shadow: var(--shadow);
  border-top: 3px solid var(--teal);
}
.dash-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: .10em;
  text-transform: uppercase;
  color: var(--ink3);
  margin-bottom: 6px;
}
.fin-tag {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600; letter-spacing: .04em;
}
.tag-live   { background: var(--teal-bg);   color: var(--teal-dk);   border: 1px solid var(--teal-bdr); }
.tag-demo   { background: var(--blue-bg);   color: var(--blue-dk);   border: 1px solid var(--blue-bdr); }
.tag-rub    { background: var(--amber-bg);  color: var(--amber);     border: 1px solid var(--amber-bdr); }
.tag-norub  { background: var(--teal-bg);   color: var(--teal-dk);   border: 1px solid var(--teal-bdr); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── CONSTANTS ──
PAIRS = ["EUR/RUB","EUR/USD","RUB/EUR","RUB/USD","USD/EUR","USD/RUB"]

# Teal-blue-purple palette matching the reference image
PAIR_COLORS = {
    "EUR/RUB": "#13C9C2",  # teal
    "EUR/USD": "#4A9EF8",  # blue
    "RUB/EUR": "#9B74F5",  # purple
    "RUB/USD": "#64C8FF",  # light blue
    "USD/EUR": "#7B5EA7",  # violet
    "USD/RUB": "#0DA8A2",  # dark teal
}

TIERS = ["<$500","$500-1K","$1K-3K","$3K-10K","$10K-50K",">$50K"]

MONTHS_EN = {
    "2025-10":"Oct 25","2025-11":"Nov 25","2025-12":"Dec 25",
    "2026-01":"Jan 26","2026-02":"Feb 26","2026-03":"Mar 26","2026-04":"Apr 26",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
    font=dict(family="'Inter', sans-serif", color="#5A6A7E", size=11),
    margin=dict(l=8, r=8, t=44, b=8),
    xaxis=dict(gridcolor="#F0F2F7", gridwidth=1, zerolinecolor="#E4E8EF",
               linecolor="#E4E8EF", linewidth=1, tickfont=dict(size=10, color="#8B99AB")),
    yaxis=dict(gridcolor="#F0F2F7", gridwidth=1, zerolinecolor="#E4E8EF",
               linecolor="#E4E8EF", linewidth=1, tickfont=dict(size=10, color="#8B99AB")),
    legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#E4E8EF", borderwidth=1,
                font=dict(size=11, color="#2D3A4A"), orientation="h",
                yanchor="bottom", y=1.02, xanchor="left", x=0),
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E4E8EF",
                    font=dict(color="#1A2333", size=12, family="'Inter', sans-serif")),
    title_font=dict(size=13, color="#1A2333", family="'Inter', sans-serif"),
)

REQUIRED_COLS = {"from_currency","to_currency","from_amount","to_amount","spread","fx_revenue_usd","source"}

# ── DATA PROCESSING ──
def get_usd_amount(row):
    fc,tc = row.get("from_currency",""), row.get("to_currency","")
    fa,ta = float(row.get("from_amount",0)), float(row.get("to_amount",0))
    ru    = float(row.get("rate_usd_fixed",1) or 1)
    if fc=="USD": return fa
    if tc=="USD": return ta
    if fc=="RUB": return ta*ru
    if tc=="RUB": return fa*ru
    return fa*ru

def assign_tier(amt):
    if amt<500:   return "<$500"
    if amt<1000:  return "$500-1K"
    if amt<3000:  return "$1K-3K"
    if amt<10000: return "$3K-10K"
    if amt<50000: return "$10K-50K"
    return ">$50K"

@st.cache_data(show_spinner=False)
def process_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    if "updated_at" in df.columns:
        df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
        df["month"]   = df["updated_at"].dt.strftime("%Y-%m")
        df["hour"]    = df["updated_at"].dt.hour
        df["weekday"] = df["updated_at"].dt.day_name()
    else:
        df["month"]="unknown"; df["hour"]=0; df["weekday"]="unknown"
    df["pair"]           = df["from_currency"].astype(str)+"/"+df["to_currency"].astype(str)
    df["fx_revenue_usd"] = pd.to_numeric(df["fx_revenue_usd"],errors="coerce").fillna(0)
    df["spread"]         = pd.to_numeric(df["spread"],errors="coerce").fillna(0)
    df["amount_usd"]     = df.apply(get_usd_amount,axis=1)
    df["tier"]           = df["amount_usd"].apply(assign_tier)
    df["source"]         = df["source"].astype(str).str.strip().str.lower()
    return df

def fmt_usd(v):
    if abs(v)>=1e6: return f"${v/1e6:.2f}M"
    if abs(v)>=1e3: return f"${v/1e3:.1f}K"
    return f"${v:,.0f}"

def fmt_pct(v,t): return f"{v/t*100:.1f}%" if t>0 else "0%"

def sim_revenue(sub: pd.DataFrame, overrides: dict, elast: float) -> float:
    total=0.0
    for _,r in sub.iterrows():
        old_sp=r["spread"]; new_sp=overrides.get(r["pair"],old_sp)
        sf=new_sp/old_sp if old_sp>0 else 1.0
        vf=1+elast*max(0,old_sp-new_sp)
        total+=r["fx_revenue_usd"]*sf*vf
    return total

def agg_sim(df: pd.DataFrame, overrides: dict, elast: float, by: list) -> pd.DataFrame:
    rows=[]
    for keys,grp in df.groupby(by,observed=True):
        base=grp["fx_revenue_usd"].sum(); sim=sim_revenue(grp,overrides,elast); n=len(grp)
        row=dict(zip(by, keys if isinstance(keys,tuple) else [keys]))
        row.update({"n":n,"base_rev":base,"sim_rev":sim,"delta":sim-base,"avg_spread":grp["spread"].mean()})
        rows.append(row)
    return pd.DataFrame(rows)

def color_delta(val):
    if isinstance(val,(int,float)):
        if val>0.5:   return "color:#0DA8A2;font-weight:600"
        if val<-0.5:  return "color:#EF4A6B;font-weight:600"
        return "color:#8B99AB"
    return ""

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 22px">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px">
        <div style="width:32px;height:32px;background:#13C9C2;border-radius:8px;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <rect x="1" y="8" width="3" height="7" fill="white" opacity=".7"/>
            <rect x="6" y="4" width="3" height="11" fill="white"/>
            <rect x="11" y="1" width="3" height="14" fill="white" opacity=".55"/>
          </svg>
        </div>
        <div>
          <div style="font-size:14px;font-weight:600;color:#D8ECF8;letter-spacing:-.01em">FX Revenue</div>
          <div style="font-size:9px;color:#485E74;letter-spacing:.12em;text-transform:uppercase">Analytics · Stape</div>
        </div>
      </div>
      <div style="height:1px;background:rgba(255,255,255,0.08)"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Data")
    uploaded = st.file_uploader("CSV or Excel", type=["csv","xlsx","xls"], label_visibility="collapsed")

    if uploaded:
        try:
            df_raw = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
            missing = REQUIRED_COLS - set([c.strip().lower() for c in df_raw.columns])
            if missing: st.error(f"Missing columns: {', '.join(missing)}"); df_raw=None
            else: st.success(f"✓ {uploaded.name}  ·  {len(df_raw):,} rows")
        except Exception as e:
            st.error(f"Error: {e}"); df_raw=None
    else:
        df_raw=None
        st.info("Upload a CSV or Excel file to begin")
        with st.expander("Expected columns"):
            st.markdown("`updated_at` · `source` · `from_currency` · `to_currency`  \n"
                        "`from_amount` · `to_amount` · `spread` · `fx_revenue_usd`  \n"
                        "`original_rate_fixed` · `rate_usd_fixed`")

    st.markdown("### 🔍 Filters")

    if df_raw is not None:
        df            = process_dataframe(df_raw)
        avail_pairs   = sorted(df["pair"].unique().tolist())
        avail_sources = sorted(df["source"].unique().tolist())
        avail_months  = sorted(df["month"].unique().tolist())
        avail_tiers   = [t for t in TIERS if t in df["tier"].unique()]
    else:
        avail_pairs=PAIRS; avail_sources=["company","user"]
        avail_months=list(MONTHS_EN.keys()); avail_tiers=TIERS; df=pd.DataFrame()

    sel_pairs   = st.multiselect("Currency pair",    avail_pairs,   default=avail_pairs,   key="f_pair")
    sel_sources = st.multiselect("Source",           avail_sources, default=avail_sources, key="f_src")
    sel_tiers   = st.multiselect("Size tier (USD)",  avail_tiers,   default=avail_tiers,   key="f_tier")
    sel_months  = st.multiselect("Month",            avail_months,  default=avail_months,  key="f_month",
                                 format_func=lambda m: MONTHS_EN.get(m,m))

    st.markdown("### ⚙️ Simulation")
    elast = st.slider("Volume elasticity (× / p.p.)", 0.0, 2.0, 0.0, 0.05,
                      help="0 = volume unchanged  |  0.4 = +40% deals per 1 p.p. spread reduction")

    st.markdown("---")
    if st.button("↺ Reset filters", use_container_width=True): st.rerun()

# ── HEADER ──
col_h1, col_h2 = st.columns([3,1])
with col_h1:
    src_str = "no data loaded" if df.empty else f"{len(df):,} transactions · {df['month'].nunique()} months"
    st.markdown(f"""
    <div style="padding:4px 0 16px">
      <h1 style="font-size:24px;font-weight:600;letter-spacing:-.03em;margin:0;
                 color:#1A2333;font-family:'Inter',sans-serif">
        FX Revenue Dashboard
      </h1>
      <div style="font-size:13px;color:#8B99AB;margin-top:5px;font-family:'Inter',sans-serif">
        {src_str}
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    tag="demo" if df.empty else "live"
    label="Demo mode" if df.empty else "Live data"
    st.markdown(f'<div style="text-align:right;padding-top:16px">'
                f'<span class="fin-tag tag-{tag}">● {label}</span></div>',
                unsafe_allow_html=True)

if df.empty:
    st.markdown("""
    <div class="dash-card-teal" style="text-align:center;padding:72px 40px">
      <div style="font-size:40px;margin-bottom:18px;opacity:.18">◎</div>
      <div style="font-size:18px;font-weight:600;color:#1A2333;margin-bottom:8px">
        Upload data to get started
      </div>
      <div style="font-size:13px;color:#5A6A7E;max-width:480px;margin:0 auto;line-height:1.7">
        Import a CSV or Excel file using the panel on the left.<br>
        The dashboard will automatically compute metrics, spread distribution,
        revenue dynamics and break-even analysis.
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("#### Expected file structure")
    st.dataframe(pd.DataFrame({
        "updated_at":["2026-01-15 10:23:00","2026-01-15 11:05:00"],"source":["company","user"],
        "from_currency":["USD","EUR"],"to_currency":["RUB","USD"],
        "from_amount":[5000.00,1200.00],"to_amount":[455000.00,1320.00],
        "spread":[3.5,2.0],"original_rate_fixed":[91.0,1.10],
        "rate_usd_fixed":[1.0,1.0],"fx_revenue_usd":[175.00,24.00],
    }), use_container_width=True, hide_index=True)
    st.stop()

filt = df[
    df["pair"].isin(sel_pairs   if sel_pairs   else avail_pairs)   &
    df["source"].isin(sel_sources if sel_sources else avail_sources) &
    df["tier"].isin(sel_tiers   if sel_tiers   else avail_tiers)   &
    df["month"].isin(sel_months  if sel_months  else avail_months)
].copy()

if "ov" not in st.session_state: st.session_state.ov={}

def get_mean_spread(pair_df, pair):
    sub=pair_df[pair_df["pair"]==pair]
    return float(sub["spread"].mean()) if len(sub)>0 else 3.5

tab_ov,tab_calc,tab_analysis,tab_export = st.tabs(
    ["📈  Overview","🧮  Calculator","🔬  Analysis","⬇️  Export"])

# ══ TAB 1 — OVERVIEW ══
with tab_ov:
    base_total=filt["fx_revenue_usd"].sum(); sim_total=sim_revenue(filt,st.session_state.ov,elast)
    delta_total=sim_total-base_total; n_total=len(filt); avg_rev=sim_total/n_total if n_total>0 else 0
    base_all=df["fx_revenue_usd"].sum()

    kc1,kc2,kc3,kc4=st.columns(4)
    kc1.metric("Revenue (simulation)", fmt_usd(sim_total),
               delta=f"{'+' if delta_total>=0 else ''}{fmt_usd(delta_total)} vs base" if abs(delta_total)>0.5 else None)
    kc2.metric("Transactions", f"{n_total:,}", delta=fmt_pct(n_total,len(df)))
    kc3.metric("Avg revenue / deal", fmt_usd(avg_rev))
    kc4.metric("Share of total", fmt_pct(base_total,base_all) if base_all>0 else "100%",
               delta=fmt_usd(base_all))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Monthly stacked bar
    months_in_filter=sorted(filt["month"].unique())
    pairs_in_filter=[p for p in PAIRS if p in filt["pair"].unique()]

    fig_monthly=go.Figure()
    for pair in pairs_in_filter:
        sub_p=filt[filt["pair"]==pair]
        y_vals=[sim_revenue(sub_p[sub_p["month"]==m],st.session_state.ov,elast)
                if (sub_p["month"]==m).any() else 0 for m in months_in_filter]
        fig_monthly.add_trace(go.Bar(name=pair, x=[MONTHS_EN.get(m,m) for m in months_in_filter],
            y=y_vals, marker_color=PAIR_COLORS.get(pair,"#13C9C2"),
            marker_line=dict(width=0),
            hovertemplate=f"<b>{pair}</b><br>%{{x}}: %{{y:$,.0f}}<extra></extra>"))
    fig_monthly.update_layout(**PLOTLY_LAYOUT, title="Revenue by month",
                               barmode="stack", height=280,
                               bargap=0.3)
    st.plotly_chart(fig_monthly, use_container_width=True)

    col_t,col_s=st.columns(2)
    with col_t:
        tiers_in_filt=[t for t in TIERS if t in filt["tier"].unique()]
        tier_revs=[sim_revenue(filt[filt["tier"]==t],st.session_state.ov,elast) for t in tiers_in_filt]
        fig_tier=go.Figure(go.Bar(x=tier_revs,y=tiers_in_filt,orientation="h",
            marker=dict(color=tier_revs,
                colorscale=[[0,"#E6FAF9"],[0.4,"#64C8D8"],[1.0,"#13C9C2"]],
                line=dict(width=0)),
            hovertemplate="%{y}: %{x:$,.0f}<extra></extra>"))
        fig_tier.update_layout(**PLOTLY_LAYOUT, title="Revenue by size tier", height=260)
        fig_tier.update_yaxes(categoryorder="array", categoryarray=tiers_in_filt[::-1])
        st.plotly_chart(fig_tier, use_container_width=True)

    with col_s:
        sources=filt["source"].unique().tolist()
        src_rev=[sim_revenue(filt[filt["source"]==s],st.session_state.ov,elast) for s in sources]
        src_n=[len(filt[filt["source"]==s]) for s in sources]
        src_colors=["#4A9EF8","#9B74F5"]
        fig_src=make_subplots(specs=[[{"secondary_y":True}]])
        fig_src.add_trace(go.Bar(name="Revenue",x=sources,y=src_rev,
            marker_color=src_colors, marker_line=dict(width=0),
            hovertemplate="%{x}: %{y:$,.0f}<extra></extra>"), secondary_y=False)
        fig_src.add_trace(go.Scatter(name="Deals",x=sources,y=src_n,mode="markers",
            marker=dict(size=12,color=["#13C9C2","#64C8FF"],symbol="circle",
                        line=dict(color="#FFFFFF",width=2)),
            hovertemplate="%{x}: %{y:,} deals<extra></extra>"), secondary_y=True)
        fig_src.update_layout(**PLOTLY_LAYOUT, title="Sources — revenue / deal count", height=260)
        fig_src.update_yaxes(title_text="Revenue $",secondary_y=False,gridcolor="#F0F2F7",
            title_font=dict(size=10,color="#8B99AB"),color="#5A6A7E")
        fig_src.update_yaxes(title_text="Deals",secondary_y=True,gridcolor=None,
            title_font=dict(size=10,color="#8B99AB"),color="#5A6A7E")
        st.plotly_chart(fig_src, use_container_width=True)

    st.markdown("#### Breakdown by pair")
    pair_rows=[]
    for pair in pairs_in_filter:
        sub=filt[filt["pair"]==pair]; b=sub["fx_revenue_usd"].sum()
        s=sim_revenue(sub,st.session_state.ov,elast); n=len(sub); mu=sub["spread"].mean()
        pair_rows.append({"Pair":pair,"Deals":n,"Base ($)":round(b,2),
            "Simulated ($)":round(s,2),"Δ ($)":round(s-b,2),
            "Δ (%)":round((s-b)/b*100,2) if b>0 else 0,
            "μ spread (%)":round(mu,3),"Custom":"✓" if sub["spread"].nunique()>1 else "—",
            "Type":"RUB" if "RUB" in pair else "no RUB",
            "Share (%)":round(b/base_total*100,1) if base_total>0 else 0})
    pair_df_show=pd.DataFrame(pair_rows).sort_values("Simulated ($)",ascending=False)
    st.dataframe(pair_df_show.style.map(color_delta,subset=["Δ ($)","Δ (%)"]),
                 use_container_width=True, hide_index=True)

# ══ TAB 2 — CALCULATOR ══
with tab_calc:
    st.markdown("""
    <div class="dash-card-teal" style="margin-bottom:1rem">
      <div style="font-size:12px;color:#5A6A7E;line-height:1.7">
        <b style="color:#1A2333;font-weight:600">How simulation works:</b>&ensp;
        <code style="background:#E6FAF9;color:#0DA8A2;padding:2px 8px;border-radius:5px;font-size:11px">
          rev_sim = rev_base × (sp_new / sp_real) × (1 + E × max(0, sp_old − sp_new))
        </code><br>
        <span style="color:#8B99AB;font-size:11px">
          Uses the real weighted average spread (μ) from data.
          Pairs with custom spreads marked <span style="color:#F5A524">●</span>
        </span>
      </div>
    </div>""", unsafe_allow_html=True)

    pairs_in_filt2=[p for p in PAIRS if p in filt["pair"].unique()]
    cols=st.columns(3)

    for idx,pair in enumerate(pairs_in_filt2):
        sub=filt[filt["pair"]==pair]; mean_sp=get_mean_spread(filt,pair)
        min_sp=float(sub["spread"].min()) if len(sub)>0 else mean_sp
        max_sp=float(sub["spread"].max()) if len(sub)>0 else mean_sp
        has_cust=sub["spread"].nunique()>1; cur_sp=st.session_state.ov.get(pair,mean_sp)
        with cols[idx%3]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
              <span style="font-size:13px;font-weight:600;color:{PAIR_COLORS.get(pair,'#13C9C2')}">{pair}</span>
              <span style="font-size:9px;color:#8B99AB">
                μ={mean_sp:.3f}%{"&nbsp;<span style='color:#F5A524'>● custom</span>" if has_cust else ""}
              </span>
            </div>
            <div style="font-size:10px;color:#8B99AB;margin-bottom:5px">
              min {min_sp:.2f}% · max {max_sp:.2f}% · n={len(sub):,}
            </div>""", unsafe_allow_html=True)

            new_sp=st.slider(f"Spread {pair}",0.5,5.5,round(cur_sp,2),0.05,
                key=f"sp_{pair}",label_visibility="collapsed")
            st.session_state.ov[pair]=new_sp

            base_p=sub["fx_revenue_usd"].sum(); sim_p=sim_revenue(sub,st.session_state.ov,elast)
            d_p=sim_p-base_p
            dc="#0DA8A2" if d_p>0.5 else "#EF4A6B" if d_p<-0.5 else "#8B99AB"
            sc="#F5A524" if new_sp<mean_sp else "#0DA8A2" if new_sp>mean_sp else "#8B99AB"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:11px;margin-top:3px">
              <span style="color:{sc};font-weight:600">{new_sp:.2f}%{"↓" if new_sp<mean_sp else "↑" if new_sp>mean_sp else ""}</span>
              <span style="color:#5A6A7E">{fmt_usd(sim_p)}</span>
              <span style="color:{dc};font-weight:600">{'+' if d_p>=0 else ''}{fmt_usd(d_p)}</span>
            </div><hr>""", unsafe_allow_html=True)

    base_filt=filt["fx_revenue_usd"].sum(); sim_filt=sim_revenue(filt,st.session_state.ov,elast)
    delta_filt=sim_filt-base_filt; pct_filt=delta_filt/base_filt*100 if base_filt>0 else 0
    dc_main="#0DA8A2" if delta_filt>0 else "#EF4A6B"

    st.markdown(f"""
    <div class="dash-card" style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;margin-top:.5rem">
      <div style="padding:16px 22px;border-right:1px solid #EEF0F5">
        <div class="dash-label">Base (actual)</div>
        <div style="font-size:26px;font-weight:600;color:#2D3A4A;letter-spacing:-.03em">{fmt_usd(base_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-right:1px solid #EEF0F5;border-top:3px solid #13C9C2">
        <div class="dash-label">Simulation</div>
        <div style="font-size:26px;font-weight:700;color:#13C9C2;letter-spacing:-.03em">{fmt_usd(sim_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-right:1px solid #EEF0F5;border-top:3px solid {dc_main}">
        <div class="dash-label">Δ absolute</div>
        <div style="font-size:26px;font-weight:700;color:{dc_main};letter-spacing:-.03em">{'+' if delta_filt>=0 else ''}{fmt_usd(delta_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-top:3px solid {dc_main}">
        <div class="dash-label">Δ percent</div>
        <div style="font-size:26px;font-weight:700;color:{dc_main};letter-spacing:-.03em">{'+' if pct_filt>=0 else ''}{pct_filt:.1f}%</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### Break-even analysis")
    be_rows=[]
    for pair in pairs_in_filt2:
        sub=filt[filt["pair"]==pair]
        if not len(sub): continue
        mu=get_mean_spread(filt,pair); ns=st.session_state.ov.get(pair,mu)
        base=sub["fx_revenue_usd"].sum(); sim=sim_revenue(sub,st.session_state.ov,elast); d=sim-base
        sp_diff=mu-ns
        if sp_diff>0.01:
            sf=ns/mu; req_e=(1/sf-1)/sp_diff
            need_vol=f"+{req_e*100:.0f}% volume"; req_e_str=f"{req_e:.2f}x/p.p."
            verdict="✅ realistic" if req_e<=0.3 else "⚠️ uncertain" if req_e<=0.7 else "❌ unrealistic"
        elif sp_diff<-0.01:
            need_vol,req_e_str,verdict="spread increase","—","↑ revenue gain"
        else:
            need_vol,req_e_str,verdict="—","—","no change"
        be_rows.append({"Pair":pair,"μ spread (%)":round(mu,3),"New (%)":round(ns,2),
            "Base ($)":round(base,2),"Simulation ($)":round(sim,2),
            "Δ ($)":round(d,2),"Δ (%)":round(d/base*100,1) if base>0 else 0,
            "Volume needed":need_vol,"Elasticity req.":req_e_str,"Assessment":verdict})
    be_df=pd.DataFrame(be_rows)
    st.dataframe(be_df.style.map(color_delta,subset=["Δ ($)","Δ (%)"]),
                 use_container_width=True, hide_index=True)

    fig_cmp=go.Figure()
    for pair in pairs_in_filt2:
        sub=filt[filt["pair"]==pair]; b=sub["fx_revenue_usd"].sum()
        s=sim_revenue(sub,st.session_state.ov,elast)
        fig_cmp.add_trace(go.Bar(name=f"{pair} base",x=[pair],y=[b],
            marker_color="#E4E8EF",marker_line=dict(width=0),
            hovertemplate=f"<b>{pair} base</b>: %{{y:$,.0f}}<extra></extra>"))
        fig_cmp.add_trace(go.Bar(name=f"{pair} sim",x=[pair],y=[s],
            marker_color=PAIR_COLORS.get(pair,"#13C9C2"),marker_line=dict(width=0),
            hovertemplate=f"<b>{pair} simulation</b>: %{{y:$,.0f}}<extra></extra>"))
    fig_cmp.update_layout(**PLOTLY_LAYOUT,barmode="group",
        title="Base vs Simulation by pair",height=280,showlegend=False,bargap=0.25,bargroupgap=0.05)
    st.plotly_chart(fig_cmp, use_container_width=True)

# ══ TAB 3 — ANALYSIS ══
with tab_analysis:
    st.markdown("#### Revenue heatmap — pair × month")
    pairs_hm=[p for p in PAIRS if p in filt["pair"].unique()]
    months_hm=sorted(filt["month"].unique())
    hm_data=np.zeros((len(pairs_hm),len(months_hm)))
    for i,pair in enumerate(pairs_hm):
        for j,month in enumerate(months_hm):
            sub=filt[(filt["pair"]==pair)&(filt["month"]==month)]
            hm_data[i,j]=sim_revenue(sub,st.session_state.ov,elast) if len(sub)>0 else 0

    fig_hm=go.Figure(go.Heatmap(
        z=hm_data, x=[MONTHS_EN.get(m,m) for m in months_hm], y=pairs_hm,
        colorscale=[[0,"#F4F6F9"],[0.2,"#C0EAE8"],[0.55,"#3DC4BF"],[1.0,"#0A7A75"]],
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:$,.0f}<extra></extra>",
        text=[[fmt_usd(v) if v>0 else "—" for v in row] for row in hm_data],
        texttemplate="%{text}",
        textfont=dict(size=10,color="#1A2333",family="'Inter',sans-serif"),
        colorbar=dict(tickfont=dict(size=10,color="#5A6A7E"),outlinewidth=0,thickness=12,
            title=dict(text="Revenue $",font=dict(size=10,color="#8B99AB")))))
    fig_hm.update_layout(**PLOTLY_LAYOUT, height=300)
    fig_hm.update_yaxes(gridcolor=None, tickfont=dict(size=11,color="#2D3A4A"))
    st.plotly_chart(fig_hm, use_container_width=True)

    col_a1,col_a2=st.columns(2)

    with col_a1:
        st.markdown("#### Spread distribution by pair")
        spread_rows=[]
        for pair in pairs_hm:
            sub=filt[filt["pair"]==pair]
            if not len(sub): continue
            for sp_val,grp in sub.groupby("spread"):
                spread_rows.append({"pair":pair,"spread":sp_val,"n":len(grp),
                    "rev":grp["fx_revenue_usd"].sum(),"pct_n":len(grp)/len(sub)*100})
        if spread_rows:
            sp_df=pd.DataFrame(spread_rows)
            fig_sd=px.bar(sp_df,x="pct_n",y="pair",color="spread",orientation="h",barmode="stack",
                color_continuous_scale=["#C0EAE8","#3DC4BF","#13C9C2","#0A7A75"],
                labels={"pct_n":"% of transactions","pair":""},
                hover_data={"n":True,"rev":":.0f"},height=280)
            fig_sd.update_layout(**PLOTLY_LAYOUT,
                coloraxis_colorbar=dict(title=dict(text="Spread %",font=dict(size=10,color="#8B99AB")),
                    tickfont=dict(size=10,color="#5A6A7E"),outlinewidth=0,thickness=12))
            st.plotly_chart(fig_sd, use_container_width=True)

            with st.expander("Spread distribution detail"):
                pivot=sp_df.pivot_table(index="pair",columns="spread",values="pct_n",
                    aggfunc="sum",fill_value=0)
                pivot.columns=[f"{c:.1f}%" for c in pivot.columns]
                def color_pct(val):
                    if not isinstance(val,(int,float)) or val==0: return "color:#C0CAD4"
                    t=min(val/100,1.0)
                    r=int(192-(192-10)*t); g=int(234-(234-168)*t); b=int(232-(232-168)*t)
                    return (f"color:rgb({r},{g},{b});font-weight:{'600' if val>50 else '400'}")
                st.dataframe(pivot.round(1).style.map(color_pct),use_container_width=True)

    with col_a2:
        if "hour" in filt.columns:
            st.markdown("#### Avg revenue by hour (UTC)")
            hourly=filt.groupby("hour").agg(avg_rev=("fx_revenue_usd","mean"),
                n=("fx_revenue_usd","count")).reset_index()
            fig_hr=make_subplots(specs=[[{"secondary_y":True}]])
            fig_hr.add_trace(go.Scatter(x=hourly["hour"],y=hourly["avg_rev"],name="Avg revenue",
                mode="lines+markers",fill="tozeroy",
                line=dict(color="#13C9C2",width=2.5),
                fillcolor="rgba(19,201,194,0.08)",
                marker=dict(size=4,color="#13C9C2"),
                hovertemplate="Hour %{x}:00 · %{y:$,.0f}<extra></extra>"),secondary_y=False)
            fig_hr.add_trace(go.Bar(x=hourly["hour"],y=hourly["n"],name="Deal count",
                marker_color="rgba(74,158,248,0.15)",
                marker_line=dict(color="rgba(74,158,248,0.3)",width=1),
                hovertemplate="Hour %{x}:00 · %{y} deals<extra></extra>"),secondary_y=True)
            fig_hr.update_layout(**PLOTLY_LAYOUT,height=280)
            fig_hr.update_layout(legend=dict(x=0,y=1))
            fig_hr.update_xaxes(tickmode="linear",tick0=0,dtick=3,gridcolor="#F0F2F7")
            fig_hr.update_yaxes(title_text="Avg revenue $",secondary_y=False,
                title_font=dict(size=10,color="#8B99AB"),color="#5A6A7E")
            fig_hr.update_yaxes(title_text="Deal count",secondary_y=True,
                title_font=dict(size=10,color="#8B99AB"),color="#5A6A7E")
            st.plotly_chart(fig_hr, use_container_width=True)

    if "weekday" in filt.columns and filt["weekday"].nunique()>1:
        st.markdown("#### Avg revenue by day of week")
        day_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        day_en={"Monday":"Mon","Tuesday":"Tue","Wednesday":"Wed",
                "Thursday":"Thu","Friday":"Fri","Saturday":"Sat","Sunday":"Sun"}
        weekday_agg=(filt.groupby("weekday").agg(avg_rev=("fx_revenue_usd","mean"),
            n=("fx_revenue_usd","count"),total=("fx_revenue_usd","sum"))
            .reindex([d for d in day_order if d in filt["weekday"].unique()]).reset_index())
        weekday_agg["day_en"]=weekday_agg["weekday"].map(day_en)
        fig_wd=go.Figure(go.Bar(x=weekday_agg["day_en"],y=weekday_agg["avg_rev"],
            marker=dict(color=weekday_agg["avg_rev"],
                colorscale=[[0,"#E6FAF9"],[0.5,"#64C8D8"],[1.0,"#13C9C2"]],
                line=dict(width=0)),
            hovertemplate="%{x}: %{y:$,.0f} avg<extra></extra>"))
        fig_wd.update_layout(**PLOTLY_LAYOUT,height=220,title="Average revenue by day of week",
                              bargap=0.35)
        st.plotly_chart(fig_wd, use_container_width=True)

# ══ TAB 4 — EXPORT ══
with tab_export:
    st.markdown("### Export results")
    exp_c1,exp_c2=st.columns(2)

    with exp_c1:
        st.markdown("""
        <div class="dash-card-teal">
          <div class="dash-label">CSV · Filtered dataset</div>
          <div style="font-size:13px;font-weight:500;color:#1A2333;margin-bottom:4px">Aggregated data</div>
          <div style="font-size:12px;color:#5A6A7E">Current filter with simulated revenue and delta</div>
        </div>""", unsafe_allow_html=True)
        agg_exp=agg_sim(filt,st.session_state.ov,elast,by=["pair","tier","source","month"])
        st.download_button("⬇ Download CSV",data=agg_exp.to_csv(index=False).encode("utf-8"),
            file_name="fx_revenue_filtered.csv",mime="text/csv",use_container_width=True)

    with exp_c2:
        st.markdown("""
        <div class="dash-card-teal">
          <div class="dash-label">Excel · Full report</div>
          <div style="font-size:13px;font-weight:500;color:#1A2333;margin-bottom:4px">4 sheets</div>
          <div style="font-size:12px;color:#5A6A7E">Summary · By pair · By tier · By month</div>
        </div>""", unsafe_allow_html=True)
        xl_buf=io.BytesIO()
        with pd.ExcelWriter(xl_buf,engine="openpyxl") as writer:
            pd.DataFrame({"Metric":["Transactions (filter)","Base revenue","Simulated revenue",
                "Delta $","Delta %","Elasticity","Created at"],
                "Value":[len(filt),round(base_total,2),round(sim_total,2),
                round(delta_filt,2),round(pct_filt,2),elast,
                datetime.now().strftime("%Y-%m-%d %H:%M")]})\
                .to_excel(writer,sheet_name="Summary",index=False)
            agg_sim(filt,st.session_state.ov,elast,by=["pair"])\
                .to_excel(writer,sheet_name="By pair",index=False)
            agg_sim(filt,st.session_state.ov,elast,by=["tier"])\
                .to_excel(writer,sheet_name="By tier",index=False)
            agg_sim(filt,st.session_state.ov,elast,by=["month","pair"])\
                .to_excel(writer,sheet_name="By month",index=False)
        xl_buf.seek(0)
        st.download_button("⬇ Download Excel",data=xl_buf.read(),
            file_name="fx_revenue_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True)

    st.markdown("#### Current spread settings")
    ov_pairs=[p for p in PAIRS if p in filt["pair"].unique()]
    sp_config=[{"pair":p,"mean_spread":round(get_mean_spread(filt,p),3),
        "simulated_spread":round(st.session_state.ov.get(p,get_mean_spread(filt,p)),2),
        "elasticity":elast} for p in ov_pairs]
    st.dataframe(pd.DataFrame(sp_config),use_container_width=True,hide_index=True)
    st.download_button("⬇ Download spread config (CSV)",
        data=pd.DataFrame(sp_config).to_csv(index=False).encode("utf-8"),
        file_name="spread_config.csv",mime="text/csv")

    st.markdown("#### Raw filtered data")
    st.dataframe(filt.head(500),use_container_width=True,hide_index=True)
    st.caption(f"Showing 500 of {len(filt):,} rows")
    st.download_button("⬇ Download all filtered data (CSV)",
        data=filt.to_csv(index=False).encode("utf-8"),
        file_name="fx_data_filtered.csv",mime="text/csv")
