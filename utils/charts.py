"""Plotly chart builders — premium CricIntel analytics theme."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# ── Brand tokens ──────────────────────────────────────────────────────────────
COLORS = {
    "navy": "#0A1628",
    "navy_mid": "#132038",
    "crimson": "#E63946",
    "crimson_soft": "#FF6B6B",
    "gold": "#F4A261",
    "gold_bright": "#FFD166",
    "emerald": "#2DD4BF",
    "sky": "#38BDF8",
    "violet": "#A78BFA",
    "slate": "#64748B",
    "text": "#F0F4FF",
    "muted": "#8B9CB8",
    "grid": "rgba(139,156,184,0.08)",
    "glass": "rgba(12,18,34,0.6)",
}

CHART_PALETTE = [
    COLORS["crimson"],
    COLORS["gold"],
    COLORS["sky"],
    COLORS["emerald"],
    COLORS["violet"],
    COLORS["crimson_soft"],
    COLORS["gold_bright"],
    "#FB7185",
]

GRADIENT_SCALE = [
    [0.0, COLORS["navy_mid"]],
    [0.45, COLORS["crimson"]],
    [1.0, COLORS["gold"]],
]

# ── Register custom Plotly template ───────────────────────────────────────────
CRICINTEL_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Outfit, DM Sans, Inter, sans-serif",
            color=COLORS["text"],
            size=13,
        ),
        title=dict(
            font=dict(size=17, color=COLORS["text"], family="Outfit, sans-serif"),
            x=0,
            xanchor="left",
            pad=dict(t=0, b=16),
        ),
        colorway=CHART_PALETTE,
        margin=dict(l=12, r=12, t=56, b=12, pad=4),
        hoverlabel=dict(
            bgcolor="rgba(12,18,34,0.92)",
            bordercolor="rgba(230,57,70,0.35)",
            font=dict(size=13, color=COLORS["text"], family="DM Sans, sans-serif"),
        ),
        legend=dict(
            bgcolor="rgba(12,18,34,0.5)",
            bordercolor="rgba(255,255,255,0.06)",
            borderwidth=1,
            font=dict(size=12, color=COLORS["muted"]),
        ),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            linecolor="rgba(255,255,255,0.06)",
            tickcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            title=dict(font=dict(size=12, color=COLORS["muted"])),
            tickfont=dict(size=11, color=COLORS["muted"]),
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            linecolor="rgba(255,255,255,0.06)",
            tickcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            title=dict(font=dict(size=12, color=COLORS["muted"])),
            tickfont=dict(size=11, color=COLORS["muted"]),
        ),
    )
)
pio.templates["cricintel"] = CRICINTEL_TEMPLATE
pio.templates.default = "cricintel"


def _apply_theme(fig: go.Figure, title: str = "", height: int | None = None) -> go.Figure:
    fig.update_layout(
        template="cricintel",
        title=dict(text=title, x=0, xanchor="left"),
    )
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(showgrid=True, gridwidth=1)
    fig.update_yaxes(showgrid=True, gridwidth=1)
    return fig


def _bar_trace_style(fig: go.Figure) -> go.Figure:
    fig.update_traces(
        marker=dict(
            line=dict(width=0),
            cornerradius=6,
        ),
        opacity=0.92,
    )
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
            df,
            x="value",
            y="name",
            orientation="h",
            color="value",
            color_continuous_scale=GRADIENT_SCALE,
        )
        fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        fig.update_traces(
            hovertemplate="<span style='color:#8B9CB8'>Player</span><br>"
            "<b>%{y}</b><br>Runs: <b>%{x:,}</b><extra></extra>"
        )
    else:
        fig = px.bar(
            df,
            x="name",
            y="value",
            color="value",
            color_continuous_scale=GRADIENT_SCALE,
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_traces(
            hovertemplate="<span style='color:#8B9CB8'>Category</span><br>"
            "<b>%{x}</b><br>Value: <b>%{y:,}</b><extra></extra>"
        )

    return _apply_theme(_bar_trace_style(fig), title, height=380)


def pie_chart(labels: list, values: list, title: str) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                marker=dict(
                    colors=CHART_PALETTE,
                    line=dict(color="rgba(6,10,20,0.8)", width=2),
                ),
                textinfo="label+percent",
                textfont=dict(size=11, color=COLORS["text"]),
                hovertemplate="<b>%{label}</b><br>%{value:,} · %{percent}<extra></extra>",
                pull=[0.02] * len(labels),
            )
        ]
    )
    fig.update_layout(showlegend=False)
    fig.add_annotation(
        text="IPL",
        x=0.5,
        y=0.5,
        font=dict(size=14, color=COLORS["muted"], family="Outfit"),
        showarrow=False,
    )
    return _apply_theme(fig, title, height=380)


def phase_bar_chart(phase_data: dict[str, int], title: str) -> go.Figure:
    fig = px.bar(
        x=list(phase_data.keys()),
        y=list(phase_data.values()),
        color=list(phase_data.keys()),
        color_discrete_sequence=CHART_PALETTE,
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Runs: %{y:,}<extra></extra>",
        marker=dict(cornerradius=8, line=dict(width=0)),
    )
    return _apply_theme(fig, title, height=360)


def gauge_chart(value: float, title: str, suffix: str = "%") -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number=dict(
                suffix=suffix,
                font=dict(size=32, color=COLORS["text"], family="Outfit"),
            ),
            title=dict(
                text=title,
                font=dict(size=13, color=COLORS["muted"], family="DM Sans"),
            ),
            gauge=dict(
                axis=dict(
                    range=[0, 100],
                    tickcolor=COLORS["muted"],
                    tickwidth=1,
                    tickfont=dict(size=10, color=COLORS["muted"]),
                ),
                bar=dict(color=COLORS["crimson"], thickness=0.22),
                bgcolor="rgba(12,18,34,0.5)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 40], color="rgba(19,32,56,0.8)"),
                    dict(range=[40, 70], color="rgba(30,48,80,0.6)"),
                    dict(range=[70, 100], color="rgba(230,57,70,0.15)"),
                ],
                threshold=dict(
                    line=dict(color=COLORS["gold"], width=3),
                    thickness=0.8,
                    value=value,
                ),
            ),
        )
    )
    fig.update_layout(
        template="cricintel",
        paper_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=24, r=24, t=48, b=8),
    )
    return fig


def win_probability_chart(
    team1_prob: float, team2_prob: float, team1: str, team2: str
) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=[team1, team2],
            y=[team1_prob * 100, team2_prob * 100],
            marker=dict(
                color=[COLORS["sky"], COLORS["crimson"]],
                line=dict(width=0),
                cornerradius=10,
            ),
            text=[f"{team1_prob * 100:.1f}%", f"{team2_prob * 100:.1f}%"],
            textposition="outside",
            textfont=dict(size=14, color=COLORS["text"], family="Outfit"),
            hovertemplate="<b>%{x}</b><br>Win Probability: %{y:.1f}%<extra></extra>",
        )
    )
    fig.update_yaxes(range=[0, 110], title="Win Probability (%)", ticksuffix="%")
    return _apply_theme(fig, "Predicted Win Probability", height=360)


def apply_chart_layout(fig: go.Figure, title: str = "", height: int = 380) -> go.Figure:
    """Apply premium theme to ad-hoc Plotly figures in page modules."""
    return _apply_theme(fig, title, height)


def radar_chart(
    categories: list[str],
    values_a: list[float],
    values_b: list[float],
    name_a: str,
    name_b: str,
    title: str,
) -> go.Figure:
    """Normalized radar comparison between two players."""
    max_vals = [max(a, b, 1) for a, b in zip(values_a, values_b)]
    norm_a = [v / m * 100 for v, m in zip(values_a, max_vals)]
    norm_b = [v / m * 100 for v, m in zip(values_b, max_vals)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norm_a + [norm_a[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(56,189,248,0.15)",
        line=dict(color=COLORS["sky"], width=2),
        name=name_a,
        hovertemplate="<b>%{theta}</b><br>%{r:.0f}/100<extra></extra>",
    ))
    fig.add_trace(go.Scatterpolar(
        r=norm_b + [norm_b[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(230,57,70,0.15)",
        line=dict(color=COLORS["crimson"], width=2),
        name=name_b,
        hovertemplate="<b>%{theta}</b><br>%{r:.0f}/100<extra></extra>",
    ))
    fig.update_layout(
        template="cricintel",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=COLORS["grid"], tickfont=dict(size=9, color=COLORS["muted"])),
            angularaxis=dict(gridcolor=COLORS["grid"], tickfont=dict(size=11, color=COLORS["text"])),
        ),
        title=dict(text=title, x=0, xanchor="left"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, x=0),
        height=420,
        margin=dict(l=60, r=60, t=60, b=60),
    )
    return fig


def comparison_bar_chart(
    categories: list[str],
    values_a: list,
    values_b: list,
    name_a: str,
    name_b: str,
    title: str,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=name_a, x=categories, y=values_a,
        marker=dict(color=COLORS["sky"], cornerradius=6),
        hovertemplate="<b>%{x}</b><br>" + name_a + ": %{y}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name=name_b, x=categories, y=values_b,
        marker=dict(color=COLORS["crimson"], cornerradius=6),
        hovertemplate="<b>%{x}</b><br>" + name_b + ": %{y}<extra></extra>",
    ))
    fig.update_layout(barmode="group", bargap=0.18, bargroupgap=0.08)
    return _apply_theme(fig, title, height=380)


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None,
    title: str,
    labels: dict | None = None,
) -> go.Figure:
    fig = px.line(
        df, x=x, y=y, color=color,
        color_discrete_sequence=CHART_PALETTE,
        labels=labels or {},
        markers=True,
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    return _apply_theme(fig, title, height=380)


def wickets_timeline_chart(wickets_df: pd.DataFrame, title: str) -> go.Figure:
    if wickets_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No wickets", showarrow=False, font=dict(color=COLORS["muted"]))
        return _apply_theme(fig, title, height=320)

    fig = px.scatter(
        wickets_df,
        x="over_ball",
        y="inning",
        size=[12] * len(wickets_df),
        color="inning",
        hover_data=["player_dismissed", "bowler", "over"],
        color_discrete_sequence=CHART_PALETTE,
        labels={"over_ball": "Over", "inning": "Inning"},
    )
    fig.update_traces(marker=dict(symbol="x", line=dict(width=2)))
    return _apply_theme(fig, title, height=340)


def runs_per_over_chart(runs_df: pd.DataFrame, title: str) -> go.Figure:
    fig = px.bar(
        runs_df,
        x="over",
        y="runs_in_over",
        color="inning",
        barmode="group",
        color_discrete_sequence=CHART_PALETTE,
        labels={"over": "Over", "runs_in_over": "Runs", "inning": "Inning"},
    )
    fig.update_traces(marker=dict(cornerradius=5), hovertemplate="Over %{x}<br>Runs: %{y}<extra></extra>")
    return _apply_theme(fig, title, height=380)


def cumulative_runs_chart(runs_df: pd.DataFrame, title: str) -> go.Figure:
    fig = px.line(
        runs_df,
        x="over",
        y="cumulative_runs",
        color="inning",
        markers=True,
        color_discrete_sequence=CHART_PALETTE,
        labels={"over": "Over", "cumulative_runs": "Score", "inning": "Inning"},
    )
    fig.update_traces(line=dict(width=2.5))
    return _apply_theme(fig, title, height=380)
