import streamlit as st
import pandas as pd
import plotly as px

st.title("Daniel's Michigan Football Analytics")

df = pd.read_csv("data/michigan_games.csv")

# Get all teams
teams = sorted(
    pd.concat([df["homeTeam"], df["awayTeam"]]).unique()
)

team = st.selectbox(
    "Select Team",
    teams,
    index=teams.index("Michigan")   # default selection
)

st.write(f"Selected Team: {team}")

team_games = df[
    (df["homeTeam"] == team) |
    (df["awayTeam"] == team)
]

team_games = df[
    (df["homeTeam"] == selected_team) | (df["awayTeam"] == selected_team)
].copy()

team_games["location"] = np.where(
    team_games["homeTeam"] == selected_team, "Home", "Away"
)

st.dataframe(team_games)

st.subheader("Home vs. Away Breakdown")
loc_summary = (
    team_games.groupby(["location", "result"]).size().reset_index(name="count")
    )
fig_loc = px.bar(
    loc_summary,
    x="location",
    y="count",            
    color="result",
    barmode="group",
    color_discrete_map={"Win": "#2ecc71", "Loss": "#e74c3c"},
    title="Performance by Location",
    )
st.plotly_chart(fig_loc, use_container_width=True)

