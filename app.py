import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="International Powerhouse Index",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Theme / styling — intentionally mirrors the visual language of ScoutAI Recruit
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #080b12;
        --card: rgba(20, 24, 34, 0.96);
        --card-2: rgba(27, 32, 44, 0.97);
        --soft: rgba(255,255,255,0.045);
        --soft-2: rgba(255,255,255,0.07);
        --border: rgba(255,255,255,0.09);
        --border-strong: rgba(255,255,255,0.15);
        --text: #f8fafc;
        --muted: #98a2b3;
        --gold: #f6c453;
        --gold-soft: rgba(246,196,83,0.13);
        --blue: #66a7ff;
        --blue-soft: rgba(102,167,255,0.12);
        --green: #66d19e;
        --green-soft: rgba(102,209,158,0.12);
        --red: #ff6b6b;
        --red-soft: rgba(255,107,107,0.12);
        --violet: #a78bfa;
        --violet-soft: rgba(167,139,250,0.12);
    }

    html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    .stApp { background: radial-gradient(circle at 72% -10%, rgba(246,196,83,0.06), transparent 28%), var(--bg); }
    .block-container { max-width: 1500px; padding-top: 1.5rem; padding-bottom: 5rem; }
    #MainMenu, footer { visibility: hidden; }

    section[data-testid="stSidebar"] { background: #0b0f17; border-right: 1px solid var(--border); }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

    .brand-row { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:.45rem; }
    .brand-mark { display:flex; align-items:center; gap:.8rem; }
    .brand-ball { width:44px; height:44px; border-radius:14px; display:grid; place-items:center; background:linear-gradient(135deg,#171b26,#242b39); border:1px solid var(--border); box-shadow:0 10px 28px rgba(0,0,0,.24); font-size:1.35rem; }
    .brand-title { font-weight:860; letter-spacing:-.04em; font-size:1.3rem; }
    .brand-kicker { color:var(--muted); font-size:.72rem; font-weight:750; letter-spacing:.1rem; text-transform:uppercase; margin-top:.1rem; }
    .prototype-pill { border:1px solid rgba(246,196,83,.28); color:#f8d983; background:var(--gold-soft); padding:.35rem .7rem; border-radius:999px; font-size:.72rem; font-weight:800; letter-spacing:.04rem; }
    .era-pill { display:inline-flex; align-items:center; gap:.38rem; border:1px solid rgba(102,167,255,.28); color:#a9cbff; background:var(--blue-soft); padding:.38rem .72rem; border-radius:999px; font-size:.72rem; font-weight:800; letter-spacing:.035rem; }
    .rank-delta-up { color:#83e6b2; font-size:.72rem; font-weight:800; margin-left:.35rem; }
    .rank-delta-down { color:#ff9a9a; font-size:.72rem; font-weight:800; margin-left:.35rem; }
    .rank-delta-flat { color:var(--muted); font-size:.72rem; font-weight:800; margin-left:.35rem; }
    .era-note { background:linear-gradient(135deg,rgba(102,167,255,.10),rgba(102,167,255,.035)); border:1px solid rgba(102,167,255,.18); border-radius:15px; padding:.9rem 1rem; color:#c9daf5; font-size:.82rem; line-height:1.55; margin:.4rem 0 1rem; }

    .hero { position:relative; overflow:hidden; border:1px solid var(--border); border-radius:26px; padding:2rem 2.15rem; margin-bottom:1.35rem; background:linear-gradient(125deg,rgba(27,32,44,.98),rgba(12,15,23,.98)); box-shadow:0 18px 55px rgba(0,0,0,.24); }
    .hero:after { content:""; position:absolute; width:420px; height:420px; border-radius:50%; right:-160px; top:-250px; background:radial-gradient(circle,rgba(246,196,83,.13),rgba(246,196,83,0)); pointer-events:none; }
    .hero-eyebrow { color:#f5d37b; font-size:.76rem; font-weight:800; letter-spacing:.13rem; text-transform:uppercase; margin-bottom:.7rem; }
    .hero-title { font-size:clamp(2.25rem,4.3vw,4rem); font-weight:900; line-height:.98; letter-spacing:-.065em; max-width:900px; }
    .hero-sub { color:var(--muted); max-width:950px; font-size:1.03rem; line-height:1.65; margin-top:.9rem; }
    .hero-meta { display:flex; flex-wrap:wrap; gap:.6rem; margin-top:1.25rem; }
    .meta-chip { border:1px solid var(--border); background:var(--soft); border-radius:999px; padding:.42rem .72rem; color:#d4d8df; font-size:.78rem; font-weight:700; }

    .section-kicker { color:var(--muted); font-size:.73rem; font-weight:800; letter-spacing:.12rem; text-transform:uppercase; margin-bottom:.4rem; }
    .section-title { font-size:1.55rem; font-weight:850; letter-spacing:-.035em; margin-bottom:.9rem; }

    .metric-card { background:var(--card); border:1px solid var(--border); border-radius:18px; padding:1.15rem 1.2rem; min-height:122px; box-shadow:0 10px 28px rgba(0,0,0,.16); }
    .metric-label { color:var(--muted); text-transform:uppercase; font-size:.68rem; font-weight:800; letter-spacing:.08rem; }
    .metric-value { margin-top:.42rem; font-size:2rem; line-height:1; font-weight:900; letter-spacing:-.055em; }
    .metric-note { color:#c2c8d0; font-size:.78rem; margin-top:.5rem; }

    .podium-card { position:relative; overflow:hidden; background:linear-gradient(135deg,var(--card-2),#11151e); border:1px solid var(--border); border-radius:22px; padding:1.4rem 1.45rem; min-height:250px; box-shadow:0 14px 38px rgba(0,0,0,.2); transition:transform .18s ease,border-color .18s ease; }
    .podium-card:hover { transform:translateY(-2px); border-color:var(--border-strong); }
    .podium-card.rank-1 { border-color:rgba(246,196,83,.32); box-shadow:0 16px 45px rgba(246,196,83,.06); }
    .podium-rank { color:var(--muted); text-transform:uppercase; font-size:.7rem; font-weight:800; letter-spacing:.1rem; }
    .podium-team { font-size:1.55rem; font-weight:880; letter-spacing:-.04em; margin-top:.5rem; display:flex; align-items:center; gap:.55rem; }
    .flag { font-size:1.8rem; }
    .podium-score { font-size:3rem; font-weight:920; letter-spacing:-.07em; line-height:1; margin-top:1rem; }
    .podium-caption { color:var(--muted); font-size:.74rem; margin-top:.25rem; }
    .podium-strip { height:5px; border-radius:999px; background:rgba(255,255,255,.07); margin-top:1rem; overflow:hidden; }
    .podium-strip > span { display:block; height:100%; border-radius:999px; background:linear-gradient(90deg,#f6c453,#f0e09c); }
    .podium-mini { display:grid; grid-template-columns:1fr 1fr; gap:.55rem; margin-top:1rem; }
    .podium-mini-cell { background:var(--soft); border:1px solid rgba(255,255,255,.05); border-radius:10px; padding:.55rem .65rem; }
    .podium-mini-label { color:var(--muted); font-size:.62rem; font-weight:760; text-transform:uppercase; }
    .podium-mini-value { font-size:.9rem; font-weight:800; margin-top:.12rem; }

    .profile-card { background:linear-gradient(135deg,var(--card-2),#11151e); border:1px solid var(--border); border-radius:22px; padding:1.5rem 1.55rem; box-shadow:0 12px 34px rgba(0,0,0,.18); }
    .country-header { display:flex; align-items:center; gap:1rem; }
    .country-flag-big { width:68px; height:68px; border-radius:18px; display:grid; place-items:center; font-size:2.4rem; background:var(--soft); border:1px solid var(--border); }
    .country-name { font-size:2rem; font-weight:900; letter-spacing:-.055em; line-height:1; }
    .country-sub { color:var(--muted); margin-top:.3rem; font-size:.9rem; }
    .score-badge { margin-left:auto; text-align:right; }
    .score-badge-number { font-size:2.4rem; font-weight:920; letter-spacing:-.06em; }
    .score-badge-label { color:var(--muted); text-transform:uppercase; letter-spacing:.08rem; font-size:.64rem; font-weight:800; }

    .component-grid { display:grid; grid-template-columns:repeat(4,minmax(130px,1fr)); gap:.75rem; margin-top:1.25rem; }
    .component-card { background:var(--soft); border:1px solid rgba(255,255,255,.06); border-radius:13px; padding:.82rem .9rem; }
    .component-label { color:var(--muted); font-size:.66rem; font-weight:760; text-transform:uppercase; letter-spacing:.055rem; }
    .component-value { font-size:1.08rem; font-weight:850; margin-top:.3rem; }

    .rank-row { display:grid; grid-template-columns:64px minmax(170px,1.4fr) minmax(200px,2fr) 100px; gap:1rem; align-items:center; padding:.82rem .9rem; border-bottom:1px solid rgba(255,255,255,.06); }
    .rank-row:last-child { border-bottom:none; }
    .rank-number { color:var(--muted); font-weight:850; }
    .rank-team { font-weight:820; letter-spacing:-.02em; display:flex; align-items:center; gap:.5rem; }
    .bar-shell { height:8px; border-radius:999px; background:rgba(255,255,255,.06); overflow:hidden; }
    .bar-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,#f6c453,#f3e1a3); }
    .rank-score { text-align:right; font-weight:900; font-size:1.05rem; }

    .insight-card { background:var(--card); border:1px solid var(--border); border-radius:18px; padding:1.15rem 1.2rem; min-height:150px; }
    .insight-title { font-weight:850; letter-spacing:-.025em; }
    .insight-copy { color:var(--muted); font-size:.85rem; line-height:1.55; margin-top:.45rem; }

    div[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:15px; overflow:hidden; }
    div[data-testid="stPlotlyChart"] { border:1px solid var(--border); border-radius:18px; background:rgba(15,18,27,.7); padding:.35rem; }

    .stTabs [data-baseweb="tab-list"] { gap:.3rem; background:rgba(255,255,255,.025); border:1px solid var(--border); padding:.3rem; border-radius:13px; }
    .stTabs [data-baseweb="tab"] { border-radius:9px; padding:.55rem .9rem; font-weight:750; }
    .stTabs [aria-selected="true"] { background:rgba(246,196,83,.10); color:#f4d379; }

    @media (max-width: 980px) {
        .component-grid { grid-template-columns:repeat(2,minmax(130px,1fr)); }
        .rank-row { grid-template-columns:50px 1fr 85px; }
        .rank-row .bar-shell { display:none; }
    }
    @media (max-width: 620px) {
        .component-grid { grid-template-columns:1fr; }
        .hero { padding:1.4rem; }
        .score-badge { display:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent

FLAG_MAP = {
    "Brazil": "🇧🇷", "Germany": "🇩🇪", "Argentina": "🇦🇷", "Italy": "🇮🇹",
    "France": "🇫🇷", "Spain": "🇪🇸", "Uruguay": "🇺🇾", "England": "🏴",
    "Netherlands": "🇳🇱", "Mexico": "🇲🇽", "Portugal": "🇵🇹", "Belgium": "🇧🇪",
    "Croatia": "🇭🇷", "United States": "🇺🇸", "Egypt": "🇪🇬", "Hungary": "🇭🇺",
    "Colombia": "🇨🇴", "Chile": "🇨🇱", "Sweden": "🇸🇪", "Denmark": "🇩🇰",
    "Switzerland": "🇨🇭", "Japan": "🇯🇵", "South Korea": "🇰🇷", "Iran": "🇮🇷",
    "Morocco": "🇲🇦", "Nigeria": "🇳🇬", "Algeria": "🇩🇿", "Senegal": "🇸🇳",
    "Australia": "🇦🇺", "New Zealand": "🇳🇿", "Austria": "🇦🇹", "Poland": "🇵🇱",
    "Czechia": "🇨🇿", "Czechoslovakia": "🇨🇿", "Soviet Union": "🌐",
    "Yugoslavia": "🌐", "Scotland": "🏴", "Wales": "🏴", "Canada": "🇨🇦",
    "Costa Rica": "🇨🇷", "Paraguay": "🇵🇾", "Ecuador": "🇪🇨", "Cameroon": "🇨🇲",
    "Ghana": "🇬🇭", "Ivory Coast": "🇨🇮", "Tunisia": "🇹🇳", "Saudi Arabia": "🇸🇦",
    "Qatar": "🇶🇦", "Greece": "🇬🇷", "Turkey": "🇹🇷", "Türkiye": "🇹🇷",
}


def flag(team: str) -> str:
    return FLAG_MAP.get(str(team), "🌍")


def pct(value, digits=1):
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "—"


def safe_num(row, col, default=0.0):
    try:
        val = pd.to_numeric(row.get(col), errors="coerce")
        return default if pd.isna(val) else float(val)
    except Exception:
        return default


@st.cache_data(show_spinner=False)
def load_csv(name: str, required=False):
    path = BASE / name
    if not path.exists():
        if required:
            raise FileNotFoundError(name)
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_all():
    powerhouse = load_csv("powerhouse_index.csv", required=True)
    elo = load_csv("elo_history.csv")
    semifinal = load_csv("world_cup_backtest.csv")
    champion = load_csv("champion_backtest.csv")
    matches = load_csv("all_matches.csv")
    return powerhouse, elo, semifinal, champion, matches


try:
    df, elo_history, semifinal_backtest, champion_backtest, all_matches = load_all()
except FileNotFoundError:
    st.error("`powerhouse_index.csv` is missing. Export it from your notebook and place it in the same folder as this app.")
    st.code("powerhouse_export.to_csv('powerhouse_index.csv', index=False)")
    st.stop()

# Normalize team column name from notebook export.
if "team" not in df.columns:
    for candidate in ["powerhouse_team", "index", "Unnamed: 0"]:
        if candidate in df.columns:
            df = df.rename(columns={candidate: "team"})
            break

if "team" not in df.columns or "powerhouse_index" not in df.columns:
    st.error("The Powerhouse CSV must contain `team` and `powerhouse_index` columns.")
    st.stop()

# Rank if it wasn't exported.
df["powerhouse_index"] = pd.to_numeric(df["powerhouse_index"], errors="coerce")
df = df.dropna(subset=["powerhouse_index"]).copy()
df = df.sort_values("powerhouse_index", ascending=False).reset_index(drop=True)
if "rank" not in df.columns:
    df["rank"] = np.arange(1, len(df) + 1)

# Make numeric columns numeric when available.
for col in [
    "world_stage_score", "sustained_strength_score", "continental_score",
    "peak_strength_score", "avg_elo", "peak_elo", "top5_years", "top10_years",
    "wc_score", "titles", "runner_ups", "top4_finishes", "continental_titles",
    "weighted_title_score", "weighted_continental_dominance", "years_active",
]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# -----------------------------------------------------------------------------
# Era / custom-period engine
# -----------------------------------------------------------------------------
WORLD_CUP_CHAMPIONS = {
    1930: "Uruguay", 1934: "Italy", 1938: "Italy", 1950: "Uruguay",
    1954: "Germany", 1958: "Brazil", 1962: "Brazil", 1966: "England",
    1970: "Brazil", 1974: "Germany", 1978: "Argentina", 1982: "Italy",
    1986: "Argentina", 1990: "Germany", 1994: "Brazil", 1998: "France",
    2002: "Brazil", 2006: "Italy", 2010: "Spain", 2014: "Germany",
    2018: "France", 2022: "Argentina", 2026: "Spain",
}

TEAM_ALIASES = {
    "West Germany": "Germany",
}

CONTINENTAL_COMPETITIONS = {
    "European Championship": ("EURO", 0.60),
    "Copa America": ("COPA", 0.60),
    "Copa América": ("COPA", 0.60),
    "African Nations Cup": ("AFCON", 0.40),
    "Asian Cup": ("ASIAN_CUP", 0.35),
    "CONCACAF Championship": ("CONCACAF", 0.30),
    "Oceania Nations Cup": ("OFC", 0.15),
}


def minmax_100(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    finite = values.dropna()
    if finite.empty or float(finite.max()) == float(finite.min()):
        return pd.Series(0.0, index=series.index)
    return 100 * (values - finite.min()) / (finite.max() - finite.min())


def _normalize_team_name(value):
    if pd.isna(value):
        return value
    value = str(value)
    return TEAM_ALIASES.get(value, value)


def build_period_powerhouse(start_year: int, end_year: int, all_time_df: pd.DataFrame,
                            elo_df: pd.DataFrame, matches_df: pd.DataFrame) -> pd.DataFrame:
    """Build an era-specific Powerhouse Index using only information inside the window.

    This keeps the same four conceptual pillars as the all-time model. World Stage is
    based on World Cup finishes inside the window; Sustained/Peak use year-end Elo;
    Continental uses prestige-adjusted tournament match dominance inside the window.
    Components with no information in the selected window are automatically excluded
    and the remaining weights are re-normalized.
    """
    if elo_df is None or matches_df is None:
        raise ValueError("Era mode requires both elo_history.csv and all_matches.csv")

    # ----- Elo: sustained + peak -----
    eh = elo_df.copy()
    eh["date"] = pd.to_datetime(eh["date"], errors="coerce")
    eh["elo"] = pd.to_numeric(eh["elo"], errors="coerce")
    eh = eh.dropna(subset=["date", "team", "elo"])
    eh["year"] = eh["date"].dt.year
    eh["team"] = eh["team"].map(_normalize_team_name)
    eh = eh[(eh["year"] >= start_year) & (eh["year"] <= end_year)].copy()
    if eh.empty:
        raise ValueError("No Elo observations exist inside that time period.")

    year_end = (
        eh.sort_values("date")
        .groupby(["team", "year"], as_index=False)
        .tail(1)
        [["team", "year", "elo"]]
    )
    year_end["world_rank"] = year_end.groupby("year")["elo"].rank(method="min", ascending=False)
    year_end["top5"] = year_end["world_rank"] <= 5
    year_end["top10"] = year_end["world_rank"] <= 10

    period = year_end.groupby("team").agg(
        years_active=("year", "nunique"),
        top5_years=("top5", "sum"),
        top10_years=("top10", "sum"),
        avg_elo=("elo", "mean"),
        peak_elo=("elo", "max"),
    )

    # ----- World Cup pedigree inside period -----
    md = matches_df.copy()
    if "year" not in md.columns:
        md["date"] = pd.to_datetime(md["date"], errors="coerce")
        md["year"] = md["date"].dt.year
    else:
        md["year"] = pd.to_numeric(md["year"], errors="coerce")
        if "date" in md.columns:
            md["date"] = pd.to_datetime(md["date"], errors="coerce")
    for col in ["home_score", "away_score"]:
        if col in md.columns:
            md[col] = pd.to_numeric(md[col], errors="coerce")
    md["home_team"] = md["home_team"].map(_normalize_team_name)
    md["away_team"] = md["away_team"].map(_normalize_team_name)
    md = md[(md["year"] >= start_year) & (md["year"] <= end_year)].copy()

    wc_scores = {}
    wc_titles = {}
    wc_editions = sorted(set(md.loc[md["tournament"] == "World Cup", "year"].dropna().astype(int)))
    for year in wc_editions:
        games = md[(md["tournament"] == "World Cup") & (md["year"] == year)].sort_values("date")
        if games.empty or year not in WORLD_CUP_CHAMPIONS:
            continue
        final = games.tail(1).iloc[0]
        champion = WORLD_CUP_CHAMPIONS[year]
        finalists = [str(final["home_team"]), str(final["away_team"])]
        runner_up = finalists[1] if finalists[0] == champion else finalists[0]
        final_four_games = games.tail(4)
        semifinalists = set(final_four_games["home_team"].astype(str)) | set(final_four_games["away_team"].astype(str))
        others = semifinalists - {champion, runner_up}
        wc_scores[champion] = wc_scores.get(champion, 0) + 10
        wc_scores[runner_up] = wc_scores.get(runner_up, 0) + 6
        wc_titles[champion] = wc_titles.get(champion, 0) + 1
        for team in others:
            wc_scores[team] = wc_scores.get(team, 0) + 2

    wc_score_series = pd.Series(wc_scores, dtype=float, name="wc_score")
    title_series = pd.Series(wc_titles, dtype=float, name="titles")
    period = period.join(wc_score_series, how="outer").join(title_series, how="outer")
    period[["wc_score", "titles"]] = period[["wc_score", "titles"]].fillna(0)

    # ----- Continental dominance inside period -----
    cont = md[md["tournament"].isin(CONTINENTAL_COMPETITIONS)].copy()
    continental_rows = []
    if not cont.empty:
        cont["competition"] = cont["tournament"].map(lambda x: CONTINENTAL_COMPETITIONS[x][0])
        cont["prestige_weight"] = cont["tournament"].map(lambda x: CONTINENTAL_COMPETITIONS[x][1])
        cont["home_points"] = np.select(
            [cont["home_score"] > cont["away_score"], cont["home_score"] == cont["away_score"]],
            [3, 1], default=0,
        )
        cont["away_points"] = np.select(
            [cont["away_score"] > cont["home_score"], cont["home_score"] == cont["away_score"]],
            [3, 1], default=0,
        )
        home = pd.DataFrame({
            "team": cont["home_team"], "competition": cont["competition"],
            "weight": cont["prestige_weight"], "points": cont["home_points"],
            "gd": cont["home_score"] - cont["away_score"],
            "win": (cont["home_score"] > cont["away_score"]).astype(int),
        })
        away = pd.DataFrame({
            "team": cont["away_team"], "competition": cont["competition"],
            "weight": cont["prestige_weight"], "points": cont["away_points"],
            "gd": cont["away_score"] - cont["home_score"],
            "win": (cont["away_score"] > cont["home_score"]).astype(int),
        })
        tm = pd.concat([home, away], ignore_index=True).dropna(subset=["team"])
        by_comp = tm.groupby(["team", "competition"]).agg(
            matches=("team", "size"), points=("points", "sum"), gd=("gd", "sum"),
            wins=("win", "sum"), weight=("weight", "first"),
        ).reset_index()
        by_comp["ppg"] = by_comp["points"] / by_comp["matches"].clip(lower=1)
        by_comp["gdpg"] = by_comp["gd"] / by_comp["matches"].clip(lower=1)
        by_comp["win_pct"] = by_comp["wins"] / by_comp["matches"].clip(lower=1)
        # Bounded match-performance score, then prestige-adjusted.
        by_comp["performance"] = (
            0.55 * (by_comp["ppg"] / 3.0).clip(0, 1)
            + 0.25 * ((np.tanh(by_comp["gdpg"]) + 1) / 2)
            + 0.20 * by_comp["win_pct"].clip(0, 1)
        )
        by_comp["weighted_perf"] = by_comp["performance"] * by_comp["weight"]
        cont_team = by_comp.groupby("team").apply(
            lambda g: np.average(g["weighted_perf"], weights=g["matches"]),
            include_groups=False,
        )
        cont_team.name = "weighted_continental_dominance"
        period = period.join(cont_team, how="outer")
    if "weighted_continental_dominance" not in period.columns:
        period["weighted_continental_dominance"] = 0.0
    period["weighted_continental_dominance"] = period["weighted_continental_dominance"].fillna(0)

    # Keep only teams with some Elo evidence inside the era; otherwise one-off historic identities can leak in.
    period = period[period["avg_elo"].notna()].copy()
    if period.empty:
        raise ValueError("No teams could be scored for that era.")

    # ----- Component scores -----
    period["world_stage_score"] = minmax_100(period["wc_score"])
    period["sustained_strength_score"] = (
        0.50 * minmax_100(period["top5_years"]) + 0.50 * minmax_100(period["avg_elo"])
    )
    period["continental_score"] = minmax_100(period["weighted_continental_dominance"])
    period["peak_strength_score"] = minmax_100(period["peak_elo"])

    component_cols = {
        "world_stage_score": 0.35,
        "sustained_strength_score": 0.30,
        "continental_score": 0.20,
        "peak_strength_score": 0.15,
    }
    # If the selected era contains no World Cup/continental tournament, re-normalize the available pillars.
    active = {c: w for c, w in component_cols.items() if period[c].max() > period[c].min()}
    weight_sum = sum(active.values()) or 1.0
    period["powerhouse_index"] = 0.0
    for col, weight in active.items():
        period["powerhouse_index"] += (weight / weight_sum) * period[col]

    period = period.sort_values("powerhouse_index", ascending=False).copy()
    period["rank"] = np.arange(1, len(period) + 1)
    period["team"] = period.index.astype(str)

    # All-time context: movement versus the primary index.
    all_time_lookup = all_time_df.set_index("team")["rank"] if "rank" in all_time_df.columns else None
    if all_time_lookup is not None:
        period["all_time_rank"] = period["team"].map(all_time_lookup)
        period["rank_change"] = period["all_time_rank"] - period["rank"]
    else:
        period["all_time_rank"] = np.nan
        period["rank_change"] = np.nan

    # Explorer compatibility columns.
    period["continental_titles"] = np.nan
    period["runner_ups"] = np.nan
    period["top4_finishes"] = np.nan
    period["weighted_title_score"] = np.nan
    period["period_start"] = start_year
    period["period_end"] = end_year
    period["period_wc_editions"] = len(wc_editions)

    return period.reset_index(drop=True)


def rank_delta_html(value) -> str:
    if pd.isna(value):
        return ""
    value = int(value)
    if value > 0:
        return f'<span class="rank-delta-up">↑{value}</span>'
    if value < 0:
        return f'<span class="rank-delta-down">↓{abs(value)}</span>'
    return '<span class="rank-delta-flat">—</span>'

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-row">
          <div class="brand-mark">
            <div class="brand-ball">🌍</div>
            <div>
              <div class="brand-title">Powerhouse</div>
              <div class="brand-kicker">International Index</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("A football analytics prototype for measuring international greatness beyond a single ranking system.")
    st.divider()

    st.markdown("**Time frame**")
    mode = st.radio("Ranking mode", ["All-Time", "Custom Era"], horizontal=True, label_visibility="collapsed")

    # Use the available Elo years as the supported era range.
    era_min, era_max = 1950, 2026
    if elo_history is not None and "date" in elo_history.columns:
        _dates = pd.to_datetime(elo_history["date"], errors="coerce")
        if _dates.notna().any():
            era_min = max(1950, int(_dates.dt.year.min()))
            era_max = int(_dates.dt.year.max())

    if mode == "Custom Era":
        default_start = max(era_min, era_max - 6)
        period_range = st.slider("Select period", era_min, era_max, (default_start, era_max))
        start_year, end_year = period_range
        st.caption(f"{start_year}–{end_year} · {end_year-start_year+1} seasons")
    else:
        start_year, end_year = None, None
        st.caption("Full historical model")

    st.divider()
    st.markdown("**Explore**")
    search = st.text_input("Search country", placeholder="Brazil, Spain, France…")

    st.divider()
    st.markdown("**Model DNA**")
    st.caption("World Stage · 35%")
    st.progress(35)
    st.caption("Sustained Strength · 30%")
    st.progress(30)
    st.caption("Continental · 20%")
    st.progress(20)
    st.caption("Peak Strength · 15%")
    st.progress(15)

    st.divider()
    st.markdown('<span class="prototype-pill">V1 RESEARCH PROTOTYPE</span>', unsafe_allow_html=True)

# Build the active ranking table.
view_df = df.copy()
era_error = None
if mode == "Custom Era":
    try:
        view_df = build_period_powerhouse(start_year, end_year, df, elo_history, all_matches)
    except Exception as exc:
        era_error = str(exc)
        view_df = df.copy()

max_rank = st.sidebar.slider("Show top N nations", 10, min(100, len(view_df)), min(25, len(view_df)), 5)
score_floor = st.sidebar.slider("Minimum index", 0.0, 100.0, 0.0, 2.5)

filtered = view_df[view_df["powerhouse_index"] >= score_floor].copy()
if search.strip():
    filtered = filtered[filtered["team"].astype(str).str.contains(search.strip(), case=False, na=False)]
filtered = filtered.head(max_rank)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="brand-row">
      <div class="brand-mark">
        <div class="brand-ball">⚽</div>
        <div>
          <div class="brand-title">International Powerhouse Index</div>
          <div class="brand-kicker">Football greatness, modeled</div>
        </div>
      </div>
      <div class="prototype-pill">V1 • RESEARCH PROTOTYPE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if mode == "Custom Era" and era_error is None:
    hero_title = f"Who ruled international football from {start_year}–{end_year}?"
    hero_sub = "The Powerhouse framework recalculated inside your selected era — historical trophies outside the window no longer count, so rises, declines, and short-term dynasties become visible."
    hero_eye = "Era intelligence · dynamic recalculation"
    period_chip = f'<span class="meta-chip">{start_year}–{end_year}</span>'
else:
    hero_title = "Who are the true powerhouses of international football?"
    hero_sub = "A multi-dimensional ranking built from World Cup pedigree, sustained Elo strength, continental dominance, and peak performance — designed to separate historical greatness from simple current-form rankings."
    hero_eye = "Global football intelligence"
    period_chip = '<span class="meta-chip">All-Time</span>'

st.markdown(
    f"""
    <div class="hero">
      <div class="hero-eyebrow">{hero_eye}</div>
      <div class="hero-title">{hero_title}</div>
      <div class="hero-sub">{hero_sub}</div>
      <div class="hero-meta">
        {period_chip}
        <span class="meta-chip">35% World Stage</span>
        <span class="meta-chip">30% Sustained Strength</span>
        <span class="meta-chip">20% Continental</span>
        <span class="meta-chip">15% Peak Strength</span>
        <span class="meta-chip">Validated vs. Elo baseline</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if mode == "Custom Era" and era_error:
    st.error(f"Custom Era could not be calculated: {era_error}")
    st.caption("Keep `all_matches.csv` and `elo_history.csv` in the same folder as the app. Showing the all-time ranking instead.")
elif mode == "Custom Era":
    st.markdown(
        f'<div class="era-note"><strong>Era Mode is live.</strong> Every score below uses only {start_year}–{end_year}. World Cup events outside the window are ignored, sustained/peak strength use only year-end Elo inside the window, and continental performance is recalculated from matches played inside the era.</div>',
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Snapshot metrics
# -----------------------------------------------------------------------------
leader = view_df.iloc[0]
world_stage_leader = view_df.loc[view_df["world_stage_score"].idxmax()] if "world_stage_score" in view_df else leader
peak_leader = view_df.loc[view_df["peak_strength_score"].idxmax()] if "peak_strength_score" in view_df else leader

m1, m2, m3, m4 = st.columns(4)
metrics = [
    (m1, "#1 Powerhouse", f"{flag(leader['team'])} {leader['team']}", f"Index {leader['powerhouse_index']:.2f}"),
    (m2, "World Stage Leader", f"{flag(world_stage_leader['team'])} {world_stage_leader['team']}", f"Score {safe_num(world_stage_leader, 'world_stage_score'):.1f}"),
    (m3, "Peak Strength Leader", f"{flag(peak_leader['team'])} {peak_leader['team']}", f"Score {safe_num(peak_leader, 'peak_strength_score'):.1f}"),
    (m4, "Tracked Nations", f"{len(view_df):,}", "Scored in active view"),
]
for col, label, value, note in metrics:
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tab_overview, tab_explorer, tab_compare, tab_history, tab_validation, tab_method = st.tabs(
    ["🏆 Rankings", "🔎 Nation Explorer", "⚔️ Compare", "📈 History", "🧪 Validation", "🧠 Methodology"]
)

# -----------------------------------------------------------------------------
# Rankings
# -----------------------------------------------------------------------------
with tab_overview:
    st.markdown('<div class="section-kicker">Elite tier</div><div class="section-title">The podium</div>', unsafe_allow_html=True)
    podium_cols = st.columns(3)
    for i in range(min(3, len(view_df))):
        row = view_df.iloc[i]
        cls = " rank-1" if i == 0 else ""
        with podium_cols[i]:
            st.markdown(
                f"""
                <div class="podium-card{cls}">
                    <div class="podium-rank">Rank {int(row['rank'])}</div>
                    <div class="podium-team"><span class="flag">{flag(row['team'])}</span>{row['team']} {rank_delta_html(row.get("rank_change", np.nan)) if mode == "Custom Era" else ""}</div>
                    <div class="podium-score">{row['powerhouse_index']:.2f}</div>
                    <div class="podium-caption">Powerhouse Index / 100</div>
                    <div class="podium-strip"><span style="width:{min(100,row['powerhouse_index']):.1f}%"></span></div>
                    <div class="podium-mini">
                      <div class="podium-mini-cell"><div class="podium-mini-label">World Stage</div><div class="podium-mini-value">{safe_num(row,'world_stage_score'):.1f}</div></div>
                      <div class="podium-mini-cell"><div class="podium-mini-label">Sustained</div><div class="podium-mini-value">{safe_num(row,'sustained_strength_score'):.1f}</div></div>
                      <div class="podium-mini-cell"><div class="podium-mini-label">Continental</div><div class="podium-mini-value">{safe_num(row,'continental_score'):.1f}</div></div>
                      <div class="podium-mini-cell"><div class="podium-mini-label">Peak</div><div class="podium-mini-value">{safe_num(row,'peak_strength_score'):.1f}</div></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    c_rank, c_chart = st.columns([1.12, 1])
    with c_rank:
        st.markdown('<div class="section-kicker">Leaderboard</div><div class="section-title">Powerhouse table</div>', unsafe_allow_html=True)
        shown = filtered.head(max_rank)
        rows_html = ['<div class="profile-card" style="padding:.45rem .7rem;">']
        denom = max(float(shown["powerhouse_index"].max()), 1.0) if len(shown) else 1.0
        for _, row in shown.iterrows():
            width = max(3, 100 * float(row["powerhouse_index"]) / denom)
            rows_html.append(
                f'<div class="rank-row"><div class="rank-number">#{int(row["rank"])}</div><div class="rank-team"><span>{flag(row["team"])}</span>{row["team"]} {rank_delta_html(row.get("rank_change", np.nan)) if mode == "Custom Era" else ""}</div><div class="bar-shell"><div class="bar-fill" style="width:{width:.1f}%"></div></div><div class="rank-score">{row["powerhouse_index"]:.2f}</div></div>'
            )
        rows_html.append('</div>')
        st.markdown("".join(rows_html), unsafe_allow_html=True)

    with c_chart:
        st.markdown('<div class="section-kicker">Visual ranking</div><div class="section-title">Top nations by index</div>', unsafe_allow_html=True)
        chart_df = filtered.head(min(15, len(filtered))).sort_values("powerhouse_index", ascending=True)
        fig = go.Figure(go.Bar(
            x=chart_df["powerhouse_index"],
            y=[f"{flag(t)} {t}" for t in chart_df["team"]],
            orientation="h",
            text=chart_df["powerhouse_index"].round(1),
            textposition="outside",
            marker=dict(color=chart_df["powerhouse_index"], colorscale=[[0,"#394150"],[1,"#f6c453"]], showscale=False),
            hovertemplate="%{y}<br>Index %{x:.2f}<extra></extra>",
        ))
        fig.update_layout(
            height=620,
            margin=dict(l=10,r=35,t=10,b=10),
            xaxis=dict(range=[0, max(105, chart_df["powerhouse_index"].max()*1.08)], showgrid=True, gridcolor="rgba(255,255,255,.05)", zeroline=False, title="Powerhouse Index"),
            yaxis=dict(showgrid=False),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dce1e8", family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# Nation Explorer
# -----------------------------------------------------------------------------
with tab_explorer:
    st.markdown('<div class="section-kicker">Deep dive</div><div class="section-title">Nation profile</div>', unsafe_allow_html=True)
    choices = view_df["team"].astype(str).tolist()
    default_idx = 0
    selected_team = st.selectbox("Select a nation", choices, index=default_idx, key="explorer_team")
    row = view_df[view_df["team"].astype(str) == selected_team].iloc[0]

    st.markdown(
        f"""
        <div class="profile-card">
          <div class="country-header">
            <div class="country-flag-big">{flag(selected_team)}</div>
            <div>
              <div class="country-name">{selected_team}</div>
              <div class="country-sub">{("Era rank" if mode == "Custom Era" else "Global rank")} #{int(row['rank'])} · {f"{start_year}–{end_year} profile" if mode == "Custom Era" else "International powerhouse profile"}</div>
            </div>
            <div class="score-badge">
              <div class="score-badge-number">{row['powerhouse_index']:.2f}</div>
              <div class="score-badge-label">Powerhouse Index</div>
            </div>
          </div>
          <div class="component-grid">
            <div class="component-card"><div class="component-label">World Stage</div><div class="component-value">{safe_num(row,'world_stage_score'):.1f}</div></div>
            <div class="component-card"><div class="component-label">Sustained Strength</div><div class="component-value">{safe_num(row,'sustained_strength_score'):.1f}</div></div>
            <div class="component-card"><div class="component-label">Continental</div><div class="component-value">{safe_num(row,'continental_score'):.1f}</div></div>
            <div class="component-card"><div class="component-label">Peak Strength</div><div class="component-value">{safe_num(row,'peak_strength_score'):.1f}</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    left, right = st.columns([1, 1.05])
    with left:
        st.markdown('<div class="section-kicker">Legacy profile</div><div class="section-title">What built the score?</div>', unsafe_allow_html=True)
        cards = st.columns(2)
        if mode == "Custom Era":
            stats = [
                ("Period WC titles", int(safe_num(row,"titles")), f"World Cups inside {start_year}–{end_year}"),
                ("Period WC score", pct(safe_num(row,"wc_score"),0), "Finals + semifinal pedigree in this era"),
                ("Top-5 years", int(safe_num(row,"top5_years")), "Elite seasons inside selected window"),
                ("Peak Elo", pct(safe_num(row,"peak_elo"),0), "Highest year-end strength in era"),
                ("Average Elo", pct(safe_num(row,"avg_elo"),0), "Average year-end strength in era"),
                ("Continental score", pct(safe_num(row,"continental_score"),1), "Prestige-adjusted period performance"),
            ]
        else:
            stats = [
                ("World Cup titles", int(safe_num(row,"titles")), "Global trophies"),
                ("World Cup score", pct(safe_num(row,"wc_score"),0), "Titles + finals + top-four runs"),
                ("Top-5 years", int(safe_num(row,"top5_years")), "Post-1950 elite seasons"),
                ("Peak Elo", pct(safe_num(row,"peak_elo"),0), "Highest year-end strength"),
                ("Average Elo", pct(safe_num(row,"avg_elo"),0), "Sustained historical rating"),
                ("Continental titles", int(safe_num(row,"continental_titles")), "Prestige-adjusted elsewhere"),
            ]
        for idx, (label, value, note) in enumerate(stats):
            with cards[idx % 2]:
                st.markdown(f'<div class="metric-card" style="margin-bottom:.7rem;"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-kicker">Score DNA</div><div class="section-title">Four-dimensional profile</div>', unsafe_allow_html=True)
        categories = ["World Stage","Sustained","Continental","Peak"]
        vals = [safe_num(row,"world_stage_score"),safe_num(row,"sustained_strength_score"),safe_num(row,"continental_score"),safe_num(row,"peak_strength_score")]
        fig = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]], fill="toself",
            line=dict(color="#f6c453", width=2.5), fillcolor="rgba(246,196,83,.16)",
            hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
        ))
        fig.update_layout(
            height=450, margin=dict(l=35,r=35,t=20,b=20),
            polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0,100], gridcolor="rgba(255,255,255,.08)", tickfont=dict(color="#89919e")), angularaxis=dict(gridcolor="rgba(255,255,255,.08)", tickfont=dict(color="#dfe3e8", size=12))),
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e5e7eb"), showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# Compare
# -----------------------------------------------------------------------------
with tab_compare:
    st.markdown('<div class="section-kicker">Head-to-head</div><div class="section-title">Compare powerhouse DNA</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        team_a = st.selectbox("Nation A", view_df["team"].tolist(), index=0)
    with c2:
        team_b = st.selectbox("Nation B", view_df["team"].tolist(), index=min(1, len(view_df)-1))
    a = view_df[view_df["team"] == team_a].iloc[0]
    b = view_df[view_df["team"] == team_b].iloc[0]

    ca, cb = st.columns(2)
    for col, r in [(ca,a),(cb,b)]:
        with col:
            st.markdown(
                f'<div class="profile-card"><div class="country-header"><div class="country-flag-big">{flag(r["team"])}</div><div><div class="country-name">{r["team"]}</div><div class="country-sub">Rank #{int(r["rank"])}</div></div><div class="score-badge"><div class="score-badge-number">{r["powerhouse_index"]:.2f}</div><div class="score-badge-label">Index</div></div></div></div>',
                unsafe_allow_html=True,
            )
    st.write("")
    comp_names = ["World Stage","Sustained Strength","Continental","Peak Strength"]
    comp_cols = ["world_stage_score","sustained_strength_score","continental_score","peak_strength_score"]
    fig = go.Figure()
    fig.add_trace(go.Bar(name=team_a, x=comp_names, y=[safe_num(a,c) for c in comp_cols], marker_color="#f6c453"))
    fig.add_trace(go.Bar(name=team_b, x=comp_names, y=[safe_num(b,c) for c in comp_cols], marker_color="#66a7ff"))
    fig.update_layout(barmode="group", height=440, yaxis=dict(range=[0,105], gridcolor="rgba(255,255,255,.06)", title="Score / 100"), xaxis=dict(showgrid=False), margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#e5e7eb"), legend=dict(orientation="h", y=1.08, x=.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# History
# -----------------------------------------------------------------------------
with tab_history:
    st.markdown('<div class="section-kicker">Time machine</div><div class="section-title">Elo history</div>', unsafe_allow_html=True)
    if elo_history is None:
        st.info("Export `elo_history.csv` to unlock the historical trajectory view.")
    else:
        eh = elo_history.copy()
        if "team" not in eh.columns or "elo" not in eh.columns:
            st.warning("`elo_history.csv` needs `team`, `date`, and `elo` columns.")
        else:
            eh["date"] = pd.to_datetime(eh["date"], errors="coerce")
            eh["elo"] = pd.to_numeric(eh["elo"], errors="coerce")
            options = sorted(set(eh["team"].dropna().astype(str)))
            defaults = [t for t in ["Brazil","Germany","Argentina","Spain","France"] if t in options]
            selected = st.multiselect("Compare historical Elo trajectories", options, default=defaults[:4], max_selections=6)
            fig = go.Figure()
            for team in selected:
                td = eh[eh["team"].astype(str) == team].sort_values("date")
                # Year-end sampling keeps the chart clean and matches the research framing.
                if len(td):
                    td = td.assign(year=td["date"].dt.year).groupby("year", as_index=False).tail(1)
                    if mode == "Custom Era":
                        td = td[(td["year"] >= start_year) & (td["year"] <= end_year)]
                    fig.add_trace(go.Scatter(x=td["date"], y=td["elo"], mode="lines", name=f"{flag(team)} {team}", line=dict(width=2.4)))
            fig.update_layout(height=560, margin=dict(l=10,r=10,t=25,b=10), xaxis=dict(gridcolor="rgba(255,255,255,.04)", title="Year"), yaxis=dict(gridcolor="rgba(255,255,255,.06)", title="Elo rating"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#e5e7eb"), legend=dict(orientation="h", y=1.08))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------
with tab_validation:
    st.markdown('<div class="section-kicker">Research lab</div><div class="section-title">Does the index hold up?</div>', unsafe_allow_html=True)
    if semifinal_backtest is None:
        st.info("Export `world_cup_backtest.csv` and `champion_backtest.csv` to unlock the validation dashboard.")
    else:
        sb = semifinal_backtest.copy()
        sb["pre_wc_rank"] = pd.to_numeric(sb["pre_wc_rank"], errors="coerce")
        top5 = 100 * (sb["pre_wc_rank"] <= 5).mean()
        top10 = 100 * (sb["pre_wc_rank"] <= 10).mean()
        top20 = 100 * (sb["pre_wc_rank"] <= 20).mean()
        median_rank = sb["pre_wc_rank"].median()
        v1,v2,v3,v4 = st.columns(4)
        validation_metrics = [(v1,"Semifinalists Top 5",f"{top5:.0f}%","9 / 20 in your backtest"),(v2,"Semifinalists Top 10",f"{top10:.0f}%","16 / 20 in your backtest"),(v3,"Semifinalists Top 20",f"{top20:.0f}%","17 / 20 in your backtest"),(v4,"Median Semifinalist Rank",f"#{median_rank:.0f}","Across 2010–2026")]
        for col,label,value,note in validation_metrics:
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

        st.write("")
        if champion_backtest is not None:
            cb = champion_backtest.copy()
            cb["pre_wc_rank"] = pd.to_numeric(cb["pre_wc_rank"], errors="coerce")
            left, right = st.columns([1.05,1])
            with left:
                st.markdown('<div class="section-kicker">Champion check</div><div class="section-title">Where champions ranked before winning</div>', unsafe_allow_html=True)
                display_cols = [c for c in ["world_cup","champion","pre_wc_rank","powerhouse_index"] if c in cb.columns]
                st.dataframe(cb[display_cols].sort_values("world_cup"), hide_index=True, use_container_width=True)
            with right:
                st.markdown('<div class="section-kicker">Key result</div><div class="section-title">Five tournaments, five elite champions</div>', unsafe_allow_html=True)
                champ_top10 = int((cb["pre_wc_rank"] <= 10).sum())
                st.markdown(f'<div class="insight-card"><div class="insight-title">{champ_top10}/{len(cb)} champions were Top 10 before the tournament.</div><div class="insight-copy">The index is not a World Cup winner predictor. The backtest asks a narrower question: did the model identify eventual champions as established international powerhouses using only pre-tournament information? In this sample, every champion cleared the Top-10 threshold.</div></div>', unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="section-kicker">Benchmark</div><div class="section-title">Powerhouse Index vs. Elo-only baseline</div>', unsafe_allow_html=True)
        baseline = pd.DataFrame({"Metric":["Average rank","Median rank","Top 5 rate","Top 10 rate","Top 20 rate"],"Powerhouse Index":[10.0,6.0,45.0,80.0,85.0],"Elo Only":[9.8,8.0,40.0,70.0,90.0]})
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Powerhouse Index", x=baseline["Metric"].iloc[2:], y=baseline["Powerhouse Index"].iloc[2:], marker_color="#f6c453"))
        fig.add_trace(go.Bar(name="Elo Only", x=baseline["Metric"].iloc[2:], y=baseline["Elo Only"].iloc[2:], marker_color="#66a7ff"))
        fig.update_layout(barmode="group", height=380, yaxis=dict(range=[0,100], ticksuffix="%", gridcolor="rgba(255,255,255,.06)"), xaxis=dict(showgrid=False), margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#e5e7eb"), legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("Backtest sample: 20 World Cup semifinalists across 2010, 2014, 2018, 2022, and 2026. Treat this as prototype validation, not a definitive causal result.")

# -----------------------------------------------------------------------------
# Methodology
# -----------------------------------------------------------------------------
with tab_method:
    st.markdown('<div class="section-kicker">Transparent by design</div><div class="section-title">How the Powerhouse Index works</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    methodology = [
        ("🌍","World Stage","35%","World Cup pedigree. Titles, runner-ups and deep runs are converted into a global-stage score."),
        ("📈","Sustained Strength","30%","Top-five longevity and average year-end Elo measure whether a nation stayed elite across eras."),
        ("🏆","Continental","20%","Continental titles and match dominance are adjusted by tournament prestige before normalization."),
        ("⚡","Peak Strength","15%","Peak year-end Elo rewards the strongest version of a national team without letting one era define everything."),
    ]
    for c,(icon,title,weight,copy) in zip(cols, methodology):
        with c:
            st.markdown(f'<div class="insight-card"><div style="font-size:1.4rem">{icon}</div><div class="insight-title" style="margin-top:.45rem">{title} · {weight}</div><div class="insight-copy">{copy}</div></div>', unsafe_allow_html=True)

    st.write("")
    a,b,c = st.columns(3)
    with a:
        st.markdown('<div class="insight-card"><div class="insight-title">Model testing</div><div class="insight-copy">Baseline Elo was improved with a non-neutral home advantage. Tournament-weighted Elo improved validation slightly but failed the unseen test, so it was rejected rather than forced into the model.</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="insight-card"><div class="insight-title">Sensitivity analysis</div><div class="insight-copy">Alternative weighting philosophies were tested. The leading nations remained highly stable, helping show that the headline ranking is not driven by one arbitrary set of weights.</div></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="insight-card"><div class="insight-title">Interpretation</div><div class="insight-copy">This is a greatness index, not a live power ranking. Elo captures strength; the Powerhouse Index adds historical pedigree, longevity, continental success, and peak dominance.</div></div>', unsafe_allow_html=True)

    st.write("")
    st.caption("Prototype research model. All-Time mode preserves the validated historical index; Custom Era mode recalculates the same four pillars inside the selected time window and re-normalizes unavailable pillars when an era contains no relevant competition.")