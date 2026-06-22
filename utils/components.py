"""Reusable UI components and global styling for CricIntel."""

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT / "assets" / "logo.png"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu, footer, header { visibility: hidden; }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Hero */
        .hero-container {
            background: linear-gradient(135deg, #1D2951 0%, #0B1120 50%, #151D2E 100%);
            border: 1px solid rgba(196, 30, 58, 0.3);
            border-radius: 20px;
            padding: 2.5rem 2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        .hero-container::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(196,30,58,0.15) 0%, transparent 70%);
            border-radius: 50%;
        }
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #F8FAFC;
            margin: 0;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            color: #94A3B8;
            margin-top: 0.5rem;
            font-weight: 400;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(196, 30, 58, 0.2);
            color: #F87171;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
            border: 1px solid rgba(196, 30, 58, 0.4);
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #1E293B 0%, #151D2E 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 1.25rem 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: #C41E3A;
        }
        div[data-testid="stMetric"] label {
            color: #94A3B8 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }

        /* Custom KPI card */
        .kpi-card {
            background: linear-gradient(145deg, #1E293B 0%, #151D2E 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.25s ease;
            height: 100%;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            border-color: #C41E3A;
            box-shadow: 0 8px 30px rgba(196, 30, 58, 0.15);
        }
        .kpi-icon { font-size: 2rem; margin-bottom: 0.5rem; }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #F8FAFC;
            margin: 0;
        }
        .kpi-label {
            font-size: 0.8rem;
            color: #94A3B8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: 0.25rem;
        }

        /* Player cards */
        .player-card {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }
        .player-card:hover {
            border-color: #C41E3A;
            box-shadow: 0 4px 20px rgba(196, 30, 58, 0.12);
        }
        .player-card.captain {
            border-color: #F59E0B;
            background: linear-gradient(135deg, #1E293B 0%, #292524 100%);
        }
        .player-card.vice {
            border-color: #94A3B8;
        }
        .player-rank {
            display: inline-block;
            background: #C41E3A;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            text-align: center;
            line-height: 28px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 0.75rem;
        }
        .player-name {
            font-weight: 700;
            color: #F8FAFC;
            font-size: 1rem;
        }
        .player-meta {
            color: #94A3B8;
            font-size: 0.8rem;
            margin-top: 0.25rem;
        }
        .badge-captain {
            background: #F59E0B;
            color: #0F172A;
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            margin-left: 0.5rem;
        }
        .badge-vice {
            background: #64748B;
            color: white;
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            margin-left: 0.5rem;
        }

        /* Section headers */
        .section-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #F8FAFC;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(196, 30, 58, 0.4);
        }
        .section-desc {
            color: #94A3B8;
            font-size: 0.95rem;
            margin-bottom: 1.25rem;
        }

        /* Performer cards */
        .performer-card {
            background: linear-gradient(145deg, #1E293B, #151D2E);
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 1.25rem;
            text-align: center;
        }
        .performer-card:hover { border-color: #C41E3A; }
        .performer-title {
            color: #F59E0B;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .performer-name {
            color: #F8FAFC;
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        .performer-stat {
            color: #94A3B8;
            font-size: 0.85rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0B1120 0%, #151D2E 100%);
            border-right: 1px solid #1E293B;
        }
        [data-testid="stSidebar"] .stRadio label {
            font-weight: 500;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background: #1E293B;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            border: 1px solid #334155;
        }
        .stTabs [aria-selected="true"] {
            background: #C41E3A !important;
            border-color: #C41E3A !important;
        }

        /* Dataframe */
        [data-testid="stDataFrame"] {
            border: 1px solid #334155;
            border-radius: 12px;
            overflow: hidden;
        }

        /* Animations */
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 5px rgba(196, 30, 58, 0.3); }
            50% { box-shadow: 0 0 20px rgba(196, 30, 58, 0.6); }
        }
        .hero-container {
            animation: pulse-glow 4s ease-in-out infinite;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #64748B;
            font-size: 0.85rem;
            padding: 2rem 0 0.5rem;
            border-top: 1px solid #1E293B;
            margin-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_page(title: str, icon: str = "🏏") -> None:
    st.set_page_config(
        page_title=f"{title} | CricIntel",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_styles()


def render_sidebar_branding() -> None:
    with st.sidebar:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        else:
            st.markdown("## 🏏 CricIntel")
        st.markdown(
            "<p style='color:#94A3B8;font-size:0.85rem;margin-top:-0.5rem;"
            "text-align:center;'>AI-Powered Cricket Analytics</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")


def kpi_card(icon: str, value: str, label: str) -> str:
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <p class="kpi-value">{value}</p>
        <p class="kpi-label">{label}</p>
    </div>
    """


def section_header(title: str, description: str = "") -> None:
    st.markdown(f'<p class="section-header">{title}</p>', unsafe_allow_html=True)
    if description:
        st.markdown(f'<p class="section-desc">{description}</p>', unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown(
        '<div class="footer">Developed by Prince Prajapati · CricIntel 🏏</div>',
        unsafe_allow_html=True,
    )


def player_card_html(
    rank: int,
    name: str,
    points: float,
    runs: int,
    sr: float,
    role: str = "",
) -> str:
    card_class = "player-card"
    badge = ""
    if role == "captain":
        card_class += " captain"
        badge = '<span class="badge-captain">C</span>'
    elif role == "vice":
        card_class += " vice"
        badge = '<span class="badge-vice">VC</span>'
    return f"""
    <div class="{card_class}">
        <span class="player-rank">{rank}</span>
        <span class="player-name">{name}{badge}</span>
        <div class="player-meta">
            {points:,.0f} pts · {runs:,} runs · SR {sr:.1f}
        </div>
    </div>
    """


def performer_card_html(title: str, name: str, stat: str) -> str:
    return f"""
    <div class="performer-card">
        <div class="performer-title">{title}</div>
        <div class="performer-name">{name}</div>
        <div class="performer-stat">{stat}</div>
    </div>
    """
