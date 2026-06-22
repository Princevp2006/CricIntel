"""Plotly chart builders with CricIntel theme."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "navy": "#1D2951",
    "red": "#C41E3A",
    "gold": "#F59E0B",
    "green": "#10B981",
    "blue": "#3B82F6",
    "purple": "#8B5CF6",
    "teal": "#14B8A6",
}

CHART_PALETTE = [
    COLORS["red"],
    COLORS["gold"],
    COLORS["blue"],
    COLORS["green"],
    COLORS["purple"],
    COLORS["teal"],
    "#EC4899",
    "#F97316",
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E2E8F0", family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=50, b=20),
    colorway=CHART_PALETTE,
    hoverlabel=dict(bgcolor="#1E293B", font_size=13),
)


def _apply_theme(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(title=dict(text=title, font=dict(size=16, color="#F8FAFC")), **PLOTLY_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.15)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.15)", zeroline=False)
    return fig


def bar_chart(
    series: pd.Series,
    title: str,
    horizontal: bool = False,
) -> go.Figure:
    df = series.reset_index()
    df.columns = ["name", "value"]
    if horizontal:
        fig = px.bar(
            df, x="value", y="name", orientation="h",
            color="value",
            color_continuous_scale=["#1D2951", COLORS["red"], COLORS["gold"]],
        )
        fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        fig.update_traces(hovertemplate="<b>%{y}</b><br>Runs: %{x:,}<extra></extra>")
    else:
        fig = px.bar(
            df, x="name", y="value", color="value",
            color_continuous_scale=["#1D2951", COLORS["red"], COLORS["gold"]],
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Runs: %{y:,}<extra></extra>")
    return _apply_theme(fig, title)


def pie_chart(labels: list, values: list, title: str) -> go.Figure:
    fig = go.Figure(
        data=[go.Pie(
            labels=labels, values=values, hole=0.45,
            marker=dict(colors=CHART_PALETTE),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
        )]
    )
    return _apply_theme(fig, title)


def phase_bar_chart(phase_data: dict[str, int], title: str) -> go.Figure:
    fig = px.bar(
        x=list(phase_data.keys()), y=list(phase_data.values()),
        color=list(phase_data.keys()), color_discrete_sequence=CHART_PALETTE,
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Runs: %{y:,}<extra></extra>")
    return _apply_theme(fig, title)


def gauge_chart(value: float, title: str, suffix: str = "%") -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        number=dict(suffix=suffix, font=dict(size=28, color="#F8FAFC")),
        title=dict(text=title, font=dict(size=14, color="#94A3B8")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#64748B"),
            bar=dict(color=COLORS["red"]),
            bgcolor="#1E293B", bordercolor="#334155",
            steps=[
                dict(range=[0, 40], color="#1E293B"),
                dict(range=[40, 70], color="#334155"),
                dict(range=[70, 100], color="#475569"),
            ],
        ),
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0"), height=280)
    return fig


def win_probability_chart(
    team1_prob: float, team2_prob: float, team1: str, team2: str
) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=[team1, team2],
        y=[team1_prob * 100, team2_prob * 100],
        marker_color=[COLORS["blue"], COLORS["red"]],
        text=[f"{team1_prob*100:.1f}%", f"{team2_prob*100:.1f}%"],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Win Prob: %{y:.1f}%<extra></extra>",
    ))
    fig.update_yaxes(range=[0, 100], title="Win Probability (%)")
    return _apply_theme(fig, "Predicted Win Probability")
