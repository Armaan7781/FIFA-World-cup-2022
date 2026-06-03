import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# --- 1. UI RESET & BLACK GRID ARCHITECTURE ---
st.set_page_config(page_title="World Cup '22 Dashboard", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background: #0A0B0E;
            color: #E2E8F0;
            font-family: 'Inter', sans-serif;
        }
        section[data-testid="stSidebar"] {
            background-color: #050608 !important;
            border-right: 1px solid #1A1D24;
        }
        .stTabs [data-baseweb="tab"] {
            color: #4A5568 !important;
            font-size: 16px;
            font-weight: 700;
            padding: 14px 28px;
        }
        .stTabs [aria-selected="true"] {
            color: #38BDF8 !important;
            border-bottom: 3px solid #38BDF8 !important;
        }
        /* Custom Spatial Canvas Containers */
        .pitch-container {
            background: #111318;
            border: 1px solid #1A1D24;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA HYDRATION ENGINE ---
@st.cache_data
def load_dashboard_matrices():
    team_summary = pd.read_csv('wc_team_summary_clean.csv')
    player_summary = pd.read_csv('wc_player_summary_clean.csv')
    spatial_pos = pd.read_csv('wc_spatial_positions.csv')
    spatial_shots = pd.read_csv('wc_spatial_shots.csv')
    spatial_passes = pd.read_csv('wc_spatial_passes.csv')
    return team_summary, player_summary, spatial_pos, spatial_shots, spatial_passes

t_summary, p_summary, s_pos, s_shots, s_passes = load_dashboard_matrices()

# --- 3. WIDE CHART GENERATION HELPER ---
def render_wide_bar(df, x_col, y_col, title, color_hex):
    # Sort descending based on performance metrics
    sorted_df = df.sort_values(by=y_col, ascending=False).head(10)
    
    fig = px.bar(
        sorted_df, 
        x=x_col, 
        y=y_col, 
        title=title,
        text=y_col # Directly binds the data values to the labels
    )
    fig.update_traces(
        marker_color=color_hex,
        texttemplate='%{text}', 
        textposition='outside', # Places labels safely on the outer edge of the bar
        cliponaxis=False
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450, # Broad, high-impact landscape canvas
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(title="", showgrid=False, type='category'),
        yaxis=dict(title="", showgrid=True, gridcolor="#1A1D24"),
        font=dict(family="Inter, sans-serif", size=13)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. MAP CANVAS LAYOUTS (mplsoccer) ---
def render_live_heatmap(spatial_df, entity_name, filter_col, title):
    filtered = spatial_df[spatial_df[filter_col] == entity_name]
    
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#111318')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#111318', line_color='#2D3748', goal_type='line')
    pitch.draw(ax=ax)
    
    if not filtered.empty:
        # Generate 2D Histogram density fields
        pitch.kdeplot(filtered['x'], filtered['y'], ax=ax, cmap='plasma', fill=True, shade_lowest=False, alpha=0.6, n_levels=10)
    
    plt.title(title, color='#FFFFFF', fontsize=18, pad=10, weight='bold')
    st.pyplot(fig, clear_figure=True)

def render_team_pass_network(team_name):
    # Filters valid completions for pass maps
    t_passes = s_passes[(s_passes['team'] == team_name) & (s_passes['completed'] == True)]
    
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#111318')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#111318', line_color='#2D3748')
    pitch.draw(ax=ax)
    
    if not t_passes.empty:
        # Synthesize tactical positions using dynamic distribution centers
        pitch.scatter(t_passes['x'].mean(), t_passes['y'].mean(), s=400, color='#38BDF8', edgecolors='#FFFFFF', ax=ax, zorder=3)
        pitch.arrows(t_passes['x'].head(30), t_passes['y'].head(30), t_passes['end_x'].head(30), t_passes['end_y'].head(30), color='#38BDF8', alpha=0.3, width=2, headwidth=3, ax=ax)
        
    plt.title(f"{team_name} - Tactical Average Distribution Network", color='#FFFFFF', fontsize=18, pad=10, weight='bold')
    st.pyplot(fig, clear_figure=True)

# --- 5. APPLICATION CONTROL FLOW ---
st.title("⚽ World Cup '22 Strategic Analytics Engine")
view_scope = st.sidebar.radio("CHOOSE CONTROLLER PROFILE", ["Squad Database", "Player Profiles"])

# --- TAB FRAMEWORK CODES ---
if view_scope == "Squad Database":
    t_choice = st.sidebar.selectbox("CHOOSE ACTIVE COUNTRY", sorted(t_summary['team'].unique()))
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["⚔️ ATTACK", "🎯 MIDFIELD", "🛡️ DEFENSE", "🧤 GOALKEEPERS"])
    
    with tab_atk:
        render_wide_bar(t_summary, 'team', 'Goals', 'Tournament Finishing Leaderboard (Total Goals)', '#F43F5E')
        render_wide_bar(t_summary, 'team', 'xG', 'Expected Goals (xG) Volume Ledger', '#FB7185')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        render_live_heatmap(s_shots, t_choice, 'team', f"{t_choice} - Shot Generation Density Zones")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_mid:
        render_wide_bar(t_summary, 'team', 'Succ_Passes', 'Distribution Leaders (Completed Base Passes)', '#6366F1')
        render_wide_bar(t_summary, 'team', 'Prog_Passes', 'Line-Breaking Impact (Progressive Passes Passed)', '#818CF8')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        render_team_pass_network(t_choice)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_def:
        render_wide_bar(t_summary, 'team', 'Pressures', 'Defensive Interruptions (Total System Pressures)', '#10B981')
        render_wide_bar(t_summary, 'team', 'Tackles', 'Ground Duels Contested (Successful Defensive Tackles)', '#34D399')

    with tab_gk:
        render_wide_bar(t_summary, 'team', 'Saves', 'Prevented Goals Profile (Goalkeeper Shot-Stopping Saves)', '#F59E0B')

else:
    # Player Selection Flow
    p_team = st.sidebar.selectbox("SQUAD FILTER", sorted(p_summary['team'].unique()))
    filtered_p = p_summary[p_summary['team'] == p_team]
    p_choice = st.sidebar.selectbox("CHOOSE INDIVIDUAL ATHLETE", sorted(filtered_p['player'].unique()))
    
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["⚔️ ATTACK", "🎯 MIDFIELD", "🛡️ DEFENSE", "🧤 GOALKEEPERS"])
    
    with tab_atk:
        render_wide_bar(p_summary, 'player', 'Goals', 'Golden Boot Standings (Total Goals)', '#F43F5E')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        render_live_heatmap(s_pos, p_choice, 'player', f"{p_choice} - Position Aggregation Matrix Map")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_mid:
        render_wide_bar(p_summary, 'player', 'Prog_Passes', 'Midfield Transition Value (Progressive Passes)', '#6366F1')

    with tab_def:
        render_wide_bar(p_summary, 'player', 'Recoveries', 'Ball Out-of-Possession Regains (Recoveries)', '#10B981')

    with tab_gk:
        render_wide_bar(p_summary, 'player', 'Saves', 'Glove Index Leaderboard (Total Saves)', '#F59E0B')
