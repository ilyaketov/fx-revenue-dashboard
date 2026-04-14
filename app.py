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
    page_title="FX Revenue Dashboard · Stape",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# STAPE DESIGN SYSTEM
# ─────────────────────────────────────────────
STAPE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root tokens ── */
:root {
  --bg:          #080818;
  --bg2:         #0F1030;
  --bg3:         #161840;
  --bg4:         #1E2050;
  --purple:      #7B2FF7;
  --purple-lt:   #9B5FFF;
  --blue:        #4A9DFF;
  --blue-dk:     #2D6FCC;
  --indigo:      #6366F1;
  --violet:      #8B5CF6;
  --grad:        linear-gradient(135deg, #7B2FF7 0%, #4A9DFF 100%);
  --grad-soft:   linear-gradient(135deg, rgba(123,47,247,0.15) 0%, rgba(74,157,255,0.15) 100%);
  --bdr:         rgba(123,47,247,0.18);
  --bdr2:        rgba(74,157,255,0.25);
  --tx:          #E8EAFF;
  --tx2:         #9095C8;
  --tx3:         #4A4F7A;
  --green:       #10D9A0;
  --red:         #FF5572;
  --amber:       #FFB020;
}

/* ── Global ── */
html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, sans-serif !important;
  background: var(--bg) !important;
  color: var(--tx) !important;
}
.main .block-container {
  padding: 1.5rem 2rem 2rem;
  max-width: 1400px;
  background: var(--bg) !important;
}
.stApp { background: var(--bg) !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--bdr) !important;
}
[data-testid="stSidebar"] * { color: var(--tx) !important; }
[data-testid="stSidebar"] .stMarkdown h3 {
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: .1em !important;
  text-transform: uppercase !important;
  color: var(--tx3) !important;
  margin: 1rem 0 .4rem !important;
}

/* ── Multiselect / widgets ── */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--bdr) !important;
  border-radius: 8px !important;
  color: var(--tx) !important;
}
.stSlider > div { color: var(--tx) !important; }
.stSlider [data-testid="stTickBar"] { display: none; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  border: 1.5px dashed var(--purple) !important;
  background: rgba(123,47,247,0.04) !important;
  border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
  background: rgba(123,47,247,0.08) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  gap: 0;
  background: var(--bg2) !important;
  border-bottom: 1px solid var(--bdr) !important;
  border-radius: 0 !important;
  padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  border-radius: 0 !important;
  color: var(--tx3) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 12px 20px !important;
  transition: all .15s !important;
}
.stTabs [aria-selected="true"] {
  background: transparent !important;
  border-bottom: 2px solid var(--purple) !important;
  color: var(--purple-lt) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: transparent !important;
  padding: 1.5rem 0 !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--grad) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  padding: 8px 16px !important;
  transition: all .2s !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 20px rgba(123,47,247,0.4) !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] > button {
  background: var(--bg3) !important;
  color: var(--purple-lt) !important;
  border: 1px solid var(--bdr2) !important;
  border-radius: 8px !important;
  font-size: 12px !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: var(--bg4) !important;
  border-color: var(--purple) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
  background: var(--bg2) !important;
  border: 1px solid var(--bdr) !important;
  border-radius: 12px !important;
  padding: 16px 20px !important;
}
[data-testid="stMetric"] > div:first-child {
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: .06em !important;
  text-transform: uppercase !important;
  color: var(--tx3) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
  font-size: 26px !important;
  font-weight: 700 !important;
  color: var(--tx) !important;
}
[data-testid="stMetricDelta"] {
  font-size: 12px !important;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
  background: var(--bg2) !important;
  border: 1px solid var(--bdr) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}
.dvn-scroller { background: var(--bg2) !important; }

/* ── Divider ── */
hr { border-color: var(--bdr) !important; opacity: 1 !important; }

/* ── Expanders ── */
details {
  background: var(--bg2) !important;
  border: 1px solid var(--bdr) !important;
  border-radius: 10px !important;
  padding: 4px 12px !important;
}
summary { color: var(--tx2) !important; font-size: 13px !important; }

/* ── Info / success boxes ── */
[data-testid="stInfo"] {
  background: rgba(74,157,255,0.07) !important;
  border: 1px solid rgba(74,157,255,0.25) !important;
  border-radius: 8px !important;
  color: var(--blue) !important;
}
[data-testid="stSuccess"] {
  background: rgba(16,217,160,0.07) !important;
  border: 1px solid rgba(16,217,160,0.25) !important;
  border-radius: 8px !important;
  color: var(--green) !important;
}
[data-testid="stWarning"] {
  background: rgba(255,176,32,0.07) !important;
  border: 1px solid rgba(255,176,32,0.25) !important;
  border-radius: 8px !important;
  color: var(--amber) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 3px; }

/* ── Custom card ── */
.stape-card {
  background: var(--bg2);
  border: 1px solid var(--bdr);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 1rem;
}
.stape-card-grad {
  background: var(--grad-soft);
  border: 1px solid var(--bdr2);
  border-radius: 12px;
  padding: 18px 20px;
}
.stape-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--tx3);
  margin-bottom: 6px;
}
.stape-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}
.tag-rub  { background: rgba(255,176,32,0.12); color: #FFB020; border: 1px solid rgba(255,176,32,0.25); }
.tag-norub{ background: rgba(16,217,160,0.10); color: #10D9A0; border: 1px solid rgba(16,217,160,0.25); }
.tag-live { background: rgba(16,217,160,0.10); color: #10D9A0; border: 1px solid rgba(16,217,160,0.25); }
.tag-demo { background: rgba(74,157,255,0.10); color: #4A9DFF; border: 1px solid rgba(74,157,255,0.25); }

/* ── Pair badge ── */
.pair-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 5px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 600;
}
</style>
"""
st.markdown(STAPE_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
PAIRS = ["EUR/RUB", "EUR/USD", "RUB/EUR", "RUB/USD", "USD/EUR", "USD/RUB"]
PAIR_COLORS = {
    "EUR/RUB": "#FFB020", "EUR/USD": "#10D9A0", "RUB/EUR": "#4A9DFF",
    "RUB/USD": "#6366F1", "USD/EUR": "#9B5FFF", "USD/RUB": "#7B2FF7",
}
TIERS = ["<$500", "$500–1K", "$1K–3K", "$3K–10K", "$10K–50K", ">$50K"]
TIER_ORDER = {t: i for i, t in enumerate(TIERS)}

MONTHS_RU = {
    "2025-10": "Окт 25", "2025-11": "Ноя 25", "2025-12": "Дек 25",
    "2026-01": "Янв 26", "2026-02": "Фев 26", "2026-03": "Мар 26", "2026-04": "Апр 26",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9095C8", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(gridcolor="rgba(123,47,247,0.12)", zerolinecolor="rgba(123,47,247,0.12)"),
    yaxis=dict(gridcolor="rgba(123,47,247,0.12)", zerolinecolor="rgba(123,47,247,0.12)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(123,47,247,0.2)",
                borderwidth=1, font=dict(size=11)),
    hoverlabel=dict(bgcolor="#1E2050", bordercolor="#7B2FF7",
                    font=dict(color="#E8EAFF", size=12)),
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
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 16px">
      <div style="width:36px;height:36px;background:linear-gradient(135deg,#7B2FF7,#4A9DFF);
                  border-radius:10px;display:flex;align-items:center;justify-content:center;
                  font-size:16px;flex-shrink:0">💜</div>
      <div>
        <div style="font-size:14px;font-weight:700;color:#E8EAFF;letter-spacing:-.01em">FX Revenue</div>
        <div style="font-size:10px;color:#4A4F7A;font-family:monospace">powered by Stape</div>
      </div>
    </div>
    <hr style="border-color:rgba(123,47,247,0.2);margin:0 0 12px">
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
    st.markdown("""
    <h1 style="font-size:24px;font-weight:700;letter-spacing:-.02em;margin:0;
               background:linear-gradient(135deg,#9B5FFF,#4A9DFF);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent">
      FX Revenue Dashboard
    </h1>
    <div style="font-size:13px;color:#4A4F7A;margin-top:4px;font-family:monospace">
      Анализ и симуляция выручки · {src}
    </div>
    """.format(src="данные не загружены" if df.empty else f"{len(df):,} транзакций · {df['month'].nunique()} мес."),
    unsafe_allow_html=True)
with col_h2:
    tag = "demo" if df.empty else "live"
    label = "Demo режим" if df.empty else "Реальные данные"
    st.markdown(f'<div style="text-align:right;margin-top:10px"><span class="stape-tag tag-{tag}">● {label}</span></div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NO DATA STATE
# ─────────────────────────────────────────────
if df.empty:
    st.markdown("""
    <div class="stape-card-grad" style="text-align:center;padding:60px 40px">
      <div style="font-size:48px;margin-bottom:16px">📊</div>
      <div style="font-size:20px;font-weight:600;color:#E8EAFF;margin-bottom:8px">
        Загрузите данные для анализа
      </div>
      <div style="font-size:14px;color:#9095C8;max-width:500px;margin:0 auto">
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
                               barmode="stack", height=280,
                               title_font=dict(size=14, color="#E8EAFF"))
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
                colorscale=[[0, "#1E2050"], [0.4, "#6366F1"], [1.0, "#7B2FF7"]],
            ),
            hovertemplate="%{y}: %{x:$,.0f}<extra></extra>",
        ))
        fig_tier.update_layout(**PLOTLY_LAYOUT, title="Тиры объёма (USD)",
                               height=260, title_font=dict(size=14, color="#E8EAFF"))
        fig_tier.update_yaxes(categoryorder="array", categoryarray=tiers_in_filt[::-1])
        st.plotly_chart(fig_tier, use_container_width=True)

    with col_s:
        sources = filt["source"].unique().tolist()
        src_rev = [sim_revenue(filt[filt["source"] == s], st.session_state.ov, elast) for s in sources]
        src_n   = [len(filt[filt["source"] == s]) for s in sources]

        fig_src = make_subplots(specs=[[{"secondary_y": True}]])
        fig_src.add_trace(go.Bar(name="Выручка", x=sources, y=src_rev,
                                  marker_color=["#7B2FF7", "#4A9DFF"],
                                  hovertemplate="%{x}: %{y:$,.0f}<extra></extra>"), secondary_y=False)
        fig_src.add_trace(go.Scatter(name="Сделки", x=sources, y=src_n, mode="markers",
                                      marker=dict(size=10, color=["#9B5FFF","#6DD5FA"]),
                                      hovertemplate="%{x}: %{y:,} сделок<extra></extra>"), secondary_y=True)
        fig_src.update_layout(**PLOTLY_LAYOUT, title="Источники (выручка / кол-во)",
                               height=260, title_font=dict(size=14, color="#E8EAFF"))
        fig_src.update_yaxes(title_text="Выручка", secondary_y=False,
                              gridcolor="rgba(123,47,247,0.12)", color="#9095C8")
        fig_src.update_yaxes(title_text="Сделки", secondary_y=True,
                              gridcolor=None, color="#9095C8")
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
            c = "#10D9A0" if val > 0.5 else "#FF5572" if val < -0.5 else "#9095C8"
            return f"color: {c}"
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
    <div class="stape-card-grad" style="margin-bottom:1rem">
      <div style="font-size:13px;color:#9095C8">
        <b style="color:#E8EAFF">Как работает симуляция:</b> изменение спреда пересчитывается как
        <code style="background:rgba(123,47,247,0.2);padding:1px 6px;border-radius:4px">
        new_rev = base_rev × (new_spread / real_spread) × (1 + elasticity × max(0, old − new))
        </code><br>
        <span style="color:#4A4F7A;font-size:11px">
        Используется реальный средний спред (μ) из данных, а не стандартный.
        Пары с кастомными спредами отмечены ●
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
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
              <span style="font-family:monospace;font-size:13px;font-weight:600;
                           color:{PAIR_COLORS.get(pair,'#888')}">{pair}</span>
              <span style="font-size:10px;color:#4A4F7A">
                μ={mean_sp:.3f}%{"  <span style='color:#FFB020'>●кастом</span>" if has_cust else ""}
              </span>
            </div>
            <div style="font-size:10px;color:#4A4F7A;font-family:monospace;margin-bottom:6px">
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
            dc     = "#10D9A0" if d_p > 0.5 else "#FF5572" if d_p < -0.5 else "#9095C8"
            sc     = "#FFB020" if new_sp < mean_sp else "#10D9A0" if new_sp > mean_sp else "#9095C8"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:11px;
                        font-family:monospace;margin-top:2px">
              <span style="color:{sc};font-weight:600">{new_sp:.2f}%
                {"↓" if new_sp < mean_sp else "↑" if new_sp > mean_sp else ""}
              </span>
              <span style="color:#9095C8">{fmt_usd(sim_p)}</span>
              <span style="color:{dc}">{'+' if d_p>=0 else ''}{fmt_usd(d_p)}</span>
            </div>
            <hr style="margin:10px 0;border-color:rgba(123,47,247,0.15)">
            """, unsafe_allow_html=True)

    # ── Summary bar ──
    base_filt  = filt["fx_revenue_usd"].sum()
    sim_filt   = sim_revenue(filt, st.session_state.ov, elast)
    delta_filt = sim_filt - base_filt
    pct_filt   = delta_filt / base_filt * 100 if base_filt > 0 else 0
    dc_main    = "#10D9A0" if delta_filt > 0 else "#FF5572"

    st.markdown(f"""
    <div class="stape-card" style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:20px;margin-top:1rem">
      <div><div class="stape-label">База (реальная)</div>
           <div style="font-size:22px;font-weight:700;font-family:monospace;color:#9095C8">{fmt_usd(base_filt)}</div></div>
      <div><div class="stape-label">Симуляция</div>
           <div style="font-size:22px;font-weight:700;font-family:monospace;
           background:linear-gradient(135deg,#9B5FFF,#4A9DFF);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent">{fmt_usd(sim_filt)}</div></div>
      <div><div class="stape-label">Δ абсолютное</div>
           <div style="font-size:22px;font-weight:700;font-family:monospace;color:{dc_main}">
           {'+' if delta_filt>=0 else ''}{fmt_usd(delta_filt)}</div></div>
      <div><div class="stape-label">Δ процентное</div>
           <div style="font-size:22px;font-weight:700;font-family:monospace;color:{dc_main}">
           {'+' if pct_filt>=0 else ''}{pct_filt:.1f}%</div></div>
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
        fig_cmp.add_trace(go.Bar(name=f"{pair} база", x=[pair], y=[b],
                                  marker_color="rgba(99,102,241,0.35)",
                                  hovertemplate=f"<b>{pair} база</b>: %{{y:$,.0f}}<extra></extra>"))
        fig_cmp.add_trace(go.Bar(name=f"{pair} симуляция", x=[pair], y=[s],
                                  marker_color=PAIR_COLORS.get(pair, "#888"),
                                  hovertemplate=f"<b>{pair} симуляция</b>: %{{y:$,.0f}}<extra></extra>"))
    fig_cmp.update_layout(**PLOTLY_LAYOUT, barmode="group",
                           title="База vs Симуляция по парам", height=280,
                           title_font=dict(size=14, color="#E8EAFF"),
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
        colorscale=[[0, "#0F1030"], [0.3, "#1E1B5E"], [0.6, "#6366F1"], [1.0, "#7B2FF7"]],
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:$,.0f}<extra></extra>",
        text=[[fmt_usd(v) if v > 0 else "—" for v in row] for row in hm_data],
        texttemplate="%{text}", textfont=dict(size=11, color="#E8EAFF"),
    ))
    fig_hm.update_layout(**PLOTLY_LAYOUT, height=300)
    fig_hm.update_yaxes(gridcolor=None, tickfont=dict(family="monospace"))
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
                            color_continuous_scale=["#10D9A0", "#6366F1", "#7B2FF7", "#FF5572"],
                            labels={"pct_n": "% транзакций", "pair": ""},
                            hover_data={"n": True, "rev": ":.0f"},
                            height=280)
            fig_sd.update_layout(**PLOTLY_LAYOUT,
                                  coloraxis_colorbar=dict(tickfont=dict(size=10)),
                                  title_font=dict(size=14, color="#E8EAFF"))
            fig_sd.update_coloraxes(colorbar_title="Спред %")
            st.plotly_chart(fig_sd, use_container_width=True)

            with st.expander("Детали распределения спреда"):
                pivot = sp_df.pivot_table(index="pair", columns="spread",
                                           values="pct_n", aggfunc="sum", fill_value=0)
                pivot.columns = [f"{c:.1f}%" for c in pivot.columns]
                st.dataframe(pivot.round(1).style.background_gradient(
                    cmap="Blues", axis=None), use_container_width=True)

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
                line=dict(color="#7B2FF7", width=2),
                fillcolor="rgba(123,47,247,0.08)",
                marker=dict(size=4),
                hovertemplate="Час %{x}:00 · %{y:$,.0f}<extra></extra>",
            ), secondary_y=False)
            fig_hr.add_trace(go.Bar(
                x=hourly["hour"], y=hourly["n"], name="Кол-во",
                marker_color="rgba(74,157,255,0.2)",
                hovertemplate="Час %{x}:00 · %{y} сделок<extra></extra>",
            ), secondary_y=True)
            fig_hr.update_layout(**PLOTLY_LAYOUT, height=280,
                                  title_font=dict(size=14, color="#E8EAFF"),
                                  legend=dict(x=0, y=1))
            fig_hr.update_xaxes(tickmode="linear", tick0=0, dtick=3,
                                 tickformat="%d:00", gridcolor="rgba(123,47,247,0.12)")
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
                colorscale=[[0, "#1E2050"], [1.0, "#7B2FF7"]],
            ),
            hovertemplate="%{x}: %{y:$,.0f} средняя<extra></extra>",
        ))
        fig_wd.update_layout(**PLOTLY_LAYOUT, height=220, title="Средняя выручка по дням",
                              title_font=dict(size=14, color="#E8EAFF"))
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
        <div class="stape-card">
          <div style="font-size:15px;font-weight:600;margin-bottom:6px">📄 CSV</div>
          <div style="font-size:12px;color:#9095C8">Агрегированные данные по текущему фильтру
          с симулированной выручкой и дельтой</div>
        </div>
        """, unsafe_allow_html=True)

        agg_exp = agg_sim(filt, st.session_state.ov, elast,
                          by=["pair", "tier", "source", "month"])
        csv_buf = agg_exp.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Скачать CSV",  data=csv_buf,
                           file_name="fx_revenue_filtered.csv", mime="text/csv",
                           use_container_width=True)

    # ── Excel export ──
    with exp_c2:
        st.markdown("""
        <div class="stape-card">
          <div style="font-size:15px;font-weight:600;margin-bottom:6px">📊 Excel (полный отчёт)</div>
          <div style="font-size:12px;color:#9095C8">4 листа: Сводка · По парам · По тирам · По месяцам</div>
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
