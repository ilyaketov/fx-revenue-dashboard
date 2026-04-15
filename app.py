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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
:root {
  --bg:#F4F6F9; --bg2:#FFFFFF; --bg3:#EBEEf3; --bg4:#DDE2EB;
  --ink:#0A1628; --ink2:#1E3050; --ink3:#3A4E66; --ink4:#6A7D95; --ink5:#A8B8C8;
  --blue:#0F4DA3; --blue-mid:#1A65CC; --blue-lt:#3B82E8; --blue-bg:#E8F0FB; --blue-bdr:#AECAF0;
  --sb-bg:#2A3B52; --sb-bg2:#344B64; --sb-bg3:#3E5878; --sb-bdr:rgba(255,255,255,0.12);
  --sb-tx:#C8D8EA; --sb-tx2:#8FA8C0; --sb-tx3:#607A96;
  --bdr:#D4D9E3; --bdr2:#BCC4D0;
  --green:#0C6641; --green-mid:#0E8454; --green-bg:#E5F4ED; --green-bdr:#9ACFB8;
  --red:#9B1A1F; --red-bg:#FAE8E8; --red-bdr:#E0AAAC;
  --amber:#7A4800; --amber-bg:#FDF2E0; --amber-bdr:#E5C070;
}
html,body,[class*="css"]{font-family:'IBM Plex Sans',-apple-system,sans-serif!important;background:var(--bg)!important;color:var(--ink)!important;-webkit-font-smoothing:antialiased!important;}
.main .block-container{padding:0 2.5rem 3rem!important;max-width:1440px!important;background:var(--bg)!important;}
.stApp{background:var(--bg)!important;}
h1,h2,h3,h4,h5,h6{color:var(--ink)!important;}
.main .block-container::before{content:'';display:block;height:3px;background:linear-gradient(90deg,var(--blue) 0%,var(--blue-lt) 55%,var(--bg4) 100%);margin:0 -2.5rem 1.5rem;}
[data-testid="stSidebar"]{background:var(--sb-bg)!important;border-right:1px solid var(--sb-bdr)!important;}
[data-testid="stSidebar"] *{color:var(--sb-tx)!important;}
[data-testid="stSidebar"] .stMarkdown h3{font-size:9px!important;font-weight:700!important;letter-spacing:.16em!important;text-transform:uppercase!important;color:var(--sb-tx3)!important;margin:1.3rem 0 .5rem!important;padding-bottom:5px!important;border-bottom:1px solid var(--sb-bdr)!important;}
[data-testid="stSidebar"] [data-testid="stMultiSelect"]>div,[data-testid="stSidebar"] [data-testid="stSelectbox"]>div>div{background:var(--sb-bg2)!important;border:1px solid var(--sb-bdr)!important;border-radius:3px!important;}
[data-testid="stSidebar"] [data-baseweb="tag"]{background:rgba(15,77,163,0.5)!important;border-color:rgba(59,130,232,0.6)!important;color:#C0D8F5!important;border-radius:2px!important;}
[data-testid="stSidebar"] [data-testid="stFileUploader"]{border:1px dashed var(--sb-bdr)!important;background:var(--sb-bg2)!important;border-radius:4px!important;}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover{border-color:rgba(59,130,232,0.55)!important;background:rgba(59,130,232,0.08)!important;}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] span{color:var(--sb-tx)!important;}
[data-testid="stSidebar"] hr{border-color:var(--sb-bdr)!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--bg2)!important;border-bottom:1px solid var(--bdr)!important;padding:0!important;border-radius:0!important;gap:0!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;border:none!important;border-bottom:2px solid transparent!important;margin-bottom:-1px!important;border-radius:0!important;color:var(--ink4)!important;font-size:11px!important;font-weight:600!important;letter-spacing:.08em!important;text-transform:uppercase!important;padding:14px 24px!important;}
.stTabs [data-baseweb="tab"]:hover{color:var(--ink2)!important;}
.stTabs [aria-selected="true"]{background:transparent!important;border-bottom:2px solid var(--blue)!important;color:var(--blue)!important;}
.stTabs [data-baseweb="tab-panel"]{background:transparent!important;padding:1.5rem 0!important;}
.stButton>button{background:var(--ink)!important;color:#EEF3F8!important;border:none!important;border-radius:3px!important;font-weight:500!important;font-size:12px!important;letter-spacing:.03em!important;padding:7px 18px!important;}
.stButton>button:hover{background:var(--ink2)!important;}
[data-testid="stDownloadButton"]>button{background:var(--bg2)!important;color:var(--blue-mid)!important;border:1px solid var(--blue-bdr)!important;border-radius:3px!important;font-size:12px!important;font-weight:500!important;}
[data-testid="stDownloadButton"]>button:hover{background:var(--blue-bg)!important;}
[data-testid="stMetric"]{background:var(--bg2)!important;border:1px solid var(--bdr)!important;border-top:2px solid var(--blue)!important;border-radius:2px!important;padding:18px 20px 14px!important;}
[data-testid="stMetric"]>div:first-child{font-size:9px!important;font-weight:700!important;letter-spacing:.15em!important;text-transform:uppercase!important;color:var(--ink4)!important;}
[data-testid="stMetric"] [data-testid="stMetricValue"]{font-size:28px!important;font-weight:400!important;color:var(--ink)!important;letter-spacing:-.03em!important;font-family:'IBM Plex Mono',monospace!important;}
[data-testid="stMetricDelta"]{font-size:11px!important;}
[data-testid="stDataFrame"]{background:var(--bg2)!important;border:1px solid var(--bdr)!important;border-radius:2px!important;overflow:hidden!important;}
hr{border:none!important;border-top:1px solid var(--bdr)!important;margin:.75rem 0!important;}
details{background:var(--bg2)!important;border:1px solid var(--bdr)!important;border-radius:3px!important;padding:2px 12px!important;}
summary{color:var(--ink3)!important;font-size:12px!important;font-weight:500!important;}
[data-testid="stInfo"]{background:var(--blue-bg)!important;border:1px solid var(--blue-bdr)!important;border-left:3px solid var(--blue)!important;border-radius:2px!important;color:var(--ink2)!important;}
[data-testid="stSuccess"]{background:var(--green-bg)!important;border:1px solid var(--green-bdr)!important;border-left:3px solid var(--green)!important;border-radius:2px!important;color:var(--green)!important;}
[data-testid="stWarning"]{background:var(--amber-bg)!important;border:1px solid var(--amber-bdr)!important;border-left:3px solid var(--amber)!important;border-radius:2px!important;color:var(--amber)!important;}
[data-testid="stError"]{background:var(--red-bg)!important;border:1px solid var(--red-bdr)!important;border-left:3px solid var(--red)!important;border-radius:2px!important;}
::-webkit-scrollbar{width:4px;height:4px;}::-webkit-scrollbar-track{background:var(--bg3);}::-webkit-scrollbar-thumb{background:var(--bg4);border-radius:2px;}
.fin-card{background:var(--bg2);border:1px solid var(--bdr);border-radius:2px;padding:18px 22px;margin-bottom:1rem;}
.fin-card-rule{background:var(--bg2);border:1px solid var(--bdr);border-top:2px solid var(--blue);border-radius:2px;padding:16px 22px;margin-bottom:1rem;}
.fin-label{font-size:9px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ink4);margin-bottom:6px;}
.fin-tag{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:2px;font-size:10px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;font-family:'IBM Plex Mono',monospace;}
.tag-rub{background:var(--amber-bg);color:var(--amber);border:1px solid var(--amber-bdr);}
.tag-norub{background:var(--green-bg);color:var(--green);border:1px solid var(--green-bdr);}
.tag-live{background:var(--green-bg);color:var(--green);border:1px solid var(--green-bdr);}
.tag-demo{background:var(--blue-bg);color:var(--blue);border:1px solid var(--blue-bdr);}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PAIRS = ["EUR/RUB","EUR/USD","RUB/EUR","RUB/USD","USD/EUR","USD/RUB"]
PAIR_COLORS = {
    "EUR/RUB":"#0F4DA3",
    "EUR/USD":"#0C7A52",
    "RUB/EUR":"#2870B0",
    "RUB/USD":"#0E9E6A",
    "USD/EUR":"#185C8A",
    "USD/RUB":"#094D34",
}
TIERS = ["<$500","$500-1K","$1K-3K","$3K-10K","$10K-50K",">$50K"]

MONTHS_EN = {
    "2025-10":"Oct 25","2025-11":"Nov 25","2025-12":"Dec 25",
    "2026-01":"Jan 26","2026-02":"Feb 26","2026-03":"Mar 26","2026-04":"Apr 26",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
    font=dict(family="'IBM Plex Sans',sans-serif", color="#1E3050", size=11),
    margin=dict(l=8, r=8, t=40, b=8),
    xaxis=dict(gridcolor="#EBEEf3", gridwidth=1, zerolinecolor="#D4D9E3",
               linecolor="#D4D9E3", linewidth=1, tickfont=dict(size=10, color="#4A5A72")),
    yaxis=dict(gridcolor="#EBEEf3", gridwidth=1, zerolinecolor="#D4D9E3",
               linecolor="#D4D9E3", linewidth=1, tickfont=dict(size=10, color="#4A5A72")),
    legend=dict(bgcolor="rgba(255,255,255,0.97)", bordercolor="#D4D9E3", borderwidth=1,
                font=dict(size=11, color="#1E3050"), orientation="h",
                yanchor="bottom", y=1.02, xanchor="left", x=0),
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#D4D9E3",
                    font=dict(color="#0A1628", size=12, family="'IBM Plex Sans',sans-serif")),
    title_font=dict(size=13, color="#0A1628", family="'IBM Plex Sans',sans-serif"),
)

REQUIRED_COLS = {"from_currency","to_currency","from_amount","to_amount","spread","fx_revenue_usd","source"}

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
        c="#0C6641" if val>0.5 else "#9B1A1F" if val<-0.5 else "#6A7D95"
        fw="600" if abs(val)>0.5 else "400"
        return f"color:{c};font-weight:{fw};font-family:'IBM Plex Mono',monospace"
    return ""

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 20px">
      <div style="display:flex;align-items:center;gap:11px;margin-bottom:16px">
        <div style="width:30px;height:30px;background:#0F4DA3;border-radius:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
            <rect x="1" y="8" width="3" height="7" fill="white" opacity=".65"/>
            <rect x="6" y="4" width="3" height="11" fill="white"/>
            <rect x="11" y="1" width="3" height="14" fill="white" opacity=".5"/>
          </svg>
        </div>
        <div>
          <div style="font-size:13px;font-weight:600;color:#D8E8F4;letter-spacing:-.01em;font-family:'IBM Plex Sans',sans-serif">FX Revenue</div>
          <div style="font-size:9px;color:#607A96;letter-spacing:.14em;text-transform:uppercase;font-family:monospace">Analytics · Stape</div>
        </div>
      </div>
      <div style="height:1px;background:rgba(255,255,255,0.12)"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Data")
    uploaded = st.file_uploader("CSV or Excel (.xlsx)", type=["csv","xlsx","xls"], label_visibility="collapsed")

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
            st.markdown("`updated_at` · `source` · `from_currency` · `to_currency`  \n`from_amount` · `to_amount` · `spread` · `fx_revenue_usd`  \n`original_rate_fixed` · `rate_usd_fixed`")

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
    elast = st.slider("Volume elasticity (× per p.p.)", min_value=0.0, max_value=2.0,
                      value=0.0, step=0.05,
                      help="0 = volume unchanged  |  0.4 = +40% deals per 1 p.p. spread reduction")

    st.markdown("---")
    if st.button("↺ Reset filters", use_container_width=True): st.rerun()

# ── HEADER ──
col_h1, col_h2 = st.columns([3,1])
with col_h1:
    src_str = "no data loaded" if df.empty else f"{len(df):,} transactions · {df['month'].nunique()} months"
    st.markdown(f"""
    <div style="padding:20px 0 4px">
      <div style="font-size:9px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
                  color:#6A7D95;margin-bottom:7px;font-family:'IBM Plex Mono',monospace">FX · REVENUE ANALYTICS</div>
      <h1 style="font-size:26px;font-weight:300;letter-spacing:-.03em;margin:0;color:#0A1628;
                 font-family:'IBM Plex Sans',sans-serif;line-height:1.1">
        FX Revenue <span style="font-weight:600">Dashboard</span></h1>
      <div style="font-size:12px;color:#6A7D95;margin-top:6px;font-family:'IBM Plex Mono',monospace;letter-spacing:.02em">{src_str}</div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    tag="demo" if df.empty else "live"
    label="Demo mode" if df.empty else "Live data"
    st.markdown(f'<div style="text-align:right;padding-top:28px"><span class="fin-tag tag-{tag}">● {label}</span></div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

if df.empty:
    st.markdown("""
    <div class="fin-card-rule" style="text-align:center;padding:64px 40px">
      <div style="font-size:32px;margin-bottom:18px;opacity:.2">▦</div>
      <div style="font-size:18px;font-weight:500;color:#0A1628;margin-bottom:8px;font-family:'IBM Plex Sans',sans-serif">Upload data to get started</div>
      <div style="font-size:13px;color:#3A4E66;max-width:480px;margin:0 auto;line-height:1.65">
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

tab_ov,tab_calc,tab_analysis,tab_export = st.tabs(["📈  Overview","🧮  Calculator","🔬  Analysis","⬇️  Export"])

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
    kc4.metric("Share of total revenue", fmt_pct(base_total,base_all) if base_all>0 else "100%", delta=fmt_usd(base_all))

    st.markdown("---")

    months_in_filter=sorted(filt["month"].unique())
    pairs_in_filter=[p for p in PAIRS if p in filt["pair"].unique()]

    fig_monthly=go.Figure()
    for pair in pairs_in_filter:
        sub_p=filt[filt["pair"]==pair]
        y_vals=[sim_revenue(sub_p[sub_p["month"]==m],st.session_state.ov,elast)
                if (sub_p["month"]==m).any() else 0 for m in months_in_filter]
        fig_monthly.add_trace(go.Bar(name=pair, x=[MONTHS_EN.get(m,m) for m in months_in_filter],
            y=y_vals, marker_color=PAIR_COLORS.get(pair,"#888"),
            hovertemplate=f"<b>{pair}</b><br>%{{x}}: %{{y:$,.0f}}<extra></extra>"))
    fig_monthly.update_layout(**PLOTLY_LAYOUT, title="Revenue by month", barmode="stack", height=280)
    st.plotly_chart(fig_monthly, use_container_width=True)

    col_t,col_s=st.columns(2)
    with col_t:
        tiers_in_filt=[t for t in TIERS if t in filt["tier"].unique()]
        tier_revs=[sim_revenue(filt[filt["tier"]==t],st.session_state.ov,elast) for t in tiers_in_filt]
        fig_tier=go.Figure(go.Bar(x=tier_revs,y=tiers_in_filt,orientation="h",
            marker=dict(color=tier_revs,colorscale=[[0,"#E8F0FB"],[0.4,"#5A92D8"],[1.0,"#0F4DA3"]]),
            hovertemplate="%{y}: %{x:$,.0f}<extra></extra>"))
        fig_tier.update_layout(**PLOTLY_LAYOUT, title="Revenue by size tier", height=260)
        fig_tier.update_yaxes(categoryorder="array", categoryarray=tiers_in_filt[::-1])
        st.plotly_chart(fig_tier, use_container_width=True)

    with col_s:
        sources=filt["source"].unique().tolist()
        src_rev=[sim_revenue(filt[filt["source"]==s],st.session_state.ov,elast) for s in sources]
        src_n=[len(filt[filt["source"]==s]) for s in sources]
        src_colors=["#0F4DA3","#0C7A52"]
        fig_src=make_subplots(specs=[[{"secondary_y":True}]])
        fig_src.add_trace(go.Bar(name="Revenue",x=sources,y=src_rev,marker_color=src_colors,
            hovertemplate="%{x}: %{y:$,.0f}<extra></extra>"), secondary_y=False)
        fig_src.add_trace(go.Scatter(name="Deals",x=sources,y=src_n,mode="markers",
            marker=dict(size=10,color=["#2870B0","#0E9E6A"],symbol="diamond"),
            hovertemplate="%{x}: %{y:,} deals<extra></extra>"), secondary_y=True)
        fig_src.update_layout(**PLOTLY_LAYOUT, title="Sources — revenue / deal count", height=260)
        fig_src.update_yaxes(title_text="Revenue $",secondary_y=False,gridcolor="#EBEEf3",
            title_font=dict(size=10,color="#6A7D95"),color="#4A5A72")
        fig_src.update_yaxes(title_text="Deals",secondary_y=True,gridcolor=None,
            title_font=dict(size=10,color="#6A7D95"),color="#4A5A72")
        st.plotly_chart(fig_src, use_container_width=True)

    st.markdown("#### Breakdown by pair")
    pair_rows=[]
    for pair in pairs_in_filter:
        sub=filt[filt["pair"]==pair]; b=sub["fx_revenue_usd"].sum()
        s=sim_revenue(sub,st.session_state.ov,elast); n=len(sub); mu=sub["spread"].mean()
        pair_rows.append({"Pair":pair,"Deals":n,"Base ($)":round(b,2),"Simulated ($)":round(s,2),
            "Δ ($)":round(s-b,2),"Δ (%)":round((s-b)/b*100,2) if b>0 else 0,
            "μ spread (%)":round(mu,3),"Custom":"✓" if sub["spread"].nunique()>1 else "—",
            "Type":"RUB" if "RUB" in pair else "no RUB",
            "Share (%)":round(b/base_total*100,1) if base_total>0 else 0})
    pair_df_show=pd.DataFrame(pair_rows).sort_values("Simulated ($)",ascending=False)
    st.dataframe(pair_df_show.style.map(color_delta,subset=["Δ ($)","Δ (%)"]),
                 use_container_width=True, hide_index=True)

# ══ TAB 2 — CALCULATOR ══
with tab_calc:
    st.markdown("""
    <div class="fin-card-rule" style="margin-bottom:1rem">
      <div style="font-size:12px;color:#3A4E66;line-height:1.65">
        <b style="color:#0A1628;font-weight:600">How simulation works:</b>&ensp;
        <code style="background:#E8F0FB;color:#0F4DA3;padding:2px 7px;border-radius:2px;
                     font-family:'IBM Plex Mono',monospace;font-size:11px">
          rev_sim = rev_base × (sp_new / sp_real) × (1 + E × max(0, sp_old − sp_new))
        </code><br>
        <span style="color:#6A7D95;font-size:11px">Uses the real weighted average spread (μ) from data.
        Pairs with custom spreads are marked <span style="color:#7A4800">●</span></span>
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
              <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;
                           color:{PAIR_COLORS.get(pair,'#1E3050')}">{pair}</span>
              <span style="font-size:9px;color:#6A7D95;font-family:'IBM Plex Mono',monospace">
                μ={mean_sp:.3f}%{"&nbsp;&nbsp;<span style='color:#7A4800'>● custom</span>" if has_cust else ""}
              </span>
            </div>
            <div style="font-size:10px;color:#6A7D95;font-family:'IBM Plex Mono',monospace;margin-bottom:5px">
              min {min_sp:.2f}% · max {max_sp:.2f}% · n={len(sub):,}
            </div>""", unsafe_allow_html=True)

            new_sp=st.slider(f"Spread {pair}",min_value=0.5,max_value=5.5,
                value=round(cur_sp,2),step=0.05,key=f"sp_{pair}",label_visibility="collapsed")
            st.session_state.ov[pair]=new_sp

            base_p=sub["fx_revenue_usd"].sum(); sim_p=sim_revenue(sub,st.session_state.ov,elast)
            d_p=sim_p-base_p
            dc="#0C6641" if d_p>0.5 else "#9B1A1F" if d_p<-0.5 else "#6A7D95"
            sc="#7A4800" if new_sp<mean_sp else "#0C6641" if new_sp>mean_sp else "#6A7D95"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:11px;
                        font-family:'IBM Plex Mono',monospace;margin-top:3px">
              <span style="color:{sc};font-weight:600">{new_sp:.2f}%{"↓" if new_sp<mean_sp else "↑" if new_sp>mean_sp else ""}</span>
              <span style="color:#3A4E66">{fmt_usd(sim_p)}</span>
              <span style="color:{dc};font-weight:500">{'+' if d_p>=0 else ''}{fmt_usd(d_p)}</span>
            </div><hr style="margin:10px 0">""", unsafe_allow_html=True)

    base_filt=filt["fx_revenue_usd"].sum(); sim_filt=sim_revenue(filt,st.session_state.ov,elast)
    delta_filt=sim_filt-base_filt; pct_filt=delta_filt/base_filt*100 if base_filt>0 else 0
    dc_main="#0C6641" if delta_filt>0 else "#9B1A1F"

    st.markdown(f"""
    <div class="fin-card" style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;margin-top:.5rem">
      <div style="padding:16px 22px;border-right:1px solid #D4D9E3">
        <div class="fin-label">Base (actual)</div>
        <div style="font-size:24px;font-weight:400;font-family:'IBM Plex Mono',monospace;color:#1E3050;letter-spacing:-.02em">{fmt_usd(base_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-right:1px solid #D4D9E3;border-top:2px solid #0F4DA3">
        <div class="fin-label">Simulation</div>
        <div style="font-size:24px;font-weight:600;font-family:'IBM Plex Mono',monospace;color:#0F4DA3;letter-spacing:-.02em">{fmt_usd(sim_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-right:1px solid #D4D9E3;border-top:2px solid {dc_main}">
        <div class="fin-label">Δ absolute</div>
        <div style="font-size:24px;font-weight:600;font-family:'IBM Plex Mono',monospace;color:{dc_main};letter-spacing:-.02em">{'+' if delta_filt>=0 else ''}{fmt_usd(delta_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-top:2px solid {dc_main}">
        <div class="fin-label">Δ percent</div>
        <div style="font-size:24px;font-weight:600;font-family:'IBM Plex Mono',monospace;color:{dc_main};letter-spacing:-.02em">{'+' if pct_filt>=0 else ''}{pct_filt:.1f}%</div>
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
            marker_color="#D4D9E3",marker_line=dict(color="#BCC4D0",width=1),
            hovertemplate=f"<b>{pair} base</b>: %{{y:$,.0f}}<extra></extra>"))
        fig_cmp.add_trace(go.Bar(name=f"{pair} sim",x=[pair],y=[s],
            marker_color=PAIR_COLORS.get(pair,"#0F4DA3"),
            hovertemplate=f"<b>{pair} simulation</b>: %{{y:$,.0f}}<extra></extra>"))
    fig_cmp.update_layout(**PLOTLY_LAYOUT,barmode="group",
        title="Base vs Simulation by pair",height=280,showlegend=False)
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
        colorscale=[[0,"#F4F6F9"],[0.2,"#C6D9F2"],[0.55,"#4E82D0"],[1.0,"#0A2E70"]],
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:$,.0f}<extra></extra>",
        text=[[fmt_usd(v) if v>0 else "—" for v in row] for row in hm_data],
        texttemplate="%{text}",
        textfont=dict(size=10,color="#0A1628",family="'IBM Plex Mono',monospace"),
        colorbar=dict(tickfont=dict(size=10,color="#4A5A72"),outlinewidth=0,thickness=12,
            title=dict(text="Revenue $",font=dict(size=10,color="#6A7D95")))))
    fig_hm.update_layout(**PLOTLY_LAYOUT, height=300)
    fig_hm.update_yaxes(gridcolor=None,
        tickfont=dict(family="'IBM Plex Mono',monospace",size=11,color="#1E3050"))
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
                color_continuous_scale=["#C6D9F2","#4E82D0","#0F4DA3","#0A2E70"],
                labels={"pct_n":"% of transactions","pair":""},
                hover_data={"n":True,"rev":":.0f"},height=280)
            fig_sd.update_layout(**PLOTLY_LAYOUT,
                coloraxis_colorbar=dict(title=dict(text="Spread %",font=dict(size=10,color="#6A7D95")),
                    tickfont=dict(size=10,color="#4A5A72"),outlinewidth=0,thickness=12))
            st.plotly_chart(fig_sd, use_container_width=True)

            with st.expander("Spread distribution detail"):
                pivot=sp_df.pivot_table(index="pair",columns="spread",values="pct_n",
                    aggfunc="sum",fill_value=0)
                pivot.columns=[f"{c:.1f}%" for c in pivot.columns]
                def color_pct(val):
                    if not isinstance(val,(int,float)) or val==0: return "color:#A8B8C8"
                    t=min(val/100,1.0)
                    r=int(198-(198-10)*t); g=int(217-(217-46)*t); b=int(242-(242-112)*t)
                    return (f"color:rgb({r},{g},{b});font-weight:{'600' if val>50 else '400'};"
                            f"font-family:'IBM Plex Mono',monospace")
                st.dataframe(pivot.round(1).style.map(color_pct),use_container_width=True)

    with col_a2:
        if "hour" in filt.columns:
            st.markdown("#### Avg revenue by hour (UTC)")
            hourly=filt.groupby("hour").agg(avg_rev=("fx_revenue_usd","mean"),
                n=("fx_revenue_usd","count")).reset_index()
            fig_hr=make_subplots(specs=[[{"secondary_y":True}]])
            fig_hr.add_trace(go.Scatter(x=hourly["hour"],y=hourly["avg_rev"],name="Avg revenue",
                mode="lines+markers",fill="tozeroy",line=dict(color="#0F4DA3",width=2),
                fillcolor="rgba(15,77,163,0.07)",marker=dict(size=4,color="#0F4DA3"),
                hovertemplate="Hour %{x}:00 · %{y:$,.0f}<extra></extra>"),secondary_y=False)
            fig_hr.add_trace(go.Bar(x=hourly["hour"],y=hourly["n"],name="Deal count",
                marker_color="rgba(12,122,82,0.12)",
                marker_line=dict(color="rgba(12,122,82,0.25)",width=1),
                hovertemplate="Hour %{x}:00 · %{y} deals<extra></extra>"),secondary_y=True)
            fig_hr.update_layout(**PLOTLY_LAYOUT,height=280)
            fig_hr.update_layout(legend=dict(x=0,y=1))
            fig_hr.update_xaxes(tickmode="linear",tick0=0,dtick=3,gridcolor="#EBEEf3")
            fig_hr.update_yaxes(title_text="Avg revenue $",secondary_y=False,
                title_font=dict(size=10,color="#6A7D95"),color="#4A5A72")
            fig_hr.update_yaxes(title_text="Deal count",secondary_y=True,
                title_font=dict(size=10,color="#6A7D95"),color="#4A5A72")
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
                colorscale=[[0,"#E8F0FB"],[0.5,"#5A92D8"],[1.0,"#0F4DA3"]],
                line=dict(color="rgba(15,77,163,0.2)",width=1)),
            hovertemplate="%{x}: %{y:$,.0f} avg<extra></extra>"))
        fig_wd.update_layout(**PLOTLY_LAYOUT,height=220,title="Average revenue by day of week")
        st.plotly_chart(fig_wd, use_container_width=True)

# ══ TAB 4 — EXPORT ══
with tab_export:
    st.markdown("### Export results")
    exp_c1,exp_c2=st.columns(2)

    with exp_c1:
        st.markdown("""
        <div class="fin-card-rule">
          <div class="fin-label">CSV · Filtered dataset</div>
          <div style="font-size:13px;font-weight:500;color:#0A1628;margin-bottom:4px">Aggregated data</div>
          <div style="font-size:12px;color:#3A4E66">Current filter with simulated revenue and delta</div>
        </div>""", unsafe_allow_html=True)
        agg_exp=agg_sim(filt,st.session_state.ov,elast,by=["pair","tier","source","month"])
        st.download_button("⬇ Download CSV",data=agg_exp.to_csv(index=False).encode("utf-8"),
            file_name="fx_revenue_filtered.csv",mime="text/csv",use_container_width=True)

    with exp_c2:
        st.markdown("""
        <div class="fin-card-rule">
          <div class="fin-label">Excel · Full report</div>
          <div style="font-size:13px;font-weight:500;color:#0A1628;margin-bottom:4px">4 sheets</div>
          <div style="font-size:12px;color:#3A4E66">Summary · By pair · By tier · By month</div>
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
