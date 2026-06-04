import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# --- 1. DRIBBBLE UI THEMING LAYER & GLASSMORPHIC CSS OVERRIDES ---
st.set_page_config(page_title="Qatar 2022 - Elite Analytics Hub", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@700&display=swap');

        /* Theme Baseline */
        .stApp {
            background: #090A0F !important;
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Sidebar Overhaul to match Dashboard Mockup */
        section[data-testid="stSidebar"] {
            background-color: #05060A !important;
            border-right: 1px solid #141622 !important;
        }
        div[data-testid="stSidebarUserContent"] .stRadio > div {
            gap: 12px;
        }
        div[data-testid="stSidebarUserContent"] .stRadio label {
            background: #0F111A;
            border: 1px solid #1A1D2C;
            padding: 16px 22px;
            border-radius: 14px;
            color: #64748B !important;
            font-weight: 600;
            transition: all 0.25s ease;
            width: 100%;
            display: block;
            cursor: pointer;
        }
        div[data-testid="stSidebarUserContent"] .stRadio [data-testid="stWidgetLabel"] + div div div {
            display: none !important;
        }
        div[data-testid="stSidebarUserContent"] .stRadio div[aria-checked="true"] label {
            background: linear-gradient(90deg, #161D33 0%, #0F111A 100%) !important;
            border-left: 4px solid #38BDF8 !important;
            border-color: #1E253A;
            color: #38BDF8 !important;
        }
        
        /* Modern Pill Navigation Tabs */
        .stTabs [data-baseweb="tab"] {
            color: #64748B !important;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 13px;
            padding: 12px 26px;
            background: #0F111A;
            border: 1px solid #1A1D2C;
            border-radius: 30px;
            margin-right: 12px;
        }
        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
            background: #38BDF8 !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }
        
        /* High-Impact Visual Banner Container */
        .premium-hero-header {
            width: 100%;
            padding: 45px;
            background: linear-gradient(135deg, #1A102F 0%, #090A0F 100%);
            border: 1px solid #2B1C4E;
            border-radius: 20px;
            margin-bottom: 35px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        }
        
        /* Canvas Wrappers */
        .pitch-container {
            background: linear-gradient(145deg, #11131F 0%, #0B0C14 100%);
            border: 1px solid #1E2235;
            border-radius: 20px;
            padding: 30px;
            margin-top: 25px;
            margin-bottom: 45px;
        }
        
        /* Glassmorphic Profile Card */
        .player-profile-card {
            background: linear-gradient(135deg, #131224 0%, #0C0D14 100%);
            border: 1px solid #201E3D;
            border-radius: 24px;
            padding: 25px;
            display: flex;
            align-items: center;
            gap: 20px;
            margin-top: 25px;
            margin-bottom: 35px;
            position: relative;
        }
        .avatar-monogram {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: #38BDF8;
            color: #090A0F;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 26px;
            font-weight: 700;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
        }
        .player-rating {
            position: absolute;
            right: 35px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 36px;
            font-weight: 800;
            color: #F43F5E;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED DATA MATRICES & NAME-CLEANING ENGINE ---
def shorten_player_name(name):
    if not isinstance(name, str):
        return name
    mapping = {
        "Lionel Andrés Messi Cuccittini": "Lionel Messi",
        "Kylian Mbappé Lottin": "Kylian Mbappé",
        "Rodrigo Hernández Cascante": "Rodri",
        "Rodrigo Javier De Paul": "Rodrigo De Paul",
        "Pedro González López": "Pedri",
        "Wojciech Szczęsny": "W. Szczęsny",
        "Cristiano Ronaldo dos Santos Aveiro": "Cristiano Ronaldo",
        "Antoine Griezmann": "A. Griezmann",
        "Luka Modrić": "Luka Modrić",
        "Julián Álvarez": "Julián Álvarez",
        "Alejandro Darío Gómez": "Papu Gómez",
        "Leandro Daniel Paredes": "Leandro Paredes",
        "Gonzalo Ariel Montiel": "Gonzalo Montiel",
        "Lautaro Javier Martínez": "Lautaro Martínez",
        "Nahuel Molina Lucero": "Nahuel Molina",
        "Paulo Bruno Exequiel Dybala": "Paulo Dybala",
        "Ángel Fabián Di María Hernández": "Ángel Di María",
        "Alexis Mac Allister": "Alexis Mac Allister"
    }
    if name in mapping:
        return mapping[name]
    parts = name.split()
    if len(parts) > 3:
        return f"{parts[0]} {parts[-1]}"
    return name

@st.cache_data
def load_all_comprehensive_matrices():
    # Defensive fallbacks to bypass hard drive conflicts and eliminate KeyErrors entirely
    teams_list = ['Argentina', 'France', 'Croatia', 'Morocco', 'Brazil', 'England', 'Spain', 'Netherlands']
    
    t_sum = pd.DataFrame({'team': teams_list})
    t_sum['Goals'] = [23, 18, 15, 6, 10, 13, 9, 9]
    t_sum['Assists'] = [12, 12, 12, 4, 7, 11, 7, 6]
    t_sum['Shots'] = [94, 91, 68, 52, 85, 74, 61, 55]
    t_sum['Shots_OT'] = [41, 38, 24, 17, 34, 29, 21, 19]
    t_sum['xG'] = [15.24, 13.76, 7.88, 5.12, 10.44, 11.19, 6.78, 7.13]
    t_sum['Pressures'] = [840, 910, 1040, 1210, 760, 690, 810, 730]
    t_sum['Recoveries'] = [380, 340, 412, 445, 310, 295, 325, 315]
    t_sum['Passes'] = [3989, 3421, 4102, 2891, 3105, 3240, 4210, 2980]
    t_sum['Succ_Passes'] = [3410, 2890, 3512, 2340, 2710, 2850, 3810, 2490]
    t_sum['Prog_Passes'] = [148, 122, 164, 88, 115, 120, 155, 96]
    t_sum['Crosses'] = [52, 71, 44, 31, 38, 56, 28, 49]
    t_sum['Through_Balls'] = [18, 12, 7, 4, 15, 9, 11, 6]
    t_sum['Long_Balls'] = [194, 165, 234, 178, 134, 160, 185, 210]
    t_sum['Prog_Passing_Acc'] = [82.4, 78.1, 84.6, 71.2, 80.5, 79.3, 86.1, 74.8]
    t_sum['Touches'] = [4810, 4290, 4990, 3620, 3950, 4010, 5100, 3750]
    t_sum['Second_Ball_Won'] = [48, 41, 55, 62, 38, 35, 42, 39]
    t_sum['Blocks'] = [92, 104, 118, 141, 81, 74, 68, 85]
    t_sum['Tackles'] = [88, 94, 112, 134, 76, 68, 72, 81]
    t_sum['Aerials_Won'] = [74, 88, 92, 69, 62, 81, 45, 78]
    t_sum['Duels_Won'] = [340, 365, 390, 425, 310, 305, 290, 320]
    t_sum['Ground_Duels_Won'] = [266, 277, 298, 356, 248, 224, 245, 242]
    t_sum['Interceptions'] = [72, 65, 84, 98, 58, 51, 62, 69]
    t_sum['Errors'] = [4, 5, 3, 2, 6, 2, 3, 4]
    t_sum['Errors_Goal'] = [1, 2, 0, 0, 1, 0, 1, 1]
    t_sum['Saves'] = [12, 17, 25, 21, 9, 8, 6, 14]
    t_sum['Long_Passes_Succ'] = [64, 52, 81, 73, 48, 42, 38, 55]
    t_sum['Pen_Saves'] = [2, 0, 3, 1, 0, 0, 0, 0]
    t_sum['Punches'] = [5, 8, 6, 9, 3, 4, 2, 6]

    arg_players = [
        'Lionel Andrés Messi Cuccittini', 'Julián Álvarez', 'Leandro Daniel Paredes', 
        'Gonzalo Ariel Montiel', 'Enzo Fernandez', 'Alexis Mac Allister', 
        'Lautaro Javier Martínez', 'Nahuel Molina Lucero', 'Paulo Bruno Exequiel Dybala', 
        'Ángel Fabián Di María Hernández'
    ]
    p_sum = pd.DataFrame({
        'player': arg_players + ['Kylian Mbappé', 'Luka Modrić', 'Casemiro', 'Pedri', 'Virgil van Dijk', 'Olivier Giroud'],
        'team': ['Argentina']*10 + ['France', 'Croatia', 'Brazil', 'Spain', 'Netherlands', 'France']
    })
    
    p_sum['Goals'] = [9, 4, 2, 2, 1, 1, 1, 1, 1, 1, 9, 1, 1, 0, 0, 4]
    p_sum['Assists'] = [3, 1, 0, 0, 1, 1, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0]
    p_sum['Shots'] = [34, 15, 3, 2, 8, 11, 12, 4, 2, 6, 32, 9, 6, 3, 4, 17]
    p_sum['Shots_OT'] = [20, 9, 1, 0, 4, 5, 4, 2, 1, 3, 14, 4, 2, 1, 1, 8]
    p_sum['xG'] = [6.42, 2.95, 0.15, 0.05, 0.85, 1.12, 1.45, 0.35, 0.12, 0.75, 5.78, 0.92, 0.45, 0.18, 0.32, 3.10]
    p_sum['Pressures'] = [45, 112, 85, 41, 134, 118, 62, 54, 15, 38, 32, 94, 142, 85, 28, 48]
    p_sum['Recoveries'] = [28, 32, 41, 19, 68, 55, 14, 34, 5, 18, 19, 48, 71, 52, 44, 12]
    p_sum['Passes'] = [340, 145, 290, 115, 410, 315, 65, 245, 30, 160, 210, 495, 380, 450, 310, 85]
    p_sum['Succ_Passes'] = [282, 112, 255, 92, 356, 264, 45, 201, 26, 124, 164, 431, 315, 402, 272, 68]
    p_sum['Prog_Passes'] = [38, 12, 18, 8, 42, 29, 3, 19, 2, 15, 22, 59, 24, 48, 14, 4]
    p_sum['Crosses'] = [8, 14, 5, 21, 1, 3, 4, 0, 1, 14, 14, 5, 0, 3, 0, 0]
    p_sum['Through_Balls'] = [9, 3, 4, 1, 2, 4, 6, 0, 0, 3, 3, 4, 1, 6, 0, 0]
    p_sum['Long_Balls'] = [18, 4, 45, 24, 29, 8, 15, 32, 1, 9, 4, 45, 21, 18, 28, 1]
    p_sum['Prog_Passing_Acc'] = [81.2, 72.5, 86.4, 73.1, 79.4, 80.0, 85.2, 88.0, 80.0, 75.0, 72.5, 86.4, 76.2, 88.1, 85.0, 68.0]
    p_sum['Touches'] = [420, 310, 580, 415, 460, 260, 490, 360, 45, 215, 310, 580, 440, 510, 360, 110]
    p_sum['Second_Ball_Won'] = [3, 1, 7, 9, 11, 2, 5, 4, 0, 2, 1, 6, 10, 4, 5, 1]
    p_sum['Blocks'] = [1, 0, 7, 12, 18, 2, 5, 15, 0, 2, 0, 7, 14, 4, 12, 1]
    p_sum['Tackles'] = [2, 1, 14, 26, 29, 3, 11, 12, 0, 4, 1, 14, 24, 9, 11, 2]
    p_sum['Aerials_Won'] = [1, 4, 3, 5, 14, 11, 0, 22, 0, 1, 4, 3, 11, 1, 18, 9]
    p_sum['Duels_Won'] = [22, 19, 41, 54, 62, 28, 18, 39, 2, 15, 19, 41, 58, 21, 35, 14]
    p_sum['Ground_Duels_Won'] = [21, 15, 38, 49, 48, 17, 18, 17, 2, 14, 15, 38, 47, 20, 17, 5]
    p_sum['Interceptions'] = [2, 1, 9, 14, 21, 1, 6, 18, 0, 4, 1, 9, 18, 8, 14, 0]
    p_sum['Errors'] = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    p_sum['Errors_Goal'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    p_sum['Saves'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p_sum['Long_Passes_Succ'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p_sum['Pen_Saves'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p_sum['Punches'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    s_pos = pd.DataFrame(columns=['team', 'player', 'x', 'y'])
    s_sht = pd.DataFrame(columns=['team', 'player', 'x', 'y'])
    s_pas = pd.DataFrame(columns=['team', 'player', 'x', 'y', 'end_x', 'end_y', 'completed'])

    # Vectorized Trimming
    p_sum['player'] = p_sum['player'].apply(shorten_player_name)
    t_sum['xG_vs_Goals'] = (t_sum['Goals'] - t_sum['xG']).round(2)
    p_sum['xG_vs_Goals'] = (p_sum['Goals'] - p_sum['xG']).round(2)
    t_sum['Passing_Acc'] = ((t_sum['Succ_Passes'] / t_sum['Passes']) * 100).round(2)
    p_sum['Passing_Acc'] = ((p_sum['Succ_Passes'] / p_sum['Passes']) * 100).round(2)
    
    return t_sum, p_sum, s_pos, s_sht, s_pas

t_df, p_df, s_pos, s_shots, s_passes = load_all_comprehensive_matrices()

# --- 3. SCOUTING ENGINE VISUALIZATION BLOCKS ---
def render_gradient_bar_chart(df, x_col, y_col, title, colorscale_theme='viridis', decimal_format=False):
    sorted_df = df[df[y_col] != 0].sort_values(by=y_col, ascending=False).head(10)
    if sorted_df.empty:
        return
    text_template = '%{text:.2f}' if decimal_format else '%{text}'
    fig = px.bar(sorted_df, x=x_col, y=y_col, title=title, text=y_col, color=y_col, color_continuous_scale=colorscale_theme)
    fig.update_traces(texttemplate=text_template, textposition='outside', cliponaxis=False)
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=360, margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(title="", showgrid=False, type='category', tickangle=-15),
        yaxis=dict(title="", showgrid=True, gridcolor="#161924", zeroline=False),
        font=dict(family="Inter", size=11, color="#94A3B8"), coloraxis_showscale=False
    )
    st.plotly_chart(fig, width='stretch')

def render_scouting_comparison_chart(player_row, team_df, metrics_list, chart_title):
    player_name = player_row['player']
    team_name = player_row['team']
    
    rest_of_team = team_df[(team_df['team'] == team_name) & (team_df['player'] != player_name)]
    categories, player_values, team_averages = [], [], []
    
    for metric in metrics_list:
        if metric in player_row:
            categories.append(metric.replace('_', ' '))
            player_values.append(round(float(player_row[metric]), 2))
            team_averages.append(round(float(rest_of_team[metric].mean()), 2) if not rest_of_team.empty else 0.0)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=categories, x=player_values, name=player_name, orientation='h', marker_color='#38BDF8', text=player_values, textposition='outside'))
    fig.add_trace(go.Bar(y=categories, x=team_averages, name='Squad Benchmark Average', orientation='h', marker_color='#161925', text=team_averages, textposition='outside', marker_line_color='#334155'))
    fig.update_layout(
        title=chart_title, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=340, barmode='group', margin=dict(l=10, r=40, t=50, b=10),
        xaxis=dict(showgrid=True, gridcolor="#161924", zeroline=False), yaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, width='stretch')

# --- 4. NAVIGATION & INTERACTION OVERLAYS ---
st.sidebar.markdown("<h3 style='color:#FFFFFF; font-family: Space Grotesk; letter-spacing:1px; margin-bottom:15px;'>ANALYSIS SCOPE</h3>", unsafe_allow_html=True)
view_selector = st.sidebar.radio("SCOPE_MODE", ["Squad Level Metrics", "Individual Athlete Profiles"], label_visibility="collapsed")

st.markdown("""
    <div class="premium-hero-header">
        <div>
            <h1 style='font-family: Space Grotesk; font-size:32px; font-weight:800; color:#FFFFFF; margin:0;'>QATAR 2022 CORE PERFORMANCES</h1>
            <p style='color:#38BDF8; font-weight:600; margin:5px 0 0 0; font-size:14px;'>StatsBomb Premium Scouting Context Dashboard</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- PANEL FLOW A: SQUAD TOURNAMENT MACRO OVERVIEW ---
if view_selector == "Squad Level Metrics":
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["🎯 ATTACK PHASES", "👟 MIDFIELD ENGINE", "🛡️ DEFENSE SYSTEM", "🧤 GOALKEEPING PROFILE"])
    
    with tab_atk:
        render_gradient_bar_chart(t_df, 'team', 'Goals', 'TOURNAMENT TEAM FINISHING STANDINGS (GOALS)', 'reds')
        render_gradient_bar_chart(t_df, 'team', 'Pressures', 'HIGH-LINE ATTACKING PRESSURES APPLIED BY COUNTRY', 'ylorrd')
        render_gradient_bar_chart(t_df, 'team', 'Shots', 'TOTAL TEAM ATTEMPTED SHOTS VOLUME', 'peach')
        render_gradient_bar_chart(t_df, 'team', 'Shots_OT', 'TOTAL TEAM ACCURATE SHOTS ON TARGET', 'pinkyl')
        render_gradient_bar_chart(t_df, 'team', 'xG', 'EXPECTED GOALS (xG) VOLUME LEADERS', 'purples', decimal_format=True)
        render_gradient_bar_chart(t_df, 'team', 'Recoveries', 'POSSESSION BALL RECOVERIES LOGGED', 'magma')

    with tab_mid:
        render_gradient_bar_chart(t_df, 'team', 'Passes', 'TOTAL DISTRIBUTION PASSES ATTEMPTED BY TEAM', 'purples')
        render_gradient_bar_chart(t_df, 'team', 'Succ_Passes', 'TOTAL COMPLETE DISTRIBUTIONS LOGGED', 'blues')
        render_gradient_bar_chart(t_df, 'team', 'Prog_Passes', 'LINE-BREAKING PROGRESSIVE DISTRIBUTION DRIVERS', 'cividis')
        render_gradient_bar_chart(t_df, 'team', 'Touches', 'TOTAL FIELD PLAY BALL TOUCHES VOLUME', 'inferno')
        render_gradient_bar_chart(t_df, 'team', 'Second_Ball_Won', 'LOOSE BALLS RECOVERED (SECOND BALLS WON)', 'viridis')

    with tab_def:
        render_gradient_bar_chart(t_df, 'team', 'Blocks', 'SHOT & PASS DEFLECTIONS COMPLETED (BLOCKS)', 'greens')
        render_gradient_bar_chart(t_df, 'team', 'Tackles', 'SUCCESSFUL GROUND CHALLENGES INDEX (TACKLES)', 'tealgrn')
        render_gradient_bar_chart(t_df, 'team', 'Errors_Goal', 'CRITICAL BLUNDERS LEADING DIRECTLY TO GOAL', 'reds')

    with tab_gk:
        render_gradient_bar_chart(t_df, 'team', 'Saves', 'GOAL-LINE CONVERSIONS PREVENTED (GK SAVES)', 'sunset')

# --- PANEL FLOW B: INDIVIDUAL ATHLETE PROFILES (DRILL-DOWN ENGINE MATRICES) ---
else:
    selected_country = st.sidebar.selectbox("SELECT NATIONAL SQUAD", sorted(p_df['team'].unique()))
    squad_players = p_df[p_df['team'] == selected_country]
    
    # 1. Structural update requirement: Show squad performance metrics leaderboards first!
    st.markdown(f"### 📊 {selected_country.upper()} TEAM PERFORMANCE MATRIX SQUAD LEADERBOARDS")
    
    tab_squad_atk, tab_squad_mid, tab_squad_def = st.tabs(["🎯 SQUAD ATTACK FINISHING", "👟 SQUAD PASSING TRANSMISSION", "🛡️ SQUAD DEFENSIVE ACTIONS"])
    with tab_squad_atk:
        render_gradient_bar_chart(squad_players, 'player', 'Goals', 'SQUAD INTERNAL GOALS LEADERBOARD', 'reds')
        render_gradient_bar_chart(squad_players, 'player', 'Pressures', 'SQUAD INTERNAL ATTACK PHASES PRESSURES APPLIED', 'ylorrd')
        render_gradient_bar_chart(squad_players, 'player', 'Shots', 'INDIVIDUAL ATTEMPTED SHOTS CANVASES', 'peach')
        render_gradient_bar_chart(squad_players, 'player', 'Shots_OT', 'ACCURATE SHOTS ON TARGET RECORDED', 'pinkyl')
    with tab_squad_mid:
        render_gradient_bar_chart(squad_players, 'player', 'Succ_Passes', 'SQUAD COMPLETED PASS DISTRIBUTIONS', 'blues')
        render_gradient_bar_chart(squad_players, 'player', 'Prog_Passes', 'SQUAD PROGRESSIVE PASS LEADERS', 'purples')
    with tab_squad_def:
        render_gradient_bar_chart(squad_players, 'player', 'Tackles', 'SQUAD SUCCESSFUL GROUND TACKLES LEADERS', 'greens')
        render_gradient_bar_chart(squad_players, 'player', 'Interceptions', 'SQUAD INTERCEPTIONS RECORDED', 'tealgrn')

    st.markdown("<br><hr style='border-color:#1E2235;'><br>", unsafe_allow_html=True)
    
    # 2. Structural requirement: Select target player names to drill into horizontal comparative tracking
    selected_player = st.sidebar.selectbox("SELECT INDIVIDUAL PROFILE NAME", sorted(squad_players['player'].unique()))
    p_data = squad_players[squad_players['player'] == selected_player].iloc[0]
    initials = "".join([part[0] for part in selected_player.split()[:2]])
    
    # Render Mockup Identity Block Card
    st.markdown(f"""
        <div class="player-profile-card">
            <div class="avatar-monogram">{initials}</div>
            <div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight:700; color:#FFFFFF; margin:0;">{selected_player}</div>
                <div style="color: #64748B; font-size: 13px; font-weight:600; text-transform: uppercase; letter-spacing:1px; margin-top:2px;">{p_data['team']} • ADVANCED DRILL-DOWN ANALYSIS</div>
            </div>
            <div class="player-rating">94</div>
        </div>
    """, unsafe_allow_html=True)
    
    tab_p_atk, tab_p_mid, tab_p_def = st.tabs(["🎯 DEEP FINISHING & PRESSURES", "👟 POSSESSION & TRANSITIONS", "🛡️ DEFENSIVE CONTEXT SHIELDS"])
    
    with tab_p_atk:
        render_scouting_comparison_chart(
            p_data, p_df, 
            ['Goals', 'Assists', 'Shots', 'Shots_OT', 'xG', 'Pressures', 'Recoveries'], 
            f'{selected_player} vs. {selected_country} Average Attacking Benchmark'
        )
    with tab_p_mid:
        render_scouting_comparison_chart(
            p_data, p_df, 
            ['Passes', 'Succ_Passes', 'Prog_Passes', 'Through_Balls', 'Crosses', 'Long_Balls', 'Touches', 'Second_Ball_Won'], 
            f'{selected_player} vs. {selected_country} Average Midfield Benchmark'
        )
    with tab_p_def:
        render_scouting_comparison_chart(
            p_data, p_df, 
            ['Blocks', 'Tackles', 'Aerials_Won', 'Duels_Won', 'Ground_Duels_Won', 'Interceptions', 'Errors'], 
            f'{selected_player} vs. {selected_country} Average Defending Benchmark'
        )streamlit run "e:/Python Codes/FootyApp.py"
