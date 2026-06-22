# 🏏 CricIntel — AI-Powered Cricket Analytics Platform

A modern, professional sports analytics dashboard built with **Streamlit**, **Pandas**, **Plotly**, and **Scikit-Learn**. CricIntel transforms IPL ball-by-ball data into actionable insights — from individual batter analysis to ML-powered win probability predictions.

![CricIntel](assets/logo.png)

## ✨ Features

| Module | Description |
|--------|-------------|
| **Home Dashboard** | Hero landing page with platform KPIs, top performers, and quick stats |
| **Batter Analyzer** | Runs, strike rate, phase-wise breakdowns, and scoring patterns |
| **Batter vs Bowler** | Head-to-head stats, dismissals, ball-by-ball table, interactive charts |
| **Fantasy Optimizer** | AI-recommended Best XI with captain & vice-captain picks |
| **Top Run Scorers** | Interactive Plotly bar charts and run distribution pie charts |
| **Win Probability** | Random Forest match outcome predictor |
| **Match Insights** | Venue, team, season, and toss analytics |

## 🎨 Design

- Modern dark theme with cricket branding (navy, red, gold palette)
- Custom CSS — rounded cards, hover effects, animated hero section
- Plotly interactive visualizations throughout
- Responsive layout with sidebar navigation and logo

## 📂 Project Structure

```
CricIntel/
├── app.py                          # Landing page
├── pages/
│   ├── 1_Batter_Analyzer.py
│   ├── 2_Batter_vs_Bowler.py
│   ├── 3_Fantasy_Team_Optimizer.py
│   ├── 4_Top_Run_Scorers.py
│   ├── 5_Win_Probability.py
│   └── 6_Match_Insights.py
├── utils/
│   ├── data_loader.py              # Cached data loading
│   ├── analytics.py                # Stats & ML models
│   ├── charts.py                   # Plotly chart builders
│   └── components.py               # UI components & CSS
├── assets/
│   └── logo.png
├── data/
│   ├── deliveries.csv
│   └── matches.csv
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md
```

## 🛠️ Technologies

- **Python** · **Pandas** · **NumPy**
- **Streamlit** — dashboard framework
- **Plotly** — interactive visualizations
- **Scikit-Learn** — win probability model

## 💻 Installation

```bash
git clone https://github.com/princevp2006/CricIntel.git
cd CricIntel
pip install -r requirements.txt
```

Place IPL datasets in the `data/` folder:

- `data/deliveries.csv`
- `data/matches.csv`

## 🚀 Run

```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## 👨‍💻 Developer

**Prince Prajapati**

CricIntel — AI-Powered Cricket Analytics Platform 🏏
