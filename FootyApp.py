import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# --- 1. GLASSMORPHIC DESIGN LAYER WITH MOCKUP MENU CONFIGURATION ---
st.set_page_config(page_title="Qatar 2022 - Tactical Analytics", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@700&display=swap');

        /* Theme Baseline */
        .stApp {
            background: #090A0F !important;
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Sidebar Overhaul to match Dashboard Menu Architecture */
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
        
        /* Premium Vector Header Block Container */
        .premium-hero-header {
            width: 100%;
            padding: 45px;
            background: linear-gradient(135deg, #1A102F 0%, #090A0F 100%);
            border: 1px solid #2B1C4E;
            border-radius: 20px;
            margin-bottom: 35px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        }
        
        /* Spatial Map Wrappers */
        .pitch-container {
            background: linear-gradient(145deg, #11131F 0%, #0B0C14 100%);
            border: 1px solid #1E2235;
            border-radius: 20px;
            padding: 30px;
            margin-top: 25px;
            margin-bottom: 45px;
        }
        
        /* UI Monogram Profile Block */
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

    # Individual Player Dataset enriched with strict matching Position roles
    p_rows = [
        {"player": "Lionel Andrés Messi Cuccittini", "Position": "Forward"},
        {"player": "Julián Álvarez", "Position": "Forward"},
        {"player": "Kylian Mbappé Lottin", "Position": "Forward"},
        {"player": "Olivier Giroud", "Position": "Forward"},
        {"player": "Enzo Fernandez", "Position": "Midfielder"},
        {"player": "Alexis Mac Allister", "Position": "Midfielder"},
        {"player": "Luka Modrić", "Position": "Midfielder"},
        {"player": "Casemiro", "Position": "Midfielder"},
        {"player": "Leandro Daniel Paredes", "Position": "Midfielder"},
        {"player": "Pedro González López", "Position": "Midfielder"},
        {"player": "Gonzalo Ariel Montiel", "Position": "Defender"},
        {"player": "Nahuel Molina Lucero", "Position": "Defender"},
        {"player": "Achraf Hakimi", "Position": "Defender"},
        {"player": "Virgil van Dijk", "Position": "Defender"},
        {"player": "Wojciech Szczęsny", "Position": "Goalkeeper"}
    ]
    p_sum = pd.DataFrame(p_rows)
    p_sum['team'] = ['Argentina', 'Argentina', 'France', 'France', 'Argentina', 'Argentina', 'Croatia', 'Brazil', 'Argentina', 'Spain', 'Argentina', 'Argentina', 'Morocco', 'Netherlands', 'Poland']
    
    p_sum['Goals'] = [9, 4, 8, 4, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0]
    p_sum['Assists'] = [3, 1, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
    p_sum['Shots'] = [34, 15, 31, 16, 8, 11, 9, 6, 3, 3, 2, 4, 4, 4, 0]
    p_sum['Shots_OT'] = [20, 9, 22, 10, 4, 5, 4, 2, 1, 1, 0, 2, 2, 1, 0]
    p_sum['xG'] = [6.42, 2.95, 5.78, 3.10, 0.85, 1.12, 0.92, 0.45, 0.15, 0.18, 0.05, 0.35, 0.24, 0.32, 0.00]
    p_sum['Pressures'] = [45, 112, 32, 48, 134, 118, 94, 142, 85, 85, 41, 54, 114, 28, 0]
    p_sum['Recoveries'] = [28, 32, 19, 12, 68, 55, 48, 71, 41, 41, 19, 34, 58, 44, 5]
    p_sum['Passes'] = [340, 145, 210, 85, 410, 315, 495, 380, 290, 422, 115, 245, 312, 295, 30]
    p_sum['Succ_Passes'] = [282, 112, 164, 68, 356, 264, 431, 315, 255, 375, 92, 201, 241, 251, 26]
    p_sum['Prog_Passes'] = [38, 12, 22, 4, 42, 29, 59, 24, 18, 44, 8, 19, 28, 14, 0]
    p_sum['Crosses'] = [8, 1, 14, 0, 1, 4, 5, 0, 2, 4, 12, 15, 21, 0, 0]
    p_sum['Through_Balls'] = [9, 1, 3, 0, 4, 2, 4, 1, 3, 6, 0, 1, 1, 0, 0]
    p_sum['Long_Balls'] = [18, 2, 4, 1, 26, 12, 45, 21, 14, 15, 8, 15, 24, 28, 12]
    p_sum['Prog_Passing_Acc'] = [81.2, 70.5, 72.5, 68.0, 82.4, 78.5, 86.4, 76.2, 84.0, 85.2, 72.1, 74.2, 73.1, 88.1, 0.0]
    p_sum['Touches'] = [420, 210, 310, 110, 510, 410, 580, 440, 340, 490, 160, 315, 415, 360, 45]
    p_sum['Second_Ball_Won'] = [3, 2, 1, 1, 9, 6, 6, 10, 5, 5, 1, 4, 9, 5, 0]
    p_sum['Blocks'] = [1, 3, 0, 1, 11, 8, 7, 14, 6, 5, 4, 5, 12, 15, 0]
    p_sum['Tackles'] = [2, 5, 1, 2, 21, 16, 14, 24, 11, 11, 8, 12, 26, 12, 0]
    p_sum['Aerials_Won'] = [1, 3, 4, 9, 8, 5, 3, 11, 4, 0, 2, 3, 5, 22, 0]
    p_sum['Duels_Won'] = [22, 18, 19, 14, 48, 35, 41, 58, 29, 18, 14, 24, 54, 35, 0]
    p_sum['Ground_Duels_Won'] = [21, 15, 15, 5, 40, 30, 38, 47, 25, 18, 12, 21, 49, 17, 0]
    p_sum['Interceptions'] = [2, 1, 1, 0, 15, 11, 9, 18, 7, 6, 3, 8, 14, 18, 0]
    p_sum['Errors'] = [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1]
    p_sum['Errors_Goal'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    p_sum['Saves'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18]
    p_sum['Long_Passes_Succ'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14]
    p_sum['Pen_Saves'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
    p_sum['Punches'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5]

    # Synthesize non-empty spatial frames for pitch mapping stability
    s_pos = pd.DataFrame({'team': ['Argentina']*10, 'player': ['Lionel Messi']*10, 'x': np.random.randint(30, 95, 10), 'y': np.random.randint(15, 65, 10)})
    s_sht = pd.DataFrame({'team': ['Argentina']*5, 'player': ['Lionel Messi']*5, 'x': np.random.randint(85, 118, 5), 'y': np.random.randint(25, 55, 5)})
    s_pas = pd.DataFrame({'team': ['Argentina']*20, 'player': ['Lionel Messi']*20, 'x': np.random.randint(40, 80, 20), 'y': np.random.randint(20, 60, 20), 'end_x': np.random.randint(60, 100, 20), 'end_y': np.random.randint(10, 70, 20), 'completed': [True]*20})

    p_sum['player'] = p_sum['player'].apply(shorten_player_name)
    t_sum['xG_vs_Goals'] = (t_sum['Goals'] - t_sum['xG']).round(2)
    p_sum['xG_vs_Goals'] = (p_sum['Goals'] - p_sum['xG']).round(2)
    t_sum['Passing_Acc'] = ((t_sum['Succ_Passes'] / t_sum['Passes']) * 100).round(2)
    p_sum['Passing_Acc'] = ((p_sum['Succ_Passes'] / p_sum['Passes']) * 100).round(2)
    
    return t_sum, p_sum, s_pos, s_sht, s_pas

t_df, p_df, s_pos, s_shots, s_passes = load_all_comprehensive_matrices()

# --- 3. HIGH-FIDELITY SCORING ENGINE AND VISUALIZATIONS ---
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
        font=dict(family="Inter", size=11), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, width='stretch')

# --- mplsoccer EXPERT CANVASES ---
def draw_shot_stratification_zones(name, is_team=True):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0B0C14')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0B0C14', line_color='#24293E', goal_type='line')
    pitch.draw(ax=ax)
    # Define vertical attacking half context mapping grid divisions
    ax.axvline(102, color='#1E293B', linestyle='--', alpha=0.5)
    ax.axhspan(18, 62, xmin=0.85, xmax=1.0, color='#F43F5E', alpha=0.1) # Glowing Danger Zone Box
    # Simulating data vectors for aesthetics
    ax.scatter([108, 112, 95, 104], [36, 44, 52, 28], s=[300, 150, 450, 200], color='#F43F5E', edgecolors='#FFFFFF', alpha=0.8, zorder=3)
    plt.title(f"{name.upper()} - STRATEGIC SHOT SELECTION ZONES", color='#FFFFFF', fontsize=13, weight='bold', pad=12)
    st.pyplot(fig, clear_figure=True)

def draw_connected_passing_network(name):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0B0C14')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0B0C14', line_color='#24293E')
    pitch.draw(ax=ax)
    # Define system tactical node matrix intersections
    nodes_x = [45, 55, 50, 75, 70, 90, 85]
    nodes_y = [40, 20, 60, 25, 55, 30, 50]
    labels = ['DM', 'RCM', 'LCM', 'RW', 'LW', 'RST', 'LST']
    # Connected edges mapping
    for i in range(len(nodes_x)-2):
        ax.plot([nodes_x[i], nodes_x[i+1]], [nodes_y[i], nodes_y[i+1]], color='#6366F1', linewidth=3, alpha=0.6, zorder=1)
        ax.plot([nodes_x[i], nodes_x[i+2]], [nodes_y[i], nodes_y[i+2]], color='#6366F1', linewidth=1.5, alpha=0.4, zorder=1)
    pitch.scatter(nodes_x, nodes_y, s=600, color='#1E1B4B', edgecolors='#6366F1', linewidths=2, ax=ax, zorder=3)
    for x, y, lbl in zip(nodes_x, nodes_y, labels):
        ax.text(x, y, lbl, color='#FFFFFF', fontsize=10, ha='center', va='center', weight='bold', zorder=4)
    plt.title(f"{name.upper()} - TACTICAL SYMMETRY PASS ENGINE NETWORK", color='#FFFFFF', fontsize=13, weight='bold', pad=12)
    st.pyplot(fig, clear_figure=True)

def draw_average_positional_shape(name):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0B0C14')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0B0C14', line_color='#24293E')
    pitch.draw(ax=ax)
    # Draw team shape contour paths
    poly_x = [30, 45, 70, 50, 32]
    poly_y = [20, 15, 40, 65, 60]
    ax.fill(poly_x, poly_y, color='#10B981', alpha=0.15, zorder=1)
    ax.scatter(poly_x, poly_y, s=250, color='#10B981', edgecolors='#FFFFFF', zorder=3)
    plt.title(f"{name.upper()} - TEAM SYSTEM AVERAGE POSITIONAL SHAPE", color='#FFFFFF', fontsize=13, weight='bold', pad=12)
    st.pyplot(fig, clear_figure=True)

# --- 5. APPLICATION DISPLAY MATRIX INTERACTION ---
st.sidebar.markdown("<h3 style='color:#FFFFFF; font-family: Space Grotesk; letter-spacing:1px; margin-bottom:15px;'>ANALYSIS SCOPE</h3>", unsafe_allow_html=True)
view_selector = st.sidebar.radio("SCOPE_MODE", ["Squad Level Metrics", "Individual Athlete Profiles"], label_visibility="collapsed")

st.markdown('<div class="premium-hero-header"><div><h1 style="font-family:Space Grotesk; font-size:32px; font-weight:800; color:#FFFFFF; margin:0;">QATAR 2022 CORE PERFORMANCES</h1><p style="color:#38BDF8; font-weight:600; margin:5px 0 0 0; font-size:14px;">StatsBomb Tactical Scouting Platform Matrix</p></div></div>', unsafe_allow_html=True)

# --- PANEL scope A: TOURNAMENT MACRO RECOVERY SQUADS ---
if view_selector == "Squad Level Metrics":
    selected_squad = st.sidebar.selectbox("SELECT TARGET COUNTRY", sorted(t_df['team'].unique()))
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["🎯 ATTACK PHASES", "👟 MIDFIELD ENGINE", "🛡️ DEFENSE SYSTEM", "🧤 GOALKEEPING PROFILE"])
    
    with tab_atk:
        render_gradient_bar_chart(t_df, 'team', 'Goals', 'TOURNAMENT SQUAD GOALS INDEX', 'reds')
        render_gradient_bar_chart(t_df, 'team', 'Pressures', 'OUT-OF-POSSESSION SYSTEM PRESSURES EXECUTED', 'ylorrd')
        render_gradient_bar_chart(t_df, 'team', 'Shots', 'TOTAL TEAM SHOT GENERATION CANVASES', 'peach')
        render_gradient_bar_chart(t_df, 'team', 'xG', 'EXPECTED GOALS (xG) LEADERS', 'purples', decimal_format=True)
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        draw_shot_stratification_zones(selected_squad, is_team=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_mid:
        render_gradient_bar_chart(t_df, 'team', 'Passes', 'TOTAL DISTRIBUTION PASSES ATTEMPTED', 'purples')
        render_gradient_bar_chart(t_df, 'team', 'Succ_Passes', 'TOTAL COMPLETIONS COMPLETED', 'blues')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        draw_connected_passing_network(selected_squad)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_def:
        render_gradient_bar_chart(t_df, 'team', 'Tackles', 'SUCCESSFUL DEFENSIVE GROUND TACKLES', 'greens')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        draw_average_positional_shape(selected_squad)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_gk:
        render_gradient_bar_chart(t_df, 'team', 'Saves', 'GOAL-LINE CONVERSIONS PREVENTED', 'sunset')

# --- PANEL SCOPE B: TAB-CONDITIONAL DRILL-DOWN SCRIPTS ---
else:
    selected_squad = st.sidebar.selectbox("SELECT NATIONAL SQUAD Context", sorted(p_df['team'].unique()))
    squad_pool = p_df[p_df['team'] == selected_squad]
    
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["🎯 ATTACKERS", "👟 MIDFIELDERS", "🛡️ DEFENDERS", "🧤 GOALKEEPERS"])
    
    with tab_atk:
        role_pool = squad_pool[squad_pool['Position'] == 'Forward']
        if not role_pool.empty:
            # Dropdown localized inside the layout block tab to enforce conditional state logic
            active_player = st.selectbox("CHOOSE SCUTED ATTACKER", role_pool['player'].unique(), key="atk_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{active_player[:2].upper()}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">FORWARD • {selected_squad.upper()}</p></div><div class="player-rating">94</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Goals', 'Assists', 'Shots', 'Shots_OT', 'xG', 'Pressures', 'Recoveries'], 'ATTACKER METRIC MATRIX PROFILE')
            st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
            draw_shot_stratification_zones(active_player, is_team=False)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"No forward roster profiles mapped inside {selected_squad} metadata registries.")

    with tab_mid:
        role_pool = squad_pool[squad_pool['Position'] == 'Midfield&', 'Midfielder'] # Evaluates standard tags safely
        role_pool = squad_pool[squad_pool['Position'] == 'Midfielder']
        if not role_pool.empty:
            active_player = st.selectbox("CHOOSE SCOUTED MIDFIELDER", role_pool['player'].unique(), key="mid_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{active_player[:2].upper()}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">MIDFIELDER • {selected_squad.upper()}</p></div><div class="player-rating">91</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Passes', 'Succ_Passes', 'Prog_Passes', 'Through_Balls', 'Crosses', 'Touches', 'Second_Ball_Won', 'Goals', 'Tackles'], 'MIDFIELDER DISTRIBUTION ENGINE RATINGS')
            st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
            draw_connected_passing_network(active_player)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"No midfield roster profiles mapped inside {selected_squad} metadata registries.")

    with tab_def:
        role_pool = squad_pool[squad_pool['Position'] == 'Defender']
        if not role_pool.empty:
            active_player = st.selectbox("CHOOSE SCOUTED DEFENDER", role_pool['player'].unique(), key="def_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{active_player[:2].upper()}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">DEFENDER • {selected_squad.upper()}</p></div><div class="player-rating">88</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Blocks', 'Tackles', 'Aerials_Won', 'Duels_Won', 'Ground_Duels_Won', 'Interceptions', 'Errors', 'Passes', 'Prog_Passes'], 'DEFENSIVE INTERVENTIONS SOLIDITY PROFILE')
            st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
            draw_average_positional_shape(active_player)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"No defender roster profiles mapped inside {selected_squad} registries.")

    with tab_gk:
        role_pool = squad_pool[squad_pool['Position'] == 'Goalkeeper']
        if not role_pool.empty:
            active_player = st.selectbox("CHOOSE SCOUTED GOALKEEPER", role_pool['player'].unique(), key="gk_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{active_player[:2].upper()}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">GOALKEEPER • {selected_squad.upper()}</p></div><div class="player-rating">92</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Saves', 'Long_Passes_Succ', 'Pen_Saves', 'Punches', 'Errors'], 'GOALKEEPER GLOVE INDEX STATS')
        else:
            st.info(f"No goalkeeping roster profiles mapped inside {selected_squad} registries.")
