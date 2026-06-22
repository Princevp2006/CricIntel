# CricIntel — AI-Powered Cricket Analytics Platform

## Overview

CricIntel is a professional, AI-powered cricket analytics platform built with **Streamlit**, **Pandas**, **Plotly**, and **Scikit-Learn**. It transforms IPL ball-by-ball data into actionable insights for players, teams, venues, and match predictions.

## Features

| Module | Description |
|--------|-------------|
| **Home Dashboard** | Platform KPIs, top performers, quick stats |
| **Batter Analyzer** | Phase-wise batting breakdowns & scoring patterns |
| **Batter vs Bowler** | Head-to-head rivalry statistics |
| **Fantasy Optimizer** | AI-recommended Best XI with captain picks |
| **Top Run Scorers** | Interactive leaderboard visualizations |
| **Win Probability** | Live ML win predictor with gauge & progress bar |
| **Tournament Insights** | Season, venue, toss & team-level analytics |
| **Player Comparison** | Radar & bar charts comparing two players |
| **Venue Analytics** | Stadium scoring patterns & rankings |
| **Team Analytics** | Franchise win rates & top performers |
| **Match Insights** | Ball-by-ball analysis by Match ID |

## Project Structure

```
CricIntel/
├── app.py                          # Landing page
├── pages/
│   ├── 1_Batter_Analyzer.py
│   ├── 2_Batter_vs_Bowler.py
│   ├── 3_Fantasy_Team_Optimizer.py
│   ├── 4_Top_Run_Scorers.py
│   ├── 5_Win_Probability.py
│   ├── 6_Tournament_Insights.py
│   ├── 7_Player_Comparison.py
│   ├── 8_Venue_Analytics.py
│   ├── 9_Team_Analytics.py
│   └── 10_Match_Insights.py
├── utils/
│   ├── data_loader.py              # Cached data loading & aggregations
│   ├── analytics.py                # Stats, ML models, match engine
│   ├── charts.py                   # Plotly chart builders
│   └── components.py               # UI components & premium CSS
├── assets/logo.png
├── data/
│   ├── deliveries.csv
│   └── matches.csv
├── .streamlit/config.toml
└── requirements.txt
```

## Tech Stack

- **Python** · **Pandas** · **NumPy**
- **Streamlit** — dashboard framework
- **Plotly** — interactive visualizations
- **Scikit-Learn** — Random Forest win probability models

## Installation

```bash
git clone https://github.com/princevp2006/CricIntel.git
cd CricIntel
pip install -r requirements.txt
```

Place IPL datasets in `data/`:
- `data/deliveries.csv`
- `data/matches.csv`

## Run

```bash
python -m streamlit run app.py
```

## Deployment

Deploy to [Streamlit Cloud](https://streamlit.io/cloud) by connecting your GitHub repository. Ensure `data/` CSVs are included or loaded from a remote source.

## Developer

**Prince Prajapati** — CricIntel Enterprise Analytics 🏏
