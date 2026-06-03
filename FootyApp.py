# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="WC 2022 Analytics", layout="wide")
st.title("🏆 FIFA World Cup 2022 Analysis")

@st.cache_data
def load_data():
    teams = pd.read_csv('wc_team_stats.csv')
    players = pd.read_csv('wc_player_stats.csv')
    return teams, players

team_stats, player_stats = load_data()

st.sidebar.header("Navigation")
view = st.sidebar.radio("Select View", ["Team Performance", "Player Performance"])

if view == "Team Performance":
    st.header("Team Performance Matrix")
    metric = st.selectbox("Select Metric to Visualize", ["Goals", "xG", "Successful_Passes"])
    
    top_teams = team_stats.sort_values(by=metric, ascending=False).head(15)
    fig = px.bar(top_teams, x='team', y=metric, color='team', title=f"Top 15 Teams by {metric}")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Raw Data")
    st.dataframe(team_stats.sort_values(by=metric, ascending=False), use_container_width=True)

else:
    st.header("Player Performance Matrix")
    metric = st.selectbox("Select Metric to Visualize", ["Goals", "xG", "Successful_Passes", "Total_Passes"])
    
    team_filter = st.selectbox("Filter by Team (Optional)", ["All"] + list(player_stats['team'].unique()))
    filtered_players = player_stats if team_filter == "All" else player_stats[player_stats['team'] == team_filter]
    
    top_players = filtered_players.sort_values(by=metric, ascending=False).head(15)
    fig = px.bar(top_players, x='player', y=metric, color='team', title=f"Top 15 Players by {metric}")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Raw Data")
    st.dataframe(filtered_players.sort_values(by=metric, ascending=False), use_container_width=True)
