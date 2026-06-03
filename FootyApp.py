import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Custom UI Architecture Configuration
st.set_page_config(page_title="World Cup Elite Analytics", layout="wide")

# Custom CSS Injection for a Premium World Cup Dark Aesthetic (Deep Maroon & Gold Accents)
st.markdown("""
    <style>
        .stApp {
            background-color: #0F0508;
            color: #F4EAD4;
        }
        h1, h2, h3 {
            color: #D4AF37 !important;
            font-family: 'Georgia', serif;
        }
        .stTabs [data-baseweb="tab"] {
            color: #A3937B !important;
            font-size: 16px;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            color: #D4AF37 !important;
            border-bottom-color: #8A1538 !important;
        }
        div[data-testid="stMetricValue"] {
            color: #D4AF37 !important;
            font-size: 32px;
        }
        div[data-testid="stMetricLabel"] {
            color: #A3937B !important;
        }
    </style>
""",unsafe_allow_html=True)

st.title("🏆 FIFA World Cup 2022 Performance Command Center")
st.markdown("---")

# 2. Optimized Local Data Caching
@st.cache_data
def load_data():
    teams = pd.read_csv('wc_team_advanced.csv')
    players = pd.read_csv('wc_player_advanced.csv')
    return teams, players

team_df, player_df = load_data()

# 3. Dynamic Sidebar Navigation Panel
st.sidebar.markdown("<h2 style='color:#D4AF37;'>Control Room</h2>", unsafe_allow_html=True)
view_type = st.sidebar.radio("Analytical Entity", ["Team Matrix", "Player Matrix"])

# Helper function to inject dark themed plotly layouts
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#F4EAD4",
        title_font_color="#D4AF37"
    )
    fig.update_traces(marker_color='#8A1538', marker_line_color='#D4AF37', marker_line_width=1)
    return fig

# --- VIEW 1: TEAM PERFORMANCE MATRIX ---
if view_type == "Team Matrix":
    
    # Executive Summary Metric Ribbon
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Highest Scoring Team", "France (16)")
    m2.metric("Highest Total xG", "Argentina (15.5)")
    m3.metric("Most Complete Passes", "Argentina (3,989)")
    m4.metric("Most Safe Interventions", "Croatia (594)")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tab Segmentation
    tab_att, tab_pass, tab_def, tab_gk = st.tabs(["🎯 Attacking", "👟 Passing Analysis", "🛡️ Defensive Unit", "🧤 Goalkeeping Overview"])
    
    with tab_att:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(team_df.sort_values(by="Goals", ascending=False).head(10), x="team", y="Goals", title="Top 10 Most Lethal Teams (Goals)")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with c2:
            fig = px.scatter(team_df, x="xG", y="Goals", text="team", hover_name="team", title="Expected Goals (xG) vs Actual Conversion")
            fig.update_traces(textposition='top center', marker=dict(size=12, color='#D4AF37'))
            st.plotly_chart(style_chart(fig), use_container_width=True)
            
    with tab_pass:
        c1, c2 = st.columns(2)
        with c1:
            team_df['Pass_Accuracy'] = (team_df['Completed_Passes'] / team_df['Total_Passes'] * 100).round(1)
            fig = px.bar(team_df.sort_values(by="Pass_Accuracy", ascending=False).head(10), x="team", y="Pass_Accuracy", title="Passing Efficiency Rating (%)")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with c2:
            fig = px.bar(team_df.sort_values(by="Key_Passes", ascending=False).head(10), x="team", y="Key_Passes", title="Chances Created (Key Passes)")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            
    with tab_def:
        fig = px.bar(team_df.sort_values(by="Defensive_Actions", ascending=False), x="team", y="Defensive_Actions", title="Total Defensive Volume (Tackles, Blocks, Interceptions, Recoveries)")
        st.plotly_chart(style_chart(fig), use_container_width=True)
        
    with tab_gk:
        fig = px.bar(team_df.sort_values(by="Saves", ascending=False), x="team", y="Saves", title="Total Goalkeeper Saves Across Tournament")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader("Comprehensive Team Data Ledger")
    st.dataframe(team_df, use_container_width=True)

# --- VIEW 2: PLAYER PERFORMANCE MATRIX ---
else:
    # Team Filter for Player Deep Dives
    available_teams = ["All Teams"] + sorted(list(player_df['team'].unique()))
    selected_team = st.sidebar.selectbox("Filter Player Dataset by Squad Location", available_teams)
    
    active_players = player_df if selected_team == "All Teams" else player_df[player_df['team'] == selected_team]
    
    tab_att, tab_pass, tab_def, tab_gk = st.tabs(["🎯 Attacking Benchmarks", "👟 Passing Orchestration", "🛡️ Defensive Actions", "🧤 Goalkeeping Glove Gold"])
    
    with tab_att:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(active_players.sort_values(by="Goals", ascending=False).head(15), x="player", y="Goals", color="team", title="Top Finishing Records")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with c2:
            fig = px.scatter(active_players[active_players['Goals'] > 0], x="xG", y="Goals", hover_name="player", color="team", title="Individual Finishing Efficiency Profile")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            
    with tab_pass:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(active_players.sort_values(by="Completed_Passes", ascending=False).head(15), x="player", y="Completed_Passes", title="Total Completed Distribution Profile")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with c2:
            fig = px.bar(active_players.sort_values(by="Key_Passes", ascending=False).head(15), x="player", y="Key_Passes", title="Chances Carved Open (Key Passes)")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            
    with tab_def:
        fig = px.bar(active_players.sort_values(by="Defensive_Actions", ascending=False).head(15), x="player", y="Defensive_Actions", color="team", title="Most Active Ground Defending Output")
        st.plotly_chart(style_chart(fig), use_container_width=True)
        
    with tab_gk:
        gk_filtered = active_players[active_players['Saves'] > 0]
        if not gk_filtered.empty:
            fig = px.bar(gk_filtered.sort_values(by="Saves", ascending=False), x="player", y="Saves", color="team", title="Shot-Stopping Output Leaders")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("No goalkeeping actions recorded inside the active context query filters.")

    st.subheader("Filtered Player Structural Data Grid")
    st.dataframe(active_players.sort_values(by="Goals", ascending=False), use_container_width=True)
