import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FX Revenue Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM — INSTITUTIONAL FINANCIAL LIGHT
# ─────────────────────────────────────────────
STAPE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ─── Design tokens ─── */
:root {
  /* Backgrounds */
  --bg:        #F7F8FA;
  --bg2:       #FFFFFF;
  --bg3:       #EFF1F5;
  --bg4:       #E4E7EE;
  --bg5:       #D8DCE6;

  /* Primary — institutional slate-blue */
  --ink:       #0D1B2E;      /* headlines, primary text  */
  --ink2:      #2C3E55;      /* body text                */
  --ink3:      #5A6A80;      /* secondary labels         */
  --ink4:      #96A3B5;      /* muted / disabled         */
  --ink5:      #C4CAD5;      /* placeholder              */

  /* Accent — single authoritative blue */
  --blue:      #1251A3;
  --blue-mid:  #1A65CC;
  --blue-lt:   #2E7DE8;
  --blue-bg:   #EBF1FB;
  --blue-bdr:  #B8CFF0;

  /* Sidebar */
  --sb-bg:     #0E1B2E;
  --sb-bg2:    #162438;
  --sb-bdr:    rgba(255,255,255,0.07);
  --sb-tx:     #A8BDD4;
  --sb-tx2:    #6882A0;
  --sb-tx3:    #38526E;

  /* Borders */
  --bdr:       #DDE1EA;
  --bdr2:      #C8CDD8;

  /* Semantic */
  --green:     #0A6E45;
  --green-mid: #0D8A57;
  --green-bg:  #E8F5EF;
  --green-bdr: #A8D9C2;
  --red:       #A61C22;
  --red-mid:   #C0222A;
  --red-bg:    #FAEAEA;
  --red-bdr:   #E8AEB0;
  --amber:     #7A4A00;
  --amber-bg:  #FDF3E0;
  --amber-bdr: #E8C87A;
}

/* ─── Global reset ─── */
html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
  background: var(--bg) !important;
  color: var(--ink) !important;
  -webkit-font-smoothing: antialiased !important;
  font-feature-settings: "tnum" on !important;
}
.main .block-container {
  padding: 0 2.5rem 3rem !important;
  max-width: 1440px !important;
  background: var(--bg) !important;
}
.stApp { background: var(--bg) !important; }
h1,h2,h3,h4,h5,h6 { color: var(--ink) !important; letter-spacing: -.01em !important; }

/* ─── Top rule ─── */
.main .block-container::before {
  content: '';
  display: block;
  height: 3px;
  background: linear-gradient(90deg, var(--blue) 0%, var(--blue-lt) 60%, var(--bg4) 100%);
  margin: 0 -2.5rem 1.5rem;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
  background: var(--sb-bg) !important;
  border-right: 1px solid var(--sb-bdr) !important;
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
  border-radius: 3px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: rgba(18,81,163,0.45) !important;
  border-color: rgba(18,81,163,0.7) !important;
  color: #A5C4F3 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
  border: 1px dashed var(--sb-bdr) !important;
  background: var(--sb-bg2) !important;
  border-radius: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
  border-color: rgba(46,125,232,0.5) !important;
  background: rgba(46,125,232,0.06) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color: var(--sb-tx) !important; }
[data-testid="stSidebar"] hr {
  border-color: var(--sb-bdr) !important;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
  gap: 0 !important;
  background: var(--bg2) !important;
  border-bottom: 1px solid var(--bdr) !important;
  border-radius: 0 !important;
  padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -1px !important;
  border-radius: 0 !important;
  color: var(--ink4) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  letter-spacing: .03em !important;
  text-transform: uppercase !important;
  padding: 14px 22px !important;
  transition: color .12s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink2) !important; }
.stTabs [aria-selected="true"] {
  background: transparent !important;
  border-bottom: 2px solid var(--blue) !important;
  color: var(--blue) !important;
  font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: transparent !important;
  padding: 1.5rem 0 !important;
}

/* ─── Buttons ─── */
.stButton > button {
  background: var(--ink) !important;
  color: #F0F4F8 !important;
  border: none !important;
  border-radius: 3px !important;
  font-weight: 500 !important;
  font-size: 12px !important;
  letter-spacing: .03em !important;
  padding: 7px 18px !important;
  transition: background .12s !important;
}
.stButton > button:hover { background: var(--ink2) !important; }
[data-testid="stDownloadButton"] > button {
  background: var(--bg2) !important;
  color: var(--blue-mid) !important;
  border: 1px solid var(--blue-bdr) !important;
  border-radius: 3px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: var(--blue-bg) !important;
}

/* ─── Metrics ─── */
[data-testid="stMetric"] {
  background: var(--bg2) !important;
  border: 1px solid var(--bdr) !important;
  border-top: 2px solid var(--blue) !important;
  border-radius: 2px !important;
  padding: 18px 20px 15px !important;
}
[data-testid="stMetric"] > div:first-child {
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: .15em !important;
  text-transform: uppercase !important;
  color: var(--ink4) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
  font-size: 30px !important;
  font-weight: 400 !important;
  color: var(--ink) !important;
  letter-spacing: -.03em !important;
  font-family: 'IBM Plex Mono', monospace !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ─── DataFrames ─── */
[data-testid="stDataFrame"] {
  background: var(--bg2) !important;
  border: 1px solid var(--bdr) !important;
  border-radius: 2px !important;
  overflow: hidden !important;
}

/* ─── Divider ─── */
hr {
  border: none !important;
  border-top: 1px solid var(--bdr) !important;
  margin: .75rem 0 !important;
}

/* ─── Expanders ─── */
details {
  background: var(--bg2) !important;
  border: 1px solid var(--bdr) !important;
  border-radius: 3px !important;
  padding: 2px 12px !important;
}
summary {
  color: var(--ink3) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}

/* ─── Alerts ─── */
[data-testid="stInfo"] {
  background: var(--blue-bg) !important;
  border: 1px solid var(--blue-bdr) !important;
  border-left: 3px solid var(--blue) !important;
  border-radius: 2px !important; color: var(--ink2) !important;
}
[data-testid="stSuccess"] {
  background: var(--green-bg) !important;
  border: 1px solid var(--green-bdr) !important;
  border-left: 3px solid var(--green) !important;
  border-radius: 2px !important; color: var(--green) !important;
}
[data-testid="stWarning"] {
  background: var(--amber-bg) !important;
  border: 1px solid var(--amber-bdr) !important;
  border-left: 3px solid var(--amber) !important;
  border-radius: 2px !important; color: var(--amber) !important;
}
[data-testid="stError"] {
  background: var(--red-bg) !important;
  border: 1px solid var(--red-bdr) !important;
  border-left: 3px solid var(--red) !important;
  border-radius: 2px !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
  background: var(--blue) !important;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg3); }
::-webkit-scrollbar-thumb { background: var(--bg5); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--ink4); }

/* ─── Custom cards ─── */
.fin-card {
  background: var(--bg2);
  border: 1px solid var(--bdr);
  border-radius: 2px;
  padding: 18px 22px;
  margin-bottom: 1rem;
}
.fin-card-rule {
  background: var(--bg2);
  border: 1px solid var(--bdr);
  border-top: 2px solid var(--blue);
  border-radius: 2px;
  padding: 16px 22px;
  margin-bottom: 1rem;
}
.fin-card-muted {
  background: var(--bg3);
  border: 1px solid var(--bdr);
  border-radius: 2px;
  padding: 16px 22px;
  margin-bottom: 1rem;
}
.fin-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--ink4);
  margin-bottom: 6px;
}
.fin-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 2px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: .05em;
  text-transform: uppercase;
  font-family: 'IBM Plex Mono', monospace;
}
.tag-rub   { background: var(--amber-bg); color: var(--amber); border: 1px solid var(--amber-bdr); }
.tag-norub { background: var(--green-bg); color: var(--green); border: 1px solid var(--green-bdr); }
.tag-live  { background: var(--green-bg); color: var(--green); border: 1px solid var(--green-bdr); }
.tag-demo  { background: var(--blue-bg);  color: var(--blue);  border: 1px solid var(--blue-bdr); }
.tag-custom{ background: var(--amber-bg); color: var(--amber); border: 1px solid var(--amber-bdr); }
</style>
"""
st.markdown(STAPE_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
PAIRS = ["EUR/RUB", "EUR/USD", "RUB/EUR", "RUB/USD", "USD/EUR", "USD/RUB"]
PAIR_COLORS = {
    "EUR/RUB": "#1251A3",   # Primary blue
    "EUR/USD": "#0A6E45",   # Institutional green
    "RUB/EUR": "#5C3D99",   # Muted violet
    "RUB/USD": "#A04B00",   # Warm sienna
    "USD/EUR": "#2E6B8A",   # Steel blue
    "USD/RUB": "#0D1B2E",   # Near-black ink
}
TIERS = ["<$500", "$500–1K", "$1K–3K", "$3K–10K", "$10K–50K", ">$50K"]
TIER_ORDER = {t: i for i, t in enumerate(TIERS)}

MONTHS_RU = {
    "2025-10": "Окт 25", "2025-11": "Ноя 25", "2025-12": "Дек 25",
    "2026-01": "Янв 26", "2026-02": "Фев 26", "2026-03": "Мар 26", "2026-04": "Апр 26",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font=dict(family="'IBM Plex Sans', -apple-system, sans-serif", color="#5A6A80", size=11),
    margin=dict(l=8, r=8, t=36, b=8),
    xaxis=dict(
        gridcolor="#EFF1F5",
        gridwidth=1,
        zerolinecolor="#DDE1EA",
        linecolor="#DDE1EA",
        linewidth=1,
        tickfont=dict(size=10, color="#96A3B5"),
    ),
    yaxis=dict(
        gridcolor="#EFF1F5",
        gridwidth=1,
        zerolinecolor="#DDE1EA",
        linecolor="#DDE1EA",
        linewidth=1,
        tickfont=dict(size=10, color="#96A3B5"),
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.96)",
        bordercolor="#DDE1EA",
        borderwidth=1,
        font=dict(size=11, color="#2C3E55"),
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="left", x=0,
    ),
    hoverlabel=dict(
        bgcolor="#FFFFFF",
        bordercolor="#DDE1EA",
        font=dict(color="#0D1B2E", size=12, family="'IBM Plex Sans', sans-serif"),
    ),
    title_font=dict(size=13, color="#0D1B2E", family="'IBM Plex Sans', sans-serif"),
)

REQUIRED_COLS = {
    "from_currency", "to_currency", "from_amount", "to_amount",
    "spread", "fx_revenue_usd", "source",
}

# ─────────────────────────────────────────────
# DATA PROCESSING
# ─────────────────────────────────────────────
def get_usd_amount(row):
    fc, tc = row.get("from_currency", ""), row.get("to_currency", "")
    fa, ta = float(row.get("from_amount", 0)), float(row.get("to_amount", 0))
    ru = float(row.get("rate_usd_fixed", 1) or 1)
    if fc == "USD": return fa
    if tc == "USD": return ta
    if fc == "RUB": return ta * ru
    if tc == "RUB": return fa * ru
    return fa * ru

def assign_tier(amt):
    if amt < 500:   return "<$500"
    if amt < 1000:  return "$500–1K"
    if amt < 3000:  return "$1K–3K"
    if amt < 10000: return "$3K–10K"
    if amt < 50000: return "$10K–50K"
    return ">$50K"

@st.cache_data(show_spinner=False)
def process_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # Parse datetime
    if "updated_at" in df.columns:
        df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
        df["month"] = df["updated_at"].dt.strftime("%Y-%m")
        df["hour"]  = df["updated_at"].dt.hour
        df["weekday"] = df["updated_at"].dt.day_name()
    else:
        df["month"] = "unknown"
        df["hour"]  = 0
        df["weekday"] = "unknown"

    df["pair"] = df["from_currency"].astype(str) + "/" + df["to_currency"].astype(str)
    df["fx_revenue_usd"] = pd.to_numeric(df["fx_revenue_usd"], errors="coerce").fillna(0)
    df["spread"] = pd.to_numeric(df["spread"], errors="coerce").fillna(0)
    df["amount_usd"] = df.apply(get_usd_amount, axis=1)
    df["tier"] = df["amount_usd"].apply(assign_tier)
    df["source"] = df["source"].astype(str).str.strip().str.lower()
    return df

def fmt_usd(v):
    if abs(v) >= 1e6: return f"${v/1e6:.2f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.1f}K"
    return f"${v:,.0f}"

def fmt_pct(v, t):
    return f"{v/t*100:.1f}%" if t > 0 else "0%"

def sim_revenue(sub: pd.DataFrame, overrides: dict, elast: float) -> float:
    total = 0.0
    for _, r in sub.iterrows():
        old_sp = r["spread"]
        new_sp = overrides.get(r["pair"], old_sp)
        sf = new_sp / old_sp if old_sp > 0 else 1.0
        sp_diff = max(0, old_sp - new_sp)
        vf = 1 + elast * sp_diff
        total += r["fx_revenue_usd"] * sf * vf
    return total

def agg_sim(df: pd.DataFrame, overrides: dict, elast: float, by: list) -> pd.DataFrame:
    rows = []
    for keys, grp in df.groupby(by, observed=True):
        base = grp["fx_revenue_usd"].sum()
        sim  = sim_revenue(grp, overrides, elast)
        n    = len(grp)
        row  = dict(zip(by, keys if isinstance(keys, tuple) else [keys]))
        row.update({"n": n, "base_rev": base, "sim_rev": sim,
                    "delta": sim - base, "avg_spread": grp["spread"].mean()})
        rows.append(row)
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:16px 0 20px">
      <div style="display:flex;align-items:center;gap:11px;margin-bottom:16px">
        <div style="width:30px;height:30px;background:#1251A3;border-radius:2px;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
            <rect x="1" y="8" width="3" height="7" rx="0" fill="white" opacity=".7"/>
            <rect x="6" y="4" width="3" height="11" rx="0" fill="white"/>
            <rect x="11" y="1" width="3" height="14" rx="0" fill="white" opacity=".55"/>
          </svg>
        </div>
        <div>
          <div style="font-size:13px;font-weight:600;color:#D8E6F2;
                      letter-spacing:-.01em;line-height:1.25;
                      font-family:'IBM Plex Sans',sans-serif">FX Revenue</div>
          <div style="font-size:9px;color:#38526E;letter-spacing:.14em;
                      text-transform:uppercase;font-family:monospace">Analytics · Stape</div>
        </div>
      </div>
      <div style="height:1px;background:rgba(255,255,255,0.07)"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── File upload ──
    st.markdown("### 📂 Данные")
    uploaded = st.file_uploader(
        "CSV или Excel (.xlsx)",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
    )

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded)
            else:
                df_raw = pd.read_excel(uploaded)

            missing = REQUIRED_COLS - set([c.strip().lower() for c in df_raw.columns])
            if missing:
                st.error(f"Отсутствуют колонки: {', '.join(missing)}")
                df_raw = None
            else:
                st.success(f"✓ {uploaded.name}  ·  {len(df_raw):,} строк")
        except Exception as e:
            st.error(f"Ошибка: {e}")
            df_raw = None
    else:
        df_raw = None
        st.info("Загрузите CSV или Excel для анализа")
        with st.expander("Ожидаемые колонки"):
            st.markdown("""
            `updated_at` · `source` · `from_currency` · `to_currency`  
            `from_amount` · `to_amount` · `spread` · `fx_revenue_usd`  
            `original_rate_fixed` · `rate_usd_fixed`
            """)

    st.markdown("### 🔍 Фильтры")

    if df_raw is not None:
        df = process_dataframe(df_raw)
        avail_pairs   = sorted(df["pair"].unique().tolist())
        avail_sources = sorted(df["source"].unique().tolist())
        avail_months  = sorted(df["month"].unique().tolist())
        avail_tiers   = [t for t in TIERS if t in df["tier"].unique()]
    else:
        avail_pairs   = PAIRS
        avail_sources = ["company", "user"]
        avail_months  = list(MONTHS_RU.keys())
        avail_tiers   = TIERS
        df = pd.DataFrame()

    sel_pairs   = st.multiselect("Валютная пара",   avail_pairs,   default=avail_pairs,   key="f_pair")
    sel_sources = st.multiselect("Источник",        avail_sources, default=avail_sources, key="f_src")
    sel_tiers   = st.multiselect("Тир суммы (USD)", avail_tiers,   default=avail_tiers,   key="f_tier")
    sel_months  = st.multiselect("Месяц",           avail_months,  default=avail_months,  key="f_month",
                                 format_func=lambda m: MONTHS_RU.get(m, m))

    st.markdown("### ⚙️ Симуляция")
    elast = st.slider(
        "Эластичность объёма (× / п.п.)",
        min_value=0.0, max_value=2.0, value=0.0, step=0.05,
        help="0 = объём не меняется при изменении спреда\n"
             "0.4 = +40% сделок при снижении на 1 п.п.",
    )

    st.markdown("---")
    if st.button("↺ Сбросить фильтры", use_container_width=True):
        st.rerun()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    src_str = "данные не загружены" if df.empty else f"{len(df):,} транзакций · {df['month'].nunique()} мес."
    st.markdown(f"""
    <div style="padding:20px 0 4px">
      <div style="font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
                  color:#96A3B5;margin-bottom:6px;font-family:'IBM Plex Mono',monospace">
        FX · Revenue Analytics
      </div>
      <h1 style="font-size:26px;font-weight:300;letter-spacing:-.03em;margin:0;
                 color:#0D1B2E;font-family:'IBM Plex Sans',sans-serif;line-height:1.1">
        FX Revenue <span style="font-weight:600">Dashboard</span>
      </h1>
      <div style="font-size:12px;color:#96A3B5;margin-top:6px;
                  font-family:'IBM Plex Mono',monospace;letter-spacing:.02em">
        {src_str}
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    tag = "demo" if df.empty else "live"
    label = "Demo режим" if df.empty else "Реальные данные"
    st.markdown(
        f'<div style="text-align:right;padding-top:28px">'
        f'<span class="fin-tag tag-{tag}">● {label}</span></div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NO DATA STATE
# ─────────────────────────────────────────────
if df.empty:
    st.markdown("""
    <div class="fin-card-rule" style="text-align:center;padding:64px 40px">
      <div style="font-size:36px;margin-bottom:18px;opacity:.35">▦</div>
      <div style="font-size:18px;font-weight:500;color:#0D1B2E;margin-bottom:8px;
                  font-family:'IBM Plex Sans',sans-serif;letter-spacing:-.01em">
        Загрузите данные для анализа
      </div>
      <div style="font-size:13px;color:#5A6A80;max-width:480px;margin:0 auto;line-height:1.6">
        Импортируйте CSV или Excel файл через панель слева.<br>
        Дашборд автоматически рассчитает метрики, распределение спреда,
        динамику выручки и точки безубыточности.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Show expected schema
    st.markdown("#### Пример структуры файла")
    sample = pd.DataFrame({
        "updated_at":        ["2026-01-15 10:23:00", "2026-01-15 11:05:00"],
        "source":            ["company", "user"],
        "from_currency":     ["USD", "EUR"],
        "to_currency":       ["RUB", "USD"],
        "from_amount":       [5000.00, 1200.00],
        "to_amount":         [455000.00, 1320.00],
        "spread":            [3.5, 2.0],
        "original_rate_fixed":[91.0, 1.10],
        "rate_usd_fixed":    [1.0, 1.0],
        "fx_revenue_usd":    [175.00, 24.00],
    })
    st.dataframe(sample, use_container_width=True, hide_index=True)
    st.stop()

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
filt = df[
    df["pair"].isin(sel_pairs if sel_pairs else avail_pairs) &
    df["source"].isin(sel_sources if sel_sources else avail_sources) &
    df["tier"].isin(sel_tiers if sel_tiers else avail_tiers) &
    df["month"].isin(sel_months if sel_months else avail_months)
].copy()

# ─────────────────────────────────────────────
# SPREAD OVERRIDES (state)
# ─────────────────────────────────────────────
if "ov" not in st.session_state:
    st.session_state.ov = {}

def get_mean_spread(pair_df: pd.DataFrame, pair: str) -> float:
    sub = pair_df[pair_df["pair"] == pair]
    return float(sub["spread"].mean()) if len(sub) > 0 else 3.5

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab_ov, tab_calc, tab_analysis, tab_export = st.tabs(
    ["📈  Обзор", "🧮  Калькулятор", "🔬  Анализ", "⬇️  Экспорт"]
)

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab_ov:

    base_total = filt["fx_revenue_usd"].sum()
    sim_total  = sim_revenue(filt, st.session_state.ov, elast)
    delta_total = sim_total - base_total
    n_total     = len(filt)
    avg_rev     = sim_total / n_total if n_total > 0 else 0
    base_all    = df["fx_revenue_usd"].sum()

    # ── KPI row ──
    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.metric("Выручка (симуляция)",  fmt_usd(sim_total),
               delta=f"{'+' if delta_total>=0 else ''}{fmt_usd(delta_total)} vs база" if abs(delta_total) > 0.5 else None)
    kc2.metric("Транзакций",           f"{n_total:,}",
               delta=fmt_pct(n_total, len(df)))
    kc3.metric("Ср. выручка / сделку", fmt_usd(avg_rev))
    kc4.metric("Доля в общей выручке", fmt_pct(base_total, base_all) if base_all > 0 else "100%",
               delta=fmt_usd(base_all))

    st.markdown("---")

    # ── Monthly stacked bar ──
    months_in_filter = sorted(filt["month"].unique())
    pairs_in_filter  = [p for p in PAIRS if p in filt["pair"].unique()]

    fig_monthly = go.Figure()
    for pair in pairs_in_filter:
        sub_p = filt[filt["pair"] == pair]
        y_vals = []
        for m in months_in_filter:
            grp = sub_p[sub_p["month"] == m]
            y_vals.append(sim_revenue(grp, st.session_state.ov, elast) if len(grp) > 0 else 0)
        fig_monthly.add_trace(go.Bar(
            name=pair, x=[MONTHS_RU.get(m, m) for m in months_in_filter],
            y=y_vals, marker_color=PAIR_COLORS.get(pair, "#888"),
            hovertemplate=f"<b>{pair}</b><br>%{{x}}: %{{y:$,.0f}}<extra></extra>",
        ))
    fig_monthly.update_layout(**PLOTLY_LAYOUT, title="Динамика выручки по месяцам",
                               barmode="stack", height=280)
    st.plotly_chart(fig_monthly, use_container_width=True)

    # ── Row 2: tiers + sources ──
    col_t, col_s = st.columns(2)

    with col_t:
        tiers_in_filt = [t for t in TIERS if t in filt["tier"].unique()]
        tier_revs = []
        for t in tiers_in_filt:
            grp = filt[filt["tier"] == t]
            tier_revs.append(sim_revenue(grp, st.session_state.ov, elast))

        fig_tier = go.Figure(go.Bar(
            x=tier_revs, y=tiers_in_filt, orientation="h",
            marker=dict(
                color=tier_revs,
                colorscale=[[0, "#EBF1FB"], [0.45, "#6B9FE4"], [1.0, "#1251A3"]],
            ),
            hovertemplate="%{y}: %{x:$,.0f}<extra></extra>",
        ))
        fig_tier.update_layout(**PLOTLY_LAYOUT, title="Тиры объёма (USD)", height=260)
        fig_tier.update_yaxes(categoryorder="array", categoryarray=tiers_in_filt[::-1])
        st.plotly_chart(fig_tier, use_container_width=True)

    with col_s:
        sources = filt["source"].unique().tolist()
        src_rev = [sim_revenue(filt[filt["source"] == s], st.session_state.ov, elast) for s in sources]
        src_n   = [len(filt[filt["source"] == s]) for s in sources]

        fig_src = make_subplots(specs=[[{"secondary_y": True}]])
        fig_src.add_trace(go.Bar(name="Выручка", x=sources, y=src_rev,
                                  marker_color=["#1251A3", "#2E6B8A"],
                                  hovertemplate="%{x}: %{y:$,.0f}<extra></extra>"), secondary_y=False)
        fig_src.add_trace(go.Scatter(name="Сделки", x=sources, y=src_n, mode="markers",
                                      marker=dict(size=10, color=["#5C3D99", "#0A6E45"],
                                                  symbol="diamond"),
                                      hovertemplate="%{x}: %{y:,} сделок<extra></extra>"), secondary_y=True)
        fig_src.update_layout(**PLOTLY_LAYOUT, title="Источники (выручка / кол-во)", height=260)
        fig_src.update_yaxes(title_text="Выручка $", secondary_y=False,
                              gridcolor="#EFF1F5", color="#96A3B5",
                              title_font=dict(size=10, color="#96A3B5"))
        fig_src.update_yaxes(title_text="Сделки", secondary_y=True,
                              gridcolor=None, color="#96A3B5",
                              title_font=dict(size=10, color="#96A3B5"))
        st.plotly_chart(fig_src, use_container_width=True)

    # ── Pair breakdown table ──
    st.markdown("#### Разбивка по парам")
    pair_rows = []
    for pair in pairs_in_filter:
        sub = filt[filt["pair"] == pair]
        b = sub["fx_revenue_usd"].sum()
        s = sim_revenue(sub, st.session_state.ov, elast)
        n = len(sub)
        mu = sub["spread"].mean()
        custom_spreads = sub["spread"].nunique() > 1
        pair_rows.append({
            "Пара":            pair,
            "Транзакций":      n,
            "База ($)":        round(b, 2),
            "Симуляция ($)":   round(s, 2),
            "Δ ($)":           round(s - b, 2),
            "Δ (%)":           round((s - b) / b * 100, 2) if b > 0 else 0,
            "μ-спред (%)":     round(mu, 3),
            "Кастом":          "✓" if custom_spreads else "—",
            "Тип":             "RUB" if "RUB" in pair else "no RUB",
            "Доля (%)":        round(b / base_total * 100, 1) if base_total > 0 else 0,
        })
    pair_df_show = pd.DataFrame(pair_rows).sort_values("Симуляция ($)", ascending=False)

    def color_delta(val):
        if isinstance(val, (int, float)):
            c = "#0A6E45" if val > 0.5 else "#A61C22" if val < -0.5 else "#96A3B5"
            fw = "600" if abs(val) > 0.5 else "400"
            return f"color: {c}; font-weight: {fw}; font-family: 'IBM Plex Mono', monospace"
        return ""

    st.dataframe(
        pair_df_show.style.map(color_delta, subset=["Δ ($)", "Δ (%)"]),
        use_container_width=True, hide_index=True,
    )

# ══════════════════════════════════════════════
# TAB 2 — CALCULATOR
# ══════════════════════════════════════════════
with tab_calc:

    st.markdown("""
    <div class="fin-card-rule" style="margin-bottom:1rem">
      <div style="font-size:12px;color:#5A6A80;line-height:1.6">
        <b style="color:#0D1B2E;font-weight:600">Как работает симуляция:</b>&ensp;изменение спреда пересчитывается как&ensp;
        <code style="background:#EBF1FB;color:#1251A3;padding:2px 7px;border-radius:2px;
                     font-family:'IBM Plex Mono',monospace;font-size:11px">
        rev_sim = rev_base × (sp_new / sp_real) × (1 + E × max(0, sp_old − sp_new))
        </code><br>
        <span style="color:#96A3B5;font-size:11px">
        Используется реальный средний спред (μ) из данных.
        Пары с кастомными спредами отмечены <span style="color:#7A4A00">●</span>
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Spread sliders ──
    pairs_in_filt2 = [p for p in PAIRS if p in filt["pair"].unique()]
    cols = st.columns(3)

    for idx, pair in enumerate(pairs_in_filt2):
        sub = filt[filt["pair"] == pair]
        mean_sp  = get_mean_spread(filt, pair)
        min_sp   = float(sub["spread"].min()) if len(sub) > 0 else mean_sp
        max_sp   = float(sub["spread"].max()) if len(sub) > 0 else mean_sp
        has_cust = sub["spread"].nunique() > 1

        # Current override or mean
        cur_sp = st.session_state.ov.get(pair, mean_sp)

        with cols[idx % 3]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;
                           color:{PAIR_COLORS.get(pair,'#2C3E55')}">{pair}</span>
              <span style="font-size:9px;color:#96A3B5;font-family:'IBM Plex Mono',monospace">
                μ={mean_sp:.3f}%{"&nbsp;&nbsp;<span style='color:#7A4A00'>●&nbsp;кастом</span>" if has_cust else ""}
              </span>
            </div>
            <div style="font-size:10px;color:#96A3B5;font-family:'IBM Plex Mono',monospace;margin-bottom:5px">
              мин {min_sp:.2f}% · макс {max_sp:.2f}% · n={len(sub):,}
            </div>
            """, unsafe_allow_html=True)

            new_sp = st.slider(
                f"Спред {pair}", min_value=0.5, max_value=5.5,
                value=round(cur_sp, 2), step=0.05,
                key=f"sp_{pair}", label_visibility="collapsed",
            )
            st.session_state.ov[pair] = new_sp

            base_p = sub["fx_revenue_usd"].sum()
            sim_p  = sim_revenue(sub, st.session_state.ov, elast)
            d_p    = sim_p - base_p
            dc     = "#0A6E45" if d_p > 0.5 else "#A61C22" if d_p < -0.5 else "#96A3B5"
            sc     = "#7A4A00" if new_sp < mean_sp else "#0A6E45" if new_sp > mean_sp else "#96A3B5"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:11px;
                        font-family:'IBM Plex Mono',monospace;margin-top:3px">
              <span style="color:{sc};font-weight:600">{new_sp:.2f}%
                {"↓" if new_sp < mean_sp else "↑" if new_sp > mean_sp else ""}
              </span>
              <span style="color:#5A6A80">{fmt_usd(sim_p)}</span>
              <span style="color:{dc};font-weight:500">{'+' if d_p>=0 else ''}{fmt_usd(d_p)}</span>
            </div>
            <hr style="margin:10px 0">
            """, unsafe_allow_html=True)

    # ── Summary bar ──
    base_filt  = filt["fx_revenue_usd"].sum()
    sim_filt   = sim_revenue(filt, st.session_state.ov, elast)
    delta_filt = sim_filt - base_filt
    pct_filt   = delta_filt / base_filt * 100 if base_filt > 0 else 0
    dc_main    = "#0A6E45" if delta_filt > 0 else "#A61C22"

    st.markdown(f"""
    <div class="fin-card" style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;margin-top:1rem">
      <div style="padding:16px 22px;border-right:1px solid #DDE1EA">
        <div class="fin-label">База (реальная)</div>
        <div style="font-size:24px;font-weight:400;font-family:'IBM Plex Mono',monospace;
                    color:#2C3E55;letter-spacing:-.02em">{fmt_usd(base_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-right:1px solid #DDE1EA;border-top:2px solid #1251A3">
        <div class="fin-label">Симуляция</div>
        <div style="font-size:24px;font-weight:600;font-family:'IBM Plex Mono',monospace;
                    color:#1251A3;letter-spacing:-.02em">{fmt_usd(sim_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-right:1px solid #DDE1EA;border-top:2px solid {dc_main}">
        <div class="fin-label">Δ абсолютное</div>
        <div style="font-size:24px;font-weight:600;font-family:'IBM Plex Mono',monospace;
                    color:{dc_main};letter-spacing:-.02em">
          {'+' if delta_filt>=0 else ''}{fmt_usd(delta_filt)}</div>
      </div>
      <div style="padding:16px 22px;border-top:2px solid {dc_main}">
        <div class="fin-label">Δ процентное</div>
        <div style="font-size:24px;font-weight:600;font-family:'IBM Plex Mono',monospace;
                    color:{dc_main};letter-spacing:-.02em">
          {'+' if pct_filt>=0 else ''}{pct_filt:.1f}%</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Breakeven table ──
    st.markdown("#### Точки безубыточности")
    be_rows = []
    for pair in pairs_in_filt2:
        sub  = filt[filt["pair"] == pair]
        if not len(sub): continue
        mu   = get_mean_spread(filt, pair)
        ns   = st.session_state.ov.get(pair, mu)
        base = sub["fx_revenue_usd"].sum()
        sim  = sim_revenue(sub, st.session_state.ov, elast)
        d    = sim - base

        sp_diff = mu - ns
        if sp_diff > 0.01:
            sf = ns / mu
            req_e = (1 / sf - 1) / sp_diff
            need_vol = f"+{req_e*100:.0f}% объёма"
            req_e_str = f"{req_e:.2f}×/п.п."
            verdict = "✅ реалистично" if req_e <= 0.3 else "⚠️ сомнительно" if req_e <= 0.7 else "❌ нереалистично"
        elif sp_diff < -0.01:
            need_vol, req_e_str, verdict = "повышение", "—", "↑ рост выручки"
        else:
            need_vol, req_e_str, verdict = "—", "—", "без изменений"

        be_rows.append({
            "Пара": pair, "μ-спред (%)": round(mu, 3), "Новый (%)": round(ns, 2),
            "База ($)": round(base, 2), "Симуляция ($)": round(sim, 2),
            "Δ ($)": round(d, 2), "Δ (%)": round(d / base * 100, 1) if base > 0 else 0,
            "Нужен объём": need_vol, "Нужна эласт.": req_e_str, "Оценка": verdict,
        })

    be_df = pd.DataFrame(be_rows)
    st.dataframe(
        be_df.style.map(color_delta, subset=["Δ ($)", "Δ (%)"]),
        use_container_width=True, hide_index=True,
    )

    # ── Base vs Sim chart ──
    fig_cmp = go.Figure()
    for pair in pairs_in_filt2:
        sub = filt[filt["pair"] == pair]
        b = sub["fx_revenue_usd"].sum()
        s = sim_revenue(sub, st.session_state.ov, elast)
        fig_cmp.add_trace(go.Bar(
            name=f"{pair} база", x=[pair], y=[b],
            marker_color="#DDE1EA", marker_line=dict(color="#C4CAD5", width=1),
            hovertemplate=f"<b>{pair} база</b>: %{{y:$,.0f}}<extra></extra>",
        ))
        fig_cmp.add_trace(go.Bar(
            name=f"{pair} симул.", x=[pair], y=[s],
            marker_color=PAIR_COLORS.get(pair, "#1251A3"),
            hovertemplate=f"<b>{pair} симуляция</b>: %{{y:$,.0f}}<extra></extra>",
        ))
    fig_cmp.update_layout(**PLOTLY_LAYOUT, barmode="group",
                           title="База vs Симуляция по парам", height=280,
                           showlegend=False)
    st.plotly_chart(fig_cmp, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — ANALYSIS
# ══════════════════════════════════════════════
with tab_analysis:

    # ── Heatmap ──
    st.markdown("#### Тепловая карта: выручка пара × месяц")
    pairs_hm  = [p for p in PAIRS if p in filt["pair"].unique()]
    months_hm = sorted(filt["month"].unique())
    hm_data   = np.zeros((len(pairs_hm), len(months_hm)))
    for i, pair in enumerate(pairs_hm):
        for j, month in enumerate(months_hm):
            sub = filt[(filt["pair"] == pair) & (filt["month"] == month)]
            hm_data[i, j] = sim_revenue(sub, st.session_state.ov, elast) if len(sub) > 0 else 0

    fig_hm = go.Figure(go.Heatmap(
        z=hm_data, x=[MONTHS_RU.get(m, m) for m in months_hm], y=pairs_hm,
        colorscale=[[0, "#F7F8FA"], [0.25, "#C8D9F5"], [0.65, "#4E82D0"], [1.0, "#0D2E6E"]],
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:$,.0f}<extra></extra>",
        text=[[fmt_usd(v) if v > 0 else "—" for v in row] for row in hm_data],
        texttemplate="%{text}",
        textfont=dict(size=10, color="#0D1B2E", family="'IBM Plex Mono',monospace"),
        colorbar=dict(
            tickfont=dict(size=10, color="#96A3B5"),
            outlinewidth=0,
            thickness=12,
        ),
    ))
    fig_hm.update_layout(**PLOTLY_LAYOUT, height=300)
    fig_hm.update_yaxes(gridcolor=None,
                         tickfont=dict(family="'IBM Plex Mono',monospace", size=11, color="#2C3E55"))
    st.plotly_chart(fig_hm, use_container_width=True)

    col_a1, col_a2 = st.columns(2)

    # ── Spread distribution ──
    with col_a1:
        st.markdown("#### Распределение спреда")
        spread_rows = []
        for pair in pairs_hm:
            sub = filt[filt["pair"] == pair]
            if not len(sub): continue
            for sp_val, grp in sub.groupby("spread"):
                spread_rows.append({
                    "pair": pair, "spread": sp_val,
                    "n": len(grp), "rev": grp["fx_revenue_usd"].sum(),
                    "pct_n": len(grp) / len(sub) * 100,
                })
        if spread_rows:
            sp_df = pd.DataFrame(spread_rows)
            fig_sd = px.bar(sp_df, x="pct_n", y="pair", color="spread",
                            orientation="h", barmode="stack",
                            color_continuous_scale=["#C4CAD5", "#6B9FE4", "#1251A3", "#0D2E6E"],
                            labels={"pct_n": "% транзакций", "pair": ""},
                            hover_data={"n": True, "rev": ":.0f"},
                            height=280)
            fig_sd.update_layout(**PLOTLY_LAYOUT,
                                  coloraxis_colorbar=dict(
                                      tickfont=dict(size=10, color="#96A3B5"),
                                      outlinewidth=0, thickness=10,
                                  ))
            fig_sd.update_coloraxes(colorbar_title="Спред %")
            st.plotly_chart(fig_sd, use_container_width=True)

            with st.expander("Детали распределения спреда"):
                pivot = sp_df.pivot_table(index="pair", columns="spread",
                                           values="pct_n", aggfunc="sum", fill_value=0)
                pivot.columns = [f"{c:.1f}%" for c in pivot.columns]
                def color_pct(val):
                    if not isinstance(val, (int, float)) or val == 0:
                        return "color: #C4CAD5"
                    intensity = min(val / 100, 1.0)
                    # White → blue gradient
                    r = int(235 - (235 - 18)  * intensity)
                    g = int(238 - (238 - 81)  * intensity)
                    b = int(245 - (245 - 163) * intensity)
                    return (f"color: rgb({r},{g},{b}); "
                            f"font-weight: {'600' if val > 50 else '400'}; "
                            f"font-family: 'IBM Plex Mono', monospace")
                st.dataframe(pivot.round(1).style.map(color_pct),
                             use_container_width=True)

    # ── Hourly pattern ──
    with col_a2:
        if "hour" in filt.columns:
            st.markdown("#### Паттерн по часам UTC")
            hourly = filt.groupby("hour").agg(
                avg_rev=("fx_revenue_usd", "mean"),
                n=("fx_revenue_usd", "count"),
            ).reset_index()

            fig_hr = make_subplots(specs=[[{"secondary_y": True}]])
            fig_hr.add_trace(go.Scatter(
                x=hourly["hour"], y=hourly["avg_rev"], name="Ср. выручка",
                mode="lines+markers", fill="tozeroy",
                line=dict(color="#1251A3", width=2),
                fillcolor="rgba(18,81,163,0.07)",
                marker=dict(size=4, color="#1251A3"),
                hovertemplate="Час %{x}:00 · %{y:$,.0f}<extra></extra>",
            ), secondary_y=False)
            fig_hr.add_trace(go.Bar(
                x=hourly["hour"], y=hourly["n"], name="Кол-во",
                marker_color="rgba(18,81,163,0.1)",
                marker_line=dict(color="rgba(18,81,163,0.2)", width=1),
                hovertemplate="Час %{x}:00 · %{y} сделок<extra></extra>",
            ), secondary_y=True)
            fig_hr.update_layout(**PLOTLY_LAYOUT, height=280)
            fig_hr.update_layout(legend=dict(x=0, y=1))
            fig_hr.update_xaxes(tickmode="linear", tick0=0, dtick=3,
                                 gridcolor="#EFF1F5")
            fig_hr.update_yaxes(title_text="Ср. выручка $", secondary_y=False,
                                 title_font=dict(size=10, color="#96A3B5"))
            fig_hr.update_yaxes(title_text="Кол-во", secondary_y=True,
                                 title_font=dict(size=10, color="#96A3B5"))
            st.plotly_chart(fig_hr, use_container_width=True)

    # ── Weekday pattern ──
    if "weekday" in filt.columns and filt["weekday"].nunique() > 1:
        st.markdown("#### Паттерн по дням недели")
        day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        day_ru    = {"Monday":"Пн","Tuesday":"Вт","Wednesday":"Ср",
                     "Thursday":"Чт","Friday":"Пт","Saturday":"Сб","Sunday":"Вс"}
        weekday_agg = filt.groupby("weekday").agg(
            avg_rev=("fx_revenue_usd", "mean"), n=("fx_revenue_usd", "count"),
            total=("fx_revenue_usd", "sum"),
        ).reindex([d for d in day_order if d in filt["weekday"].unique()]).reset_index()
        weekday_agg["day_ru"] = weekday_agg["weekday"].map(day_ru)

        fig_wd = go.Figure(go.Bar(
            x=weekday_agg["day_ru"], y=weekday_agg["avg_rev"],
            marker=dict(
                color=weekday_agg["avg_rev"],
                colorscale=[[0, "#EBF1FB"], [0.5, "#6B9FE4"], [1.0, "#1251A3"]],
                line=dict(color="rgba(18,81,163,0.2)", width=1),
            ),
            hovertemplate="%{x}: %{y:$,.0f} средняя<extra></extra>",
        ))
        fig_wd.update_layout(**PLOTLY_LAYOUT, height=220,
                              title="Средняя выручка по дням недели")
        st.plotly_chart(fig_wd, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — EXPORT
# ══════════════════════════════════════════════
with tab_export:

    st.markdown("### Экспорт результатов")

    exp_c1, exp_c2 = st.columns(2)

    # ── CSV export ──
    with exp_c1:
        st.markdown("""
        <div class="fin-card-rule">
          <div class="fin-label">CSV · Выборка</div>
          <div style="font-size:13px;font-weight:500;color:#0D1B2E;margin-bottom:4px">
            Агрегированные данные
          </div>
          <div style="font-size:12px;color:#5A6A80">
            По текущему фильтру с симулированной выручкой и дельтой
          </div>
        </div>
        """, unsafe_allow_html=True)

        agg_exp = agg_sim(filt, st.session_state.ov, elast,
                          by=["pair", "tier", "source", "month"])
        csv_buf = agg_exp.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Скачать CSV", data=csv_buf,
                           file_name="fx_revenue_filtered.csv", mime="text/csv",
                           use_container_width=True)

    # ── Excel export ──
    with exp_c2:
        st.markdown("""
        <div class="fin-card-rule">
          <div class="fin-label">Excel · Полный отчёт</div>
          <div style="font-size:13px;font-weight:500;color:#0D1B2E;margin-bottom:4px">
            4 листа
          </div>
          <div style="font-size:12px;color:#5A6A80">
            Сводка · По парам · По тирам · По месяцам
          </div>
        </div>
        """, unsafe_allow_html=True)

        xl_buf = io.BytesIO()
        with pd.ExcelWriter(xl_buf, engine="openpyxl") as writer:
            # Sheet 1: summary
            summary_data = {
                "Метрика": ["Транзакций (фильтр)", "База", "Симуляция", "Δ $", "Δ %",
                            "Эластичность", "Дата создания"],
                "Значение": [len(filt), round(base_total, 2), round(sim_total, 2),
                             round(delta_filt, 2), round(pct_filt, 2), elast,
                             datetime.now().strftime("%Y-%m-%d %H:%M")],
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name="Сводка", index=False)

            # Sheet 2: by pair
            agg_sim(filt, st.session_state.ov, elast, by=["pair"]).to_excel(
                writer, sheet_name="По парам", index=False)

            # Sheet 3: by tier
            agg_sim(filt, st.session_state.ov, elast, by=["tier"]).to_excel(
                writer, sheet_name="По тирам", index=False)

            # Sheet 4: monthly
            agg_sim(filt, st.session_state.ov, elast, by=["month", "pair"]).to_excel(
                writer, sheet_name="По месяцам", index=False)

        xl_buf.seek(0)
        st.download_button("⬇️ Скачать Excel", data=xl_buf.read(),
                           file_name="fx_revenue_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    # ── Spread config export ──
    st.markdown("#### Текущие настройки спреда")
    ov_pairs = [p for p in PAIRS if p in filt["pair"].unique()]
    sp_config = [{
        "pair": p, "mean_spread": round(get_mean_spread(filt, p), 3),
        "simulated_spread": round(st.session_state.ov.get(p, get_mean_spread(filt, p)), 2),
        "elasticity": elast,
    } for p in ov_pairs]
    st.dataframe(pd.DataFrame(sp_config), use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Скачать настройки спреда (CSV)",
        data=pd.DataFrame(sp_config).to_csv(index=False).encode("utf-8"),
        file_name="spread_config.csv", mime="text/csv",
    )

    # ── Raw filtered export ──
    st.markdown("#### Сырые данные (по фильтру)")
    st.dataframe(filt.head(500), use_container_width=True, hide_index=True)
    st.caption(f"Показано 500 из {len(filt):,} строк")
    st.download_button(
        "⬇️ Скачать все отфильтрованные данные (CSV)",
        data=filt.to_csv(index=False).encode("utf-8"),
        file_name="fx_data_filtered.csv", mime="text/csv",
    )
