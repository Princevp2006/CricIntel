"""Premium UI components and design system for CricIntel."""

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT / "assets" / "logo.png"

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --ci-bg: #060A14;
    --ci-bg-elevated: #0C1222;
    --ci-glass: rgba(255, 255, 255, 0.035);
    --ci-glass-border: rgba(255, 255, 255, 0.08);
    --ci-glass-hover: rgba(255, 255, 255, 0.06);
    --ci-crimson: #E63946;
    --ci-crimson-glow: rgba(230, 57, 70, 0.35);
    --ci-gold: #F4A261;
    --ci-gold-glow: rgba(244, 162, 97, 0.25);
    --ci-text: #F0F4FF;
    --ci-muted: #8B9CB8;
    --ci-radius-lg: 22px;
    --ci-radius-md: 16px;
    --ci-radius-sm: 12px;
    --ci-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    --ci-shadow-glow: 0 0 40px rgba(230, 57, 70, 0.12);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ci-text);
}

#MainMenu, footer, header { visibility: hidden; height: 0; }

/* ── App background mesh ── */
.stApp {
    background-color: var(--ci-bg);
    background-image:
        radial-gradient(ellipse 80% 60% at 10% -10%, rgba(230,57,70,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 95% 5%, rgba(56,189,248,0.08) 0%, transparent 50%),
        radial-gradient(ellipse 50% 40% at 50% 100%, rgba(244,162,97,0.06) 0%, transparent 55%),
        linear-gradient(180deg, #060A14 0%, #0A1020 50%, #060A14 100%);
    background-attachment: fixed;
}

.block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1320px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(6,10,20,0.97) 0%, rgba(12,18,34,0.98) 100%) !important;
    border-right: 1px solid var(--ci-glass-border) !important;
    backdrop-filter: blur(24px);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    padding-top: 0.5rem;
}
[data-testid="stSidebarNav"] span {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--ci-muted) !important;
}
[data-testid="stSidebarNavLink"] {
    background: transparent !important;
    border-radius: var(--ci-radius-sm) !important;
    padding: 0.55rem 0.85rem !important;
    margin: 0.15rem 0 !important;
    border: 1px solid transparent !important;
    transition: all 0.22s ease !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: var(--ci-glass-hover) !important;
    border-color: var(--ci-glass-border) !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: linear-gradient(135deg, rgba(230,57,70,0.18) 0%, rgba(230,57,70,0.06) 100%) !important;
    border-color: rgba(230,57,70,0.35) !important;
    box-shadow: inset 3px 0 0 var(--ci-crimson), 0 4px 20px rgba(230,57,70,0.1) !important;
}
[data-testid="stSidebarNavLink"] span {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--ci-text) !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
.sidebar-brand {
    text-align: center;
    padding: 0.5rem 0.25rem 1rem;
}
.sidebar-brand img {
    filter: drop-shadow(0 8px 24px rgba(230,57,70,0.2));
    border-radius: 12px;
}
.sidebar-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    color: var(--ci-muted);
    margin: 0.35rem 0 0;
    letter-spacing: 0.02em;
}
.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--ci-glass-border), transparent);
    margin: 1rem 0 1.25rem;
}
.sidebar-stat-pill {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-sm);
    padding: 0.6rem 0.85rem;
    margin-bottom: 0.5rem;
    backdrop-filter: blur(12px);
}
.sidebar-stat-pill span:first-child {
    font-size: 0.75rem;
    color: var(--ci-muted);
    font-weight: 500;
}
.sidebar-stat-pill span:last-child {
    font-family: 'Outfit', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--ci-gold);
}

/* ── Gradient page header ── */
.page-header {
    position: relative;
    background: linear-gradient(135deg,
        rgba(19,32,56,0.85) 0%,
        rgba(12,18,34,0.75) 45%,
        rgba(230,57,70,0.08) 100%);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-lg);
    padding: 2.25rem 2.5rem;
    margin-bottom: 2rem;
    overflow: hidden;
    backdrop-filter: blur(20px);
    box-shadow: var(--ci-shadow), var(--ci-shadow-glow);
}
.page-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--ci-crimson), var(--ci-gold), var(--ci-crimson));
    background-size: 200% 100%;
    animation: shimmer 4s linear infinite;
}
.page-header::after {
    content: '';
    position: absolute;
    top: -60%; right: -15%;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(230,57,70,0.12) 0%, transparent 65%);
    pointer-events: none;
}
.page-header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(230,57,70,0.12);
    border: 1px solid rgba(230,57,70,0.3);
    color: #FF8A93;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.85rem;
}
.page-header-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 800;
    color: var(--ci-text);
    margin: 0;
    line-height: 1.15;
    letter-spacing: -0.02em;
    position: relative;
}
.page-header-sub {
    font-size: clamp(0.95rem, 2vw, 1.05rem);
    color: var(--ci-muted);
    margin: 0.65rem 0 0;
    max-width: 640px;
    line-height: 1.6;
    position: relative;
}

/* ── Hero (home) ── */
.hero-container {
    position: relative;
    background: linear-gradient(135deg,
        rgba(10,22,40,0.9) 0%,
        rgba(12,18,34,0.8) 40%,
        rgba(230,57,70,0.1) 100%);
    border: 1px solid var(--ci-glass-border);
    border-radius: 28px;
    padding: 3rem 2.75rem;
    margin-bottom: 2rem;
    overflow: hidden;
    backdrop-filter: blur(24px);
    box-shadow: var(--ci-shadow), 0 0 60px rgba(230,57,70,0.08);
}
.hero-container::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 85% 20%, rgba(56,189,248,0.1) 0%, transparent 40%),
        radial-gradient(circle at 10% 80%, rgba(244,162,97,0.08) 0%, transparent 40%);
    pointer-events: none;
}
.hero-container::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--ci-crimson), var(--ci-gold), transparent);
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(230,57,70,0.15);
    border: 1px solid rgba(230,57,70,0.35);
    color: #FF9DA3;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    position: relative;
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 0%, #C8D4EA 60%, #F4A261 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
    letter-spacing: -0.03em;
    position: relative;
}
.hero-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.2rem);
    color: var(--ci-muted);
    margin-top: 0.75rem;
    font-weight: 400;
    position: relative;
}
.hero-desc {
    font-size: 1rem;
    color: #A8B8D0;
    margin-top: 1.25rem;
    max-width: 680px;
    line-height: 1.7;
    position: relative;
}

/* ── Glass KPI cards ── */
@keyframes kpi-rise {
    from { opacity: 0; transform: translateY(24px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 rgba(230,57,70,0); }
    50%      { box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 30px rgba(230,57,70,0.15); }
}
.kpi-card {
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-md);
    padding: 1.5rem 1.25rem;
    text-align: left;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1), border-color 0.25s ease, box-shadow 0.25s ease;
    animation: kpi-rise 0.7s cubic-bezier(0.22,1,0.36,1) forwards;
    animation-delay: var(--delay, 0s);
    opacity: 0;
    height: 100%;
    min-height: 130px;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent-line, linear-gradient(90deg, var(--ci-crimson), var(--ci-gold)));
    opacity: 0.8;
}
.kpi-card:hover {
    transform: translateY(-6px);
    border-color: rgba(230,57,70,0.35);
    box-shadow: 0 16px 48px rgba(0,0,0,0.4), 0 0 24px var(--ci-crimson-glow);
}
.kpi-icon-wrap {
    width: 44px; height: 44px;
    border-radius: 12px;
    background: rgba(230,57,70,0.12);
    border: 1px solid rgba(230,57,70,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 1rem;
}
.kpi-value {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.6rem, 3vw, 2rem);
    font-weight: 800;
    color: var(--ci-text);
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1;
}
.kpi-label {
    font-size: 0.72rem;
    color: var(--ci-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.45rem;
}
.kpi-trend {
    font-size: 0.75rem;
    color: #2DD4BF;
    margin-top: 0.5rem;
    font-weight: 500;
}

/* ── Section headers ── */
.section-label {
    font-family: 'Outfit', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ci-crimson);
    margin-bottom: 0.35rem;
}
.section-header {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.25rem, 3vw, 1.55rem);
    font-weight: 700;
    color: var(--ci-text);
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
}
.section-desc {
    color: var(--ci-muted);
    font-size: 0.92rem;
    margin-bottom: 1.75rem;
    line-height: 1.6;
    max-width: 720px;
}
.section-block {
    margin: 2.5rem 0 1.75rem;
}

/* ── Glass panels ── */
.glass-panel {
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-lg);
    padding: 1.75rem;
    backdrop-filter: blur(16px);
    box-shadow: var(--ci-shadow);
    margin-bottom: 1.5rem;
}
.glass-panel-header {
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--ci-text);
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--ci-glass-border);
}

/* ── Module cards ── */
.module-card {
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-md);
    padding: 1.5rem;
    height: 100%;
    backdrop-filter: blur(14px);
    transition: all 0.28s ease;
    cursor: default;
}
.module-card:hover {
    transform: translateY(-4px);
    border-color: rgba(230,57,70,0.3);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 20px rgba(230,57,70,0.08);
}
.module-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(230,57,70,0.2), rgba(244,162,97,0.1));
    border: 1px solid rgba(230,57,70,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}
.module-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--ci-text);
    margin: 0 0 0.4rem;
}
.module-desc {
    font-size: 0.82rem;
    color: var(--ci-muted);
    line-height: 1.55;
    margin: 0;
}

/* ── Performer / player cards ── */
.performer-card, .player-card {
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-md);
    padding: 1.5rem;
    backdrop-filter: blur(14px);
    transition: all 0.25s ease;
}
.performer-card:hover, .player-card:hover {
    border-color: rgba(230,57,70,0.3);
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.performer-title {
    font-family: 'Outfit', sans-serif;
    color: var(--ci-gold);
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
.performer-name {
    font-family: 'Outfit', sans-serif;
    color: var(--ci-text);
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0.6rem 0 0.35rem;
    letter-spacing: -0.01em;
}
.performer-stat {
    color: var(--ci-muted);
    font-size: 0.85rem;
    font-weight: 500;
}
.player-card.captain {
    border-color: rgba(244,162,97,0.45);
    background: linear-gradient(135deg, rgba(244,162,97,0.08), var(--ci-glass));
}
.player-card.vice {
    border-color: rgba(139,156,184,0.35);
}
.player-rank {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--ci-crimson), #B91C3C);
    color: white;
    width: 30px; height: 30px;
    border-radius: 10px;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 0.82rem;
    margin-right: 0.65rem;
    box-shadow: 0 4px 12px rgba(230,57,70,0.35);
}
.player-name {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    color: var(--ci-text);
    font-size: 1rem;
}
.player-meta {
    color: var(--ci-muted);
    font-size: 0.8rem;
    margin-top: 0.35rem;
    padding-left: 2.5rem;
}
.badge-captain {
    background: linear-gradient(135deg, var(--ci-gold), #E8923A);
    color: #0A0A0A;
    padding: 0.12rem 0.45rem;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 800;
    margin-left: 0.45rem;
    vertical-align: middle;
}
.badge-vice {
    background: rgba(139,156,184,0.25);
    color: var(--ci-text);
    padding: 0.12rem 0.45rem;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    margin-left: 0.45rem;
}

/* ── Captain / VC spotlight ── */
.spotlight-card {
    border-radius: var(--ci-radius-lg);
    padding: 2rem 1.75rem;
    text-align: center;
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
}
.spotlight-card.captain {
    background: linear-gradient(145deg, rgba(244,162,97,0.12), rgba(12,18,34,0.6));
    border: 1px solid rgba(244,162,97,0.35);
    box-shadow: 0 8px 40px rgba(244,162,97,0.1);
}
.spotlight-card.vice {
    background: linear-gradient(145deg, rgba(139,156,184,0.1), rgba(12,18,34,0.6));
    border: 1px solid rgba(139,156,184,0.25);
}
.spotlight-role {
    font-family: 'Outfit', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.spotlight-name {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--ci-text);
    margin: 0.5rem 0;
    letter-spacing: -0.02em;
}
.spotlight-meta {
    color: var(--ci-muted);
    font-size: 0.88rem;
}

/* ── Info / stat banners ── */
.info-banner {
    background: linear-gradient(135deg, rgba(56,189,248,0.08), rgba(12,18,34,0.5));
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: var(--ci-radius-md);
    padding: 1rem 1.35rem;
    backdrop-filter: blur(12px);
    margin: 1rem 0 1.5rem;
    font-size: 0.92rem;
    color: #A8C8E8;
}
.stat-banner {
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-md);
    padding: 1.1rem 1.4rem;
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.75rem;
}
.stat-banner-label { color: var(--ci-muted); font-size: 0.88rem; }
.stat-banner-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #2DD4BF;
}
.stat-banner-meta { color: var(--ci-muted); font-size: 0.8rem; }

/* ── Streamlit metric overrides ── */
div[data-testid="stMetric"] {
    background: var(--ci-glass) !important;
    border: 1px solid var(--ci-glass-border) !important;
    border-radius: var(--ci-radius-md) !important;
    padding: 1.35rem 1.15rem !important;
    backdrop-filter: blur(14px);
    box-shadow: var(--ci-shadow);
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    animation: kpi-rise 0.6s ease forwards;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(230,57,70,0.3) !important;
    box-shadow: 0 12px 36px rgba(0,0,0,0.4), 0 0 20px rgba(230,57,70,0.1);
}
div[data-testid="stMetric"] label {
    color: var(--ci-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif !important;
    color: var(--ci-text) !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(12,18,34,0.5);
    border-radius: 14px;
    padding: 5px;
    border: 1px solid var(--ci-glass-border);
    backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.1rem !important;
    border: 1px solid transparent !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: var(--ci-muted) !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--ci-text) !important;
    background: var(--ci-glass-hover) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(230,57,70,0.85), rgba(185,28,60,0.9)) !important;
    color: white !important;
    border-color: rgba(230,57,70,0.5) !important;
    box-shadow: 0 4px 16px rgba(230,57,70,0.35) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.75rem;
}

/* ── Charts ── */
[data-testid="stPlotlyChart"] {
    background: var(--ci-glass);
    border: 1px solid var(--ci-glass-border);
    border-radius: var(--ci-radius-lg);
    padding: 0.75rem 0.5rem 0.25rem;
    backdrop-filter: blur(12px);
    box-shadow: var(--ci-shadow);
    transition: border-color 0.25s ease;
}
[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(230,57,70,0.2);
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--ci-glass-border) !important;
    border-radius: var(--ci-radius-md) !important;
    overflow: hidden;
    backdrop-filter: blur(8px);
}

/* ── Inputs ── */
.stSelectbox > div > div,
.stNumberInput > div > div > div,
.stSlider > div > div {
    background: var(--ci-glass) !important;
    border-color: var(--ci-glass-border) !important;
    border-radius: var(--ci-radius-sm) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--ci-crimson), #B91C3C) !important;
    border: none !important;
    border-radius: var(--ci-radius-sm) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 20px rgba(230,57,70,0.35) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(230,57,70,0.45) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: var(--ci-glass) !important;
    border: 1px solid var(--ci-glass-border) !important;
    border-radius: var(--ci-radius-md) !important;
    backdrop-filter: blur(12px);
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--ci-muted);
    font-size: 0.82rem;
    padding: 2.5rem 0 1rem;
    margin-top: 3rem;
    border-top: 1px solid var(--ci-glass-border);
    letter-spacing: 0.02em;
}
.footer strong { color: var(--ci-gold); font-weight: 600; }

/* ── Mobile ── */
@media (max-width: 768px) {
    .block-container { padding: 1.25rem 1rem 2rem; }
    .hero-container { padding: 2rem 1.5rem; border-radius: 20px; }
    .page-header { padding: 1.75rem 1.5rem; border-radius: 18px; }
    .kpi-card { min-height: 110px; padding: 1.15rem; }
    .glass-panel { padding: 1.25rem; border-radius: 18px; }
    .stTabs [data-baseweb="tab"] { padding: 0.45rem 0.7rem !important; font-size: 0.78rem !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 1.45rem !important; }
}
@media (max-width: 480px) {
    .hero-title { font-size: 1.85rem; }
    .kpi-value { font-size: 1.45rem; }
}
</style>
"""


def inject_styles() -> None:
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)


def setup_page(title: str, icon: str = "🏏") -> None:
    st.set_page_config(
        page_title=f"{title} | CricIntel",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_styles()


def render_sidebar_branding(summary: dict | None = None) -> None:
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">', unsafe_allow_html=True)
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        else:
            st.markdown("### 🏏 CricIntel")
        st.markdown(
            '<p class="sidebar-tagline">Enterprise Cricket Intelligence</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        if summary:
            st.markdown(
                f"""
                <div class="sidebar-stat-pill">
                    <span>Matches</span><span>{summary['total_matches']:,}</span>
                </div>
                <div class="sidebar-stat-pill">
                    <span>Deliveries</span><span>{summary['total_deliveries']:,}</span>
                </div>
                <div class="sidebar-stat-pill">
                    <span>Players</span><span>{summary['total_players']:,}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", badge: str = "Analytics") -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-header-badge">● {badge}</div>
            <h1 class="page-header-title">{title}</h1>
            {"<p class='page-header-sub'>" + subtitle + "</p>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, description: str = "", label: str = "Insights") -> None:
    st.markdown(
        f"""
        <div class="section-block">
            <div class="section-label">{label}</div>
            <div class="section-header">{title}</div>
            {"<div class='section-desc'>" + description + "</div>" if description else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(
    icon: str,
    value: str,
    label: str,
    delay: float = 0,
    accent: str = "crimson",
    trend: str = "",
) -> str:
    accent_line = (
        "linear-gradient(90deg, #E63946, #F4A261)"
        if accent == "crimson"
        else "linear-gradient(90deg, #38BDF8, #2DD4BF)"
        if accent == "sky"
        else "linear-gradient(90deg, #F4A261, #FFD166)"
    )
    trend_html = f'<div class="kpi-trend">{trend}</div>' if trend else ""
    return f"""
    <div class="kpi-card" style="--delay:{delay}s; --accent-line:{accent_line};">
        <div class="kpi-icon-wrap">{icon}</div>
        <p class="kpi-value">{value}</p>
        <p class="kpi-label">{label}</p>
        {trend_html}
    </div>
    """


def module_card(icon: str, title: str, description: str) -> str:
    return f"""
    <div class="module-card">
        <div class="module-icon">{icon}</div>
        <p class="module-title">{title}</p>
        <p class="module-desc">{description}</p>
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
        badge = '<span class="badge-captain">CAPTAIN</span>'
    elif role == "vice":
        card_class += " vice"
        badge = '<span class="badge-vice">VICE</span>'
    return f"""
    <div class="{card_class}">
        <span class="player-rank">{rank}</span>
        <span class="player-name">{name}{badge}</span>
        <div class="player-meta">{points:,.0f} pts · {runs:,} runs · SR {sr:.1f}</div>
    </div>
    """


def spotlight_card(role: str, name: str, meta: str, kind: str = "captain") -> str:
    icon = "👑" if kind == "captain" else "🥈"
    color = "#F4A261" if kind == "captain" else "#8B9CB8"
    return f"""
    <div class="spotlight-card {kind}">
        <div style="font-size:2rem;">{icon}</div>
        <div class="spotlight-role" style="color:{color};">{role}</div>
        <div class="spotlight-name">{name}</div>
        <div class="spotlight-meta">{meta}</div>
    </div>
    """


def stat_banner(label: str, value: str, meta: str = "") -> str:
    meta_html = f'<span class="stat-banner-meta">· {meta}</span>' if meta else ""
    return f"""
    <div class="stat-banner">
        <span class="stat-banner-label">{label}</span>
        <span class="stat-banner-value">{value}</span>
        {meta_html}
    </div>
    """


def info_banner(text: str) -> str:
    return f'<div class="info-banner">{text}</div>'


def render_footer() -> None:
    st.markdown(
        '<div class="footer">Built by <strong>Prince Prajapati</strong> · CricIntel Enterprise Analytics</div>',
        unsafe_allow_html=True,
    )
