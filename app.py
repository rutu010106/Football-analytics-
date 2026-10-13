"""
app.py  —  Football Player Performance Analytics Dashboard
⚽  Built with Python · Streamlit · Pandas · Plotly

⚠️  All data is SYNTHETIC and generated for demonstration purposes.
    It does NOT represent real-world football statistics.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# THEME — dark football pitch UI
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG = "#0d1117"
SURFACE = "#161b22"
BORDER = "#30363d"
GREEN = "#00c853"
GREEN2 = "#1de9b6"
GREEN3 = "#76ff03"
MUTED = "#8b949e"
TEXT = "#e6edf3"
ACCENT_PALETTE = [GREEN, GREEN2, GREEN3, "#b9f6ca", "#69f0ae", "#00e676"]

st.markdown(
    f"""
    <style>
    /* ── global ── */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {DARK_BG};
        color: {TEXT};
    }}
    [data-testid="stSidebar"] {{
        background-color: {SURFACE};
        border-right: 1px solid {BORDER};
    }}
    /* ── tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {SURFACE};
        border-bottom: 2px solid {GREEN};
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {MUTED};
        font-weight: 600;
        font-size: 14px;
        padding: 8px 20px;
        border-radius: 6px 6px 0 0;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {GREEN} !important;
        color: #000 !important;
    }}
    /* ── metric cards ── */
    [data-testid="stMetric"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 16px 20px;
    }}
    [data-testid="stMetricLabel"] {{ color: {MUTED}; font-size: 12px; }}
    [data-testid="stMetricValue"] {{ color: {GREEN}; font-size: 28px; font-weight: 700; }}
    /* ── dataframe ── */
    [data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 8px; }}
    /* ── buttons ── */
    .stDownloadButton button {{
        background-color: {GREEN};
        color: #000;
        font-weight: 700;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
    }}
    .stDownloadButton button:hover {{ background-color: {GREEN2}; }}
    /* ── disclaimer banner ── */
    .disclaimer {{
        background-color: #1a1200;
        border: 1px solid #d4a017;
        border-radius: 6px;
        padding: 8px 14px;
        color: #d4a017;
        font-size: 13px;
        margin-bottom: 16px;
    }}
    /* ── section headers ── */
    h2, h3 {{ color: {GREEN} !important; }}
    /* ── sidebar labels ── */
    [data-testid="stSidebarContent"] label {{ color: {TEXT}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

DISCLAIMER = (
    '<div class="disclaimer">'
    "⚠️  <strong>Synthetic Data Notice:</strong> All player names, teams, and statistics "
    "in this dashboard are <strong>computer-generated</strong> and do <strong>not</strong> "
    "represent real-world football results or actual players."
    "</div>"
)

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, size=12),
    margin=dict(l=10, r=10, t=40, b=10),
)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
REQUIRED_COLUMNS = {
    "player_id", "player_name", "team", "position", "season",
    "age", "appearances", "minutes_played", "goals", "assists",
    "shots", "shots_on_target", "pass_accuracy", "dribbles",
    "tackles", "yellow_cards", "red_cards", "clean_sheets", "rating",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    csv_path = Path("football_players.csv")
    if not csv_path.exists():
        st.error(
            "❌  **football_players.csv not found.**\n\n"
            "Run `python generate_data.py` to create the dataset, "
            "then refresh this page."
        )
        st.stop()
    df = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        st.error(
            f"❌  The CSV is missing required columns: `{', '.join(sorted(missing))}`\n\n"
            "Please re-generate the dataset with `python generate_data.py`."
        )
        st.stop()
    # Ensure correct types
    for col in ["goals", "assists", "shots", "shots_on_target", "appearances",
                "minutes_played", "dribbles", "tackles", "yellow_cards",
                "red_cards", "clean_sheets", "player_id", "age"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["pass_accuracy"] = pd.to_numeric(df["pass_accuracy"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df.dropna(subset=["rating", "pass_accuracy"], inplace=True)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
def build_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown(
        f"<h2 style='color:{GREEN};margin-bottom:4px;'>⚽ Football Analytics</h2>"
        f"<p style='color:{MUTED};font-size:12px;margin-top:0;'>Interactive Dashboard</p>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<p style='color:{MUTED};font-size:12px;'>FILTERS</p>", unsafe_allow_html=True)

    all_seasons = sorted(df["season"].unique().tolist())
    seasons = st.sidebar.multiselect("📅 Season", all_seasons, default=all_seasons)

    all_teams = sorted(df["team"].unique().tolist())
    teams = st.sidebar.multiselect("🏟️ Team", all_teams, default=all_teams)

    pos_order = ["GK", "DEF", "MID", "FWD"]
    all_positions = [p for p in pos_order if p in df["position"].unique()]
    positions = st.sidebar.multiselect("🎽 Position", all_positions, default=all_positions)

    # Player filter — populated after season/team/position filter
    pre_df = df.copy()
    if seasons:
        pre_df = pre_df[pre_df["season"].isin(seasons)]
    if teams:
        pre_df = pre_df[pre_df["team"].isin(teams)]
    if positions:
        pre_df = pre_df[pre_df["position"].isin(positions)]

    all_players = sorted(pre_df["player_name"].unique().tolist())
    players = st.sidebar.multiselect("👤 Player", all_players, default=all_players)

    # Apply all filters
    filtered = df.copy()
    if seasons:
        filtered = filtered[filtered["season"].isin(seasons)]
    if teams:
        filtered = filtered[filtered["team"].isin(teams)]
    if positions:
        filtered = filtered[filtered["position"].isin(positions)]
    if players:
        filtered = filtered[filtered["player_name"].isin(players)]

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"<p style='color:{MUTED};font-size:12px;'>Showing <strong style='color:{GREEN};'>"
        f"{len(filtered)}</strong> records for "
        f"<strong style='color:{GREEN};'>{filtered['player_name'].nunique()}</strong> players</p>",
        unsafe_allow_html=True,
    )
    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_overview(df: pd.DataFrame) -> None:
    st.markdown(DISCLAIMER, unsafe_allow_html=True)
    st.markdown("## 📊 Overview")

    if df.empty:
        st.warning("No data matches the current filters. Please adjust the sidebar filters.")
        return

    # ── KPI Cards ──
    total_players = df["player_id"].nunique()
    total_goals = int(df["goals"].sum())
    total_assists = int(df["assists"].sum())
    total_minutes = int(df["minutes_played"].sum())
    avg_rating = round(float(df["rating"].mean()), 2)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👥 Total Players", f"{total_players:,}")
    c2.metric("⚽ Total Goals", f"{total_goals:,}")
    c3.metric("🎯 Total Assists", f"{total_assists:,}")
    c4.metric("⏱️ Total Minutes", f"{total_minutes:,}")
    c5.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

    st.markdown("---")

    # Aggregate by player (sum across seasons in filtered view)
    player_agg = (
        df.groupby("player_name", as_index=False)
        .agg(goals=("goals", "sum"), assists=("assists", "sum"), rating=("rating", "mean"))
    )
    player_agg["rating"] = player_agg["rating"].round(2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥅 Top 10 Goal Scorers")
        top_goals = player_agg.nlargest(10, "goals").sort_values("goals")
        fig = px.bar(
            top_goals,
            x="goals",
            y="player_name",
            orientation="h",
            text="goals",
            color_discrete_sequence=[GREEN],
        )
        fig.update_traces(textposition="outside", textfont_color=TEXT)
        fig.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Goals",
            yaxis_title="",
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⭐ Top 10 Highest Rated Players")
        top_rated = player_agg.nlargest(10, "rating").sort_values("rating")
        fig2 = px.bar(
            top_rated,
            x="rating",
            y="player_name",
            orientation="h",
            text="rating",
            color_discrete_sequence=[GREEN2],
        )
        fig2.update_traces(textposition="outside", textfont_color=TEXT)
        fig2.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Avg Rating",
            xaxis_range=[5.0, 10.0],
            yaxis_title="",
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Top Assisters row ──
    st.markdown("### 🎯 Top 10 Assist Providers")
    top_assists = player_agg.nlargest(10, "assists").sort_values("assists")
    fig3 = px.bar(
        top_assists,
        x="assists",
        y="player_name",
        orientation="h",
        text="assists",
        color_discrete_sequence=[GREEN3],
    )
    fig3.update_traces(textposition="outside", textfont_color=TEXT)
    fig3.update_layout(
        **CHART_LAYOUT,
        xaxis_title="Assists",
        yaxis_title="",
        showlegend=False,
        height=360,
    )
    st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PLAYER ANALYSIS PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_player_analysis(df: pd.DataFrame) -> None:
    st.markdown(DISCLAIMER, unsafe_allow_html=True)
    st.markdown("## 🔍 Player Analysis")

    if df.empty:
        st.warning("No data matches the current filters. Please adjust the sidebar filters.")
        return

    # Aggregate across seasons for comparison
    player_agg = (
        df.groupby(["player_name", "position", "team"], as_index=False)
        .agg(
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            shots=("shots", "sum"),
            rating=("rating", "mean"),
            appearances=("appearances", "sum"),
            minutes_played=("minutes_played", "sum"),
            pass_accuracy=("pass_accuracy", "mean"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
        )
    )
    player_agg["rating"] = player_agg["rating"].round(2)
    player_agg["pass_accuracy"] = player_agg["pass_accuracy"].round(1)

    # ── Player Comparison ──
    st.markdown("### 🆚 Player Comparison")
    all_names = sorted(player_agg["player_name"].tolist())
    default_selection = all_names[:3] if len(all_names) >= 3 else all_names
    selected = st.multiselect(
        "Select 2–5 players to compare:",
        all_names,
        default=default_selection,
        key="player_compare",
    )

    if len(selected) < 2:
        st.info("ℹ️  Select at least 2 players to see the comparison chart.")
    else:
        compare_df = player_agg[player_agg["player_name"].isin(selected)]
        metrics = ["goals", "assists", "shots", "rating"]
        metric_labels = ["Goals", "Assists", "Shots", "Rating"]

        fig = go.Figure()
        for _, row in compare_df.iterrows():
            fig.add_trace(
                go.Bar(
                    name=row["player_name"],
                    x=metric_labels,
                    y=[row[m] for m in metrics],
                    text=[f"{row[m]:.1f}" if m == "rating" else str(int(row[m])) for m in metrics],
                    textposition="outside",
                )
            )
        fig.update_layout(
            **CHART_LAYOUT,
            barmode="group",
            legend=dict(orientation="h", y=-0.2),
            height=400,
            colorway=ACCENT_PALETTE,
            yaxis_title="Value",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Scatter: Goals vs Assists ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚽ Goals vs Assists")
        fig_ga = px.scatter(
            player_agg,
            x="goals",
            y="assists",
            color="position",
            hover_data={"player_name": True, "team": True, "position": True, "rating": True},
            hover_name="player_name",
            color_discrete_sequence=ACCENT_PALETTE,
            size_max=12,
        )
        fig_ga.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color=DARK_BG)))
        fig_ga.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Goals",
            yaxis_title="Assists",
            legend_title="Position",
            height=420,
        )
        st.plotly_chart(fig_ga, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Shots vs Goals")
        fig_sg = px.scatter(
            player_agg,
            x="shots",
            y="goals",
            color="team",
            hover_data={"player_name": True, "position": True, "rating": True},
            hover_name="player_name",
            color_discrete_sequence=ACCENT_PALETTE,
        )
        fig_sg.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color=DARK_BG)))
        fig_sg.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Shots",
            yaxis_title="Goals",
            legend_title="Team",
            height=420,
        )
        st.plotly_chart(fig_sg, use_container_width=True)

    st.markdown("---")

    # ── Statistics Table ──
    st.markdown("### 📋 Player Statistics Table")

    display_cols = [
        "player_name", "team", "position", "goals", "assists",
        "shots", "rating", "appearances", "minutes_played", "pass_accuracy",
        "yellow_cards", "red_cards",
    ]
    display_df = player_agg[display_cols].copy()
    display_df.columns = [
        "Player", "Team", "Pos", "Goals", "Assists",
        "Shots", "Rating", "Apps", "Minutes", "Pass Acc %",
        "Yellow", "Red",
    ]
    display_df = display_df.sort_values("Goals", ascending=False).reset_index(drop=True)

    st.dataframe(display_df, use_container_width=True, height=420)

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="football_analytics_export.csv",
        mime="text/csv",
    )


# ─────────────────────────────────────────────────────────────────────────────
# TEAM ANALYSIS PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_team_analysis(df: pd.DataFrame) -> None:
    st.markdown(DISCLAIMER, unsafe_allow_html=True)
    st.markdown("## 🏟️ Team Analysis")

    if df.empty:
        st.warning("No data matches the current filters. Please adjust the sidebar filters.")
        return

    # Team-level aggregations
    team_agg = (
        df.groupby("team", as_index=False)
        .agg(
            players=("player_id", "nunique"),
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            avg_rating=("rating", "mean"),
        )
    )
    team_agg["avg_rating"] = team_agg["avg_rating"].round(2)
    team_agg = team_agg.sort_values("total_goals", ascending=False)

    # ── Goals & Assists per Team ──
    st.markdown("### ⚽ Goals & Assists per Team")
    if team_agg["team"].nunique() < 2:
        st.info("Select more than one team in the sidebar to see team comparisons.")
    else:
        fig_team = px.bar(
            team_agg.melt(id_vars="team", value_vars=["total_goals", "total_assists"],
                          var_name="Metric", value_name="Value"),
            x="team",
            y="Value",
            color="Metric",
            barmode="group",
            text="Value",
            color_discrete_map={"total_goals": GREEN, "total_assists": GREEN2},
            labels={"team": "Team", "Value": "Count", "Metric": "Metric"},
        )
        fig_team.update_traces(textposition="outside")
        fig_team.update_layout(
            **CHART_LAYOUT,
            legend_title="Metric",
            height=400,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_team, use_container_width=True)

    st.markdown("---")

    # ── Position Breakdown per Team ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎽 Squad Composition by Team")
        pos_team = (
            df.groupby(["team", "position"])["player_id"]
            .nunique()
            .reset_index(name="players")
        )
        fig_pos = px.bar(
            pos_team,
            x="team",
            y="players",
            color="position",
            barmode="stack",
            color_discrete_sequence=ACCENT_PALETTE,
            labels={"team": "Team", "players": "Players", "position": "Position"},
        )
        fig_pos.update_layout(
            **CHART_LAYOUT,
            height=380,
            xaxis_tickangle=-30,
            legend_title="Position",
        )
        st.plotly_chart(fig_pos, use_container_width=True)

    with col2:
        st.markdown("### ⭐ Average Rating per Team")
        fig_rating = px.bar(
            team_agg.sort_values("avg_rating", ascending=True),
            x="avg_rating",
            y="team",
            orientation="h",
            text="avg_rating",
            color_discrete_sequence=[GREEN3],
        )
        fig_rating.update_traces(textposition="outside", textfont_color=TEXT)
        fig_rating.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Avg Rating",
            xaxis_range=[5.0, 9.0],
            yaxis_title="",
            height=380,
        )
        st.plotly_chart(fig_rating, use_container_width=True)

    st.markdown("---")

    # ── Team Summary Table ──
    st.markdown("### 📋 Team Summary")
    summary = team_agg.copy()
    summary.columns = ["Team", "Players", "Total Goals", "Total Assists", "Avg Rating"]
    st.dataframe(summary.reset_index(drop=True), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# POSITION ANALYSIS PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_position_analysis(df: pd.DataFrame) -> None:
    st.markdown(DISCLAIMER, unsafe_allow_html=True)
    st.markdown("## 🎽 Position Analysis")

    if df.empty:
        st.warning("No data matches the current filters. Please adjust the sidebar filters.")
        return

    # Aggregation per position
    pos_agg = (
        df.groupby("position", as_index=False)
        .agg(
            players=("player_id", "nunique"),
            avg_goals=("goals", "mean"),
            avg_assists=("assists", "mean"),
            avg_rating=("rating", "mean"),
            avg_clean_sheets=("clean_sheets", "mean"),
        )
    )
    pos_agg = pos_agg.round(2)

    # Enforce display order
    pos_order = ["GK", "DEF", "MID", "FWD"]
    pos_agg["_order"] = pos_agg["position"].map({p: i for i, p in enumerate(pos_order)})
    pos_agg = pos_agg.sort_values("_order").drop(columns="_order")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥧 Squad Composition by Position")
        fig_pie = px.pie(
            pos_agg,
            names="position",
            values="players",
            hole=0.4,
            color_discrete_sequence=ACCENT_PALETTE,
        )
        fig_pie.update_traces(
            textinfo="label+percent",
            textfont_size=13,
            pull=[0.03] * len(pos_agg),
        )
        fig_pie.update_layout(**CHART_LAYOUT, height=380, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### ⭐ Rating Distribution by Position")
        fig_box = px.box(
            df,
            x="position",
            y="rating",
            color="position",
            color_discrete_sequence=ACCENT_PALETTE,
            category_orders={"position": pos_order},
            points="outliers",
        )
        fig_box.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Position",
            yaxis_title="Rating",
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### ⚽ Avg Goals by Position")
        fig_goals = px.bar(
            pos_agg,
            x="position",
            y="avg_goals",
            text="avg_goals",
            color="position",
            color_discrete_sequence=ACCENT_PALETTE,
        )
        fig_goals.update_traces(textposition="outside", textfont_color=TEXT)
        fig_goals.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Position",
            yaxis_title="Avg Goals",
            showlegend=False,
            height=350,
        )
        st.plotly_chart(fig_goals, use_container_width=True)

    with col4:
        st.markdown("### 🎯 Avg Assists by Position")
        fig_assists = px.bar(
            pos_agg,
            x="position",
            y="avg_assists",
            text="avg_assists",
            color="position",
            color_discrete_sequence=ACCENT_PALETTE,
        )
        fig_assists.update_traces(textposition="outside", textfont_color=TEXT)
        fig_assists.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Position",
            yaxis_title="Avg Assists",
            showlegend=False,
            height=350,
        )
        st.plotly_chart(fig_assists, use_container_width=True)

    # ── Clean Sheets (GK & DEF only) ──
    st.markdown("---")
    st.markdown("### 🧤 Avg Clean Sheets — Goalkeepers & Defenders")
    defensive = pos_agg[pos_agg["position"].isin(["GK", "DEF"])].copy()
    if defensive.empty:
        st.info("No Goalkeepers or Defenders in the current filter selection.")
    else:
        fig_cs = px.bar(
            defensive,
            x="position",
            y="avg_clean_sheets",
            text="avg_clean_sheets",
            color="position",
            color_discrete_sequence=[GREEN, GREEN2],
        )
        fig_cs.update_traces(textposition="outside", textfont_color=TEXT)
        fig_cs.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Position",
            yaxis_title="Avg Clean Sheets",
            showlegend=False,
            height=320,
        )
        st.plotly_chart(fig_cs, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    df = load_data()
    filtered_df = build_sidebar(df)

    if filtered_df.empty:
        st.warning(
            "⚠️  No data matches your current filter selection. "
            "Please broaden the filters in the sidebar."
        )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Overview", "🔍 Player Analysis", "🏟️ Team Analysis", "🎽 Position Analysis"]
    )

    with tab1:
        render_overview(filtered_df)

    with tab2:
        render_player_analysis(filtered_df)

    with tab3:
        render_team_analysis(filtered_df)

    with tab4:
        render_position_analysis(filtered_df)


if __name__ == "__main__":
    main()
