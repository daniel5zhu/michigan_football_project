import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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
    (df["homeTeam"] == team) | (df["awayTeam"] == team)
].copy()

team_games["team_score"] = np.where(
    team_games["homeTeam"] == team,
    team_games["homePoints"],
    team_games["awayPoints"],
)
team_games["opp_score"] = np.where(
    team_games["homeTeam"] == team,
    team_games["awayPoints"],
    team_games["homePoints"],
)
team_games["opponent"] = np.where(
    team_games["homeTeam"] == team,
    team_games["awayTeam"],
    team_games["homeTeam"],
)
team_games["margin"] = team_games["team_score"] - team_games["opp_score"]

team_games["location"] = np.where(
    team_games["homeTeam"] == team, "Home", "Away"
)

team_games["result"] = np.where(team_games["margin"] > 0, "Win", "Loss")

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

