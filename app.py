import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CricIntel",
    page_icon="🏏",
    layout="wide"
)


deliveries = pd.read_csv("deliveries.csv")
matches = pd.read_csv("matches.csv")


st.sidebar.title("🏏 CricIntel")

st.sidebar.markdown("""
AI Powered Cricket Analytics

Modules:
- Batter Analyzer
- Rivalry Analyzer
- Fantasy Optimizer
- Top Run Scorers
""")

option = st.sidebar.selectbox(
    "Choose Module",
    [
        "Home",
        "Batter Analyzer",
        "Batter vs Bowler",
        "Fantasy Team Optimizer",
        "Top Run Scorers"
    ]
)



player_stats = pd.DataFrame({
    "player":[
        "S Dhawan",
        "V Kohli",
        "RG Sharma",
        "DA Warner"
    ],
    "predicted_points":[
        6526,
        6513,
        6490,
        6196
    ]
})




player_stats = deliveries.groupby('batter').agg({
    'batsman_runs':'sum',
    'ball':'count',
    'is_wicket':'sum'
}).reset_index()

player_stats.columns = [
    'player',
    'runs',
    'balls_faced',
    'dismissals'
]

player_stats['strike_rate'] = (
    player_stats['runs']
    /
    player_stats['balls_faced']
) * 100

player_stats['fantasy_points'] = (
    player_stats['runs']
    +
    player_stats['strike_rate']*0.2
    -
    player_stats['dismissals']*0.5
)

player_stats['predicted_points'] = player_stats['fantasy_points']





st.set_page_config(page_title="CricIntel")

st.title("🏏 CricIntel")
st.subheader("Cricket Analytics Platform")


if option == "Top Run Scorers":

    st.subheader("📈 Top 10 Run Scorers")

    top_batters = deliveries.groupby(
        'batter'
    )['batsman_runs'].sum().sort_values(
        ascending=False
    ).head(10)

    st.bar_chart(top_batters)

    st.subheader("🥧 Run Distribution")

    top_batters = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5)

    fig, ax = plt.subplots()

    ax.pie(
    top_batters.values,
    labels=top_batters.index,
    autopct='%1.1f%%'
    )
    st.pyplot(fig)




if option == "Home":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Deliveries",
            len(deliveries)
        )

    with col2:
        st.metric(
            "Total Matches",
            deliveries['match_id'].nunique()
        )

    with col3:
        st.metric(
            "Players",
            deliveries['batter'].nunique()
        )

    st.markdown("---")

    st.write(
        "Welcome to CricIntel - AI Powered Cricket Analytics Dashboard."
    )

if option == "Batter Analyzer":

    st.subheader("🏏 Batter Analyzer")

    batter = st.selectbox(
        "Select Batter",
        sorted(deliveries['batter'].dropna().unique())
    )

    batter_data = deliveries[
        deliveries['batter'] == batter
    ]

    runs = batter_data['batsman_runs'].sum()
    balls = len(batter_data)

    strike_rate = round((runs / balls) * 100, 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Runs", runs)

    with col2:
        st.metric("Balls", balls)

    with col3:
        st.metric("Strike Rate", strike_rate)

if option == "Batter vs Bowler":

    st.subheader("⚔️ Batter vs Bowler Rivalry")

    batter = st.selectbox(
        "Select Batter",
        sorted(deliveries['batter'].dropna().unique()),
        key="batter_rivalry"
    )

    bowler = st.selectbox(
        "Select Bowler",
        sorted(deliveries['bowler'].dropna().unique()),
        key="bowler_rivalry"
    )

    data = deliveries[
        (deliveries['batter'] == batter) &
        (deliveries['bowler'] == bowler)
    ]

    runs = data['batsman_runs'].sum()
    balls = len(data)

    if balls > 0:
        strike_rate = round((runs / balls) * 100, 2)
    else:
        strike_rate = 0

    dismissals = data['is_wicket'].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Runs Scored", runs)

    with col2:
        st.metric("Balls Faced", balls)

    with col3:
        st.metric("Strike Rate", strike_rate)

    st.metric("Dismissals", dismissals)

    st.write("Ball-by-Ball Record")
    st.dataframe(
    data[
        ['over', 'ball', 'batsman_runs', 'is_wicket']
    ]
)

if option == "Fantasy Team Optimizer":

    st.subheader("🏆 Fantasy Team Optimizer")

    best_xi = player_stats.sort_values(
        'predicted_points',
        ascending=False
    ).head(11)

    captain = best_xi.iloc[0]['player']
    vice_captain = best_xi.iloc[1]['player']

    st.success(f"Captain: {captain}")
    st.info(f"Vice Captain: {vice_captain}")

    st.dataframe(
        best_xi[
            ['player','predicted_points']
        ]
    )


st.markdown("---")
st.markdown(
    "Developed by Prince Prajapati | CricIntel 🏏"
)