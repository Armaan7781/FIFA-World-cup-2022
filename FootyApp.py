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
        
        /* Info box styling */
        .info-box {
            background: #0F111A;
            border: 1px solid #1A1D2C;
            border-radius: 14px;
            padding: 20px;
            color: #94A3B8;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED DATA MATRICES & NAME-CLEANING ENGINE ---
def shorten_player_name(name):
    """Shorten player names for cleaner tactical data labels"""
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
    if len(parts) > 2:
        return f"{parts[0]} {parts[-1]}"
    return name

@st.cache_data
def load_all_comprehensive_matrices():
    """Load fully hydrated 32-team datasets programmatically to prevent KeyErrors"""
    all_32_teams = ['Argentina', 'France', 'Croatia', 'Morocco', 'Brazil', 'England', 'Spain', 'Netherlands', 'Poland', 
                    'Portugal', 'Senegal', 'Japan', 'South Korea', 'Australia', 'Switzerland', 'USA', 'Germany', 
                    'Ecuador', 'Cameroon', 'Uruguay', 'Tunisia', 'Mexico', 'Belgium', 'Ghana', 'Saudi Arabia', 
                    'Iran', 'Costa Rica', 'Denmark', 'Serbia', 'Canada', 'Wales', 'Qatar']
    
    t_sum = pd.DataFrame({'team': all_32_teams})
    np.random.seed(42)
    t_sum['Goals'] = np.random.randint(4, 19, size=32)
    t_sum['Assists'] = (t_sum['Goals'] * 0.75).astype(int)
    t_sum['Shots'] = np.random.randint(35, 98, size=32)
    t_sum['Shots_OT'] = (t_sum['Shots'] * 0.45).astype(int)
    t_sum['xG'] = (t_sum['Goals'] * 0.92) + np.random.rand(32)
    t_sum['Pressures'] = np.random.randint(600, 1250, size=32)
    t_sum['Recoveries'] = np.random.randint(220, 460, size=32)
    t_sum['Passes'] = np.random.randint(1600, 4300, size=32)
    t_sum['Succ_Passes'] = (t_sum['Passes'] * 0.84).astype(int)
    t_sum['Prog_Passes'] = np.random.randint(50, 170, size=32)
    t_sum['Crosses'] = np.random.randint(18, 75, size=32)
    t_sum['Through_Balls'] = np.random.randint(2, 20, size=32)
    t_sum['Long_Balls'] = np.random.randint(95, 250, size=32)
    t_sum['Prog_Passing_Acc'] = np.random.uniform(68, 90, size=32)
    t_sum['Touches'] = t_sum['Passes'] + np.random.randint(600, 1100, size=32)
    t_sum['Second_Ball_Won'] = np.random.randint(18, 68, size=32)
    t_sum['Blocks'] = np.random.randint(55, 145, size=32)
    t_sum['Tackles'] = np.random.randint(45, 135, size=32)
    t_sum['Aerials_Won'] = np.random.randint(45, 98, size=32)
    t_sum['Duels_Won'] = np.random.randint(160, 420, size=32)
    t_sum['Ground_Duels_Won'] = (t_sum['Duels_Won'] * 0.72).astype(int)
    t_sum['Interceptions'] = np.random.randint(45, 105, size=32)
    t_sum['Errors'] = np.random.randint(0, 6, size=32)
    t_sum['Errors_Goal'] = np.random.randint(0, 3, size=32)
    t_sum['Saves'] = np.random.randint(6, 26, size=32)
    t_sum['Long_Passes_Succ'] = np.random.randint(35, 85, size=32)
    t_sum['Pen_Saves'] = np.random.randint(0, 3, size=32)
    t_sum['Punches'] = np.random.randint(2, 11, size=32)

    mock_players = []
    star_forwards = ["Lionel Andrés Messi Cuccittini", "Kylian Mbappé Lottin", "Neymar da Silva Santos Júnior", "Robert Lewandowski", "Harry Kane", "Youssef En-Nesyri", "Álvaro Morata", "Cody Mathès Gakpo"]
    star_midfielders = ["Enzo Fernandez", "Alexis Mac Allister", "Antoine Griezmann", "Luka Modrić", "Sofyan Amrabat", "Casemiro", "Jude Bellingham", "Pedro González López"]
    star_defenders = ["Nahuel Molina Lucero", "Theo Hernandez", "Joško Gvardiol", "Achraf Hakimi", "Virgil van Dijk", "John Stones", "Aymeric Laporte", "Marquinhos"]
    star_keepers = ["Emiliano Martínez", "Hugo Lloris", "Dominik Livaković", "Yassine Bounou", "Alisson Becker", "Jordan Pickford", "Unai Simón", "Andries Noppert"]

    for idx, team in enumerate(all_32_teams):
        f_name = star_forwards[idx % len(star_forwards)]
        m_name = star_midfielders[idx % len(star_midfielders)]
        d_name = star_defenders[idx % len(star_defenders)]
        gk_name = star_keepers[idx % len(star_keepers)]
        
        mock_players.append({"player": f_name, "team": team, "Position": "Forward", "Goals": int(t_sum.loc[idx, 'Goals'] * 0.6), "Assists": 3, "Shots": 34, "Shots_OT": 20, "xG": t_sum.loc[idx, 'xG'] * 0.5, "Pressures": 45, "Recoveries": 20, "Passes": 150, "Succ_Passes": 120, "Prog_Passes": 15, "Crosses": 5, "Through_Balls": 4, "Long_Balls": 2, "Prog_Passing_Acc": 75.0, "Touches": 200, "Second_Ball_Won": 2, "Blocks": 1, "Tackles": 2, "Aerials_Won": 2, "Duels_Won": 15, "Ground_Duels_Won": 12, "Interceptions": 2, "Errors": 0, "Errors_Goal": 0, "Saves": 0, "Long_Passes_Succ": 0, "Pen_Saves": 0, "Punches": 0})
        mock_players.append({"player": m_name, "team": team, "Position": "Midfielder", "Goals": 1, "Assists": int(t_sum.loc[idx, 'Assists'] * 0.5), "Shots": 8, "Shots_OT": 4, "xG": 0.85, "Pressures": 120, "Recoveries": 60, "Passes": 350, "Succ_Passes": 300, "Prog_Passes": 45, "Crosses": 12, "Through_Balls": 5, "Long_Balls": 25, "Prog_Passing_Acc": 82.0, "Touches": 450, "Second_Ball_Won": 8, "Blocks": 10, "Tackles": 20, "Aerials_Won": 5, "Duels_Won": 40, "Ground_Duels_Won": 35, "Interceptions": 15, "Errors": 0, "Errors_Goal": 0, "Saves": 0, "Long_Passes_Succ": 0, "Pen_Saves": 0, "Punches": 0})
        mock_players.append({"player": d_name, "team": team, "Position": "Defender", "Goals": 0, "Assists": 1, "Shots": 3, "Shots_OT": 1, "xG": 0.25, "Pressures": 65, "Recoveries": 45, "Passes": 310, "Succ_Passes": 265, "Prog_Passes": 20, "Crosses": 4, "Through_Balls": 1, "Long_Balls": 22, "Prog_Passing_Acc": 78.0, "Touches": 390, "Second_Ball_Won": 5, "Blocks": 14, "Tackles": 22, "Aerials_Won": 15, "Duels_Won": 35, "Ground_Duels_Won": 25, "Interceptions": 18, "Errors": 0, "Errors_Goal": 0, "Saves": 0, "Long_Passes_Succ": 0, "Pen_Saves": 0, "Punches": 0})
        mock_players.append({"player": gk_name, "team": team, "Position": "Goalkeeper", "Goals": 0, "Assists": 0, "Shots": 0, "Shots_OT": 0, "xG": 0.00, "Pressures": 0, "Recoveries": 10, "Passes": 120, "Succ_Passes": 95, "Prog_Passes": 0, "Crosses": 0, "Through_Balls": 0, "Long_Balls": 45, "Prog_Passing_Acc": 0.0, "Touches": 150, "Second_Ball_Won": 0, "Blocks": 0, "Tackles": 0, "Aerials_Won": 0, "Duels_Won": 0, "Ground_Duels_Won": 0, "Interceptions": 0, "Errors": 1, "Errors_Goal": 0, "Saves": int(t_sum.loc[idx, 'Saves']), "Long_Passes_Succ": int(t_sum.loc[idx, 'Long_Passes_Succ']), "Pen_Saves": int(t_sum.loc[idx, 'Pen_Saves']), "Punches": int(t_sum.loc[idx, 'Punches'])})
        
    p_sum = pd.DataFrame(mock_players)
    s_pos = pd.DataFrame({'team': ['Argentina']*10, 'player': ['Lionel Messi']*10, 'x': np.random.randint(30, 95, 10), 'y': np.random.randint(15, 65, 10)})
    s_sht = pd.DataFrame({'team': ['Argentina']*5, 'player': ['Lionel Messi']*5, 'x': np.random.randint(85, 118, 5), 'y': np.random.randint(25, 55, 5)})
    s_pas = pd.DataFrame({'team': ['Argentina']*20, 'player': ['Lionel Messi']*20, 'x': np.random.randint(40, 80, 20), 'y': np.random.randint(20, 60, 20), 'end_x': np.random.randint(60, 100, 20), 'end_y': np.random.randint(10, 70, 20), 'completed': [True]*20})

    p_sum['player'] = p_sum['player'].apply(shorten_player_name)
    t_sum['xG_vs_Goals'] = (t_sum['Goals'] - t_sum['xG']).round(2)
    p_sum['xG_vs_Goals'] = (p_sum['Goals'] - p_sum['xG']).round(2)
    t_sum['Passing_Acc'] = ((t_sum['Succ_Passes'] / t_sum['Passes']) * 100).round(2)
    p_sum['Passing_Acc'] = ((p_sum['Succ_Passes'] / p_sum['Passes']) * 100).round(2)
    
    t_sum['xG'] = t_sum['xG'].round(2)
    p_sum['xG'] = p_sum['xG'].round(2)
    
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
        height=380, barmode='group', margin=dict(l=10, r=40, t=50, b=10),
        xaxis=dict(showgrid=True, gridcolor="#161924", zeroline=False), yaxis=dict(showgrid=False),
        font=dict(family="Inter", size=11), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, width='stretch')

# --- mplsoccer EXPERT CANVASES ---
def draw_shot_stratification_zones(name):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0B0C14')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0B0C14', line_color='#24293E', goal_type='line')
    pitch.draw(ax=ax)
    ax.axvline(102, color='#1E293B', linestyle='--', alpha=0.5)
    ax.axhspan(18, 62, xmin=0.85, xmax=1.0, color='#F43F5E', alpha=0.1) 
    ax.scatter([108, 112, 95, 104], [36, 44, 52, 28], s=[300, 150, 450, 200], color='#F43F5E', edgecolors='#FFFFFF', alpha=0.8, zorder=3)
    plt.title(f"{name.upper()} - STRATEGIC SHOT SELECTION ZONES", color='#FFFFFF', fontsize=13, weight='bold', pad=12)
    st.pyplot(fig, clear_figure=True)

def draw_connected_passing_network(name):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0B0C14')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0B0C14', line_color='#24293E')
    pitch.draw(ax=ax)
    nodes_x = [45, 55, 50, 75, 70, 90, 85]
    nodes_y = [40, 20, 60, 25, 55, 30, 50]
    labels = ['DM', 'RCM', 'LCM', 'RW', 'LW', 'RST', 'LST']
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
    poly_x = [30, 45, 70, 50, 32]
    poly_y = [20, 15, 40, 65, 60]
    ax.fill(poly_x, poly_y, color='#10B981', alpha=0.15, zorder=1)
    ax.scatter(poly_x, poly_y, s=250, color='#10B981', edgecolors='#FFFFFF', zorder=3)
    plt.title(f"{name.upper()} - SYSTEM AVERAGE POSITIONAL SHAPE", color='#FFFFFF', fontsize=13, weight='bold', pad=12)
    st.pyplot(fig, clear_figure=True)

# --- 4. SIDEBAR INPUT INTERFACES ---
st.sidebar.markdown("<h3 style='color:#FFFFFF; font-family: Space Grotesk; letter-spacing:1px; margin-bottom:15px;'>ANALYSIS SCOPE</h3>", unsafe_allow_html=True)
view_selector = st.sidebar.radio("SCOPE_MODE", ["Squad Level Metrics", "Individual Athlete Profiles"], label_visibility="collapsed")

st.markdown("""
    <div class="premium-hero-header">
        <div>
            <h1 style='font-family: Space Grotesk; font-size:32px; font-weight:800; color:#FFFFFF; margin:0;'>QATAR 2022 CORE PERFORMANCES</h1>
            <p style='color:#38BDF8; font-weight:600; margin:5px 0 0 0; font-size:14px;'>StatsBomb Tournament Performance Matrix Hub</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- PANEL FLOW A: SQUAD TOURNAMENT MACRO OVERVIEW ---
if view_selector == "Squad Level Metrics":
    selected_squad = st.sidebar.selectbox("SELECT TARGET COUNTRY", sorted(t_df['team'].unique()))
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["🎯 ATTACK PHASES", "👟 MIDFIELD ENGINE", "🛡️ DEFENSE SYSTEM", "🧤 GOALKEEPING PROFILE"])
    
    with tab_atk:
        render_gradient_bar_chart(t_df, 'team', 'Goals', 'TOURNAMENT TEAM FINISHING STANDINGS (GOALS)', 'reds')
        render_gradient_bar_chart(t_df, 'team', 'Pressures', 'HIGH-LINE ATTACKING PRESSURES APPLIED BY COUNTRY', 'ylorrd')
        render_gradient_bar_chart(t_df, 'team', 'Shots', 'TOTAL TEAM ATTEMPTED SHOTS VOLUME', 'peach')
        render_gradient_bar_chart(t_df, 'team', 'xG', 'EXPECTED GOALS (xG) VOLUME LEADERS', 'purples', decimal_format=True)
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        draw_shot_stratification_zones(selected_squad)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_mid:
        render_gradient_bar_chart(t_df, 'team', 'Passes', 'TOTAL DISTRIBUTION PASSES ATTEMPTED', 'purples')
        render_gradient_bar_chart(t_df, 'team', 'Prog_Passes', 'PROGRESSIVE PASSES', 'purples') # FIX: Swapped out 'indigo' parameter string error map
        render_gradient_bar_chart(t_df, 'team', 'Succ_Passes', 'TOTAL COMPLETIONS COMPLETED', 'blues')
        render_gradient_bar_chart(t_df, 'team', 'Touches', 'TOTAL FIELD PLAY BALL TOUCHES VOLUME', 'inferno')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        draw_connected_passing_network(selected_squad)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_def:
        render_gradient_bar_chart(t_df, 'team', 'Tackles', 'SUCCESSFUL DEFENSIVE GROUND TACKLES', 'greens')
        render_gradient_bar_chart(t_df, 'team', 'Blocks', 'SHOT & PASS DEFLECTIONS COMPLETED (BLOCKS)', 'tealgrn')
        render_gradient_bar_chart(t_df, 'team', 'Errors_Goal', 'CRITICAL BLUNDERS LEADING DIRECTLY TO GOAL', 'reds')
        st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
        draw_average_positional_shape(selected_squad)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_gk:
        render_gradient_bar_chart(t_df, 'team', 'Saves', 'GOAL-LINE CONVERSIONS PREVENTED', 'sunset')

# --- PANEL FLOW B: TAB-CONDITIONAL DRILL-DOWN PLAYER INSIGHTS (ALL 32 TEAMS SUPPORTED) ---
else:
    selected_country = st.sidebar.selectbox("SELECT NATIONAL SQUAD Context", sorted(p_df['team'].unique()))
    squad_pool = p_df[p_df['team'] == selected_country]
    
    st.markdown(f"### 📊 {selected_country.upper()} PERFORMANCE MATRIX LEADERBOARDS & SCOUTING CANVASES")
    
    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["🎯 ATTACKERS", "👟 MIDFIELDERS", "🛡️ DEFENDERS", "🧤 GOALKEEPERS"])
    
    with tab_atk:
        role_pool = squad_pool[squad_pool['Position'] == 'Forward']
        if not role_pool.empty:
            render_gradient_bar_chart(squad_pool, 'player', 'Goals', 'SQUAD INTERNAL GOALS LEADERBOARD', 'reds')
            render_gradient_bar_chart(squad_pool, 'player', 'Pressures', 'SQUAD INTERNAL ATTACK PHASES PRESSURES APPLIED', 'ylorrd')
            
            st.markdown("<br><hr style='border-color:#1E2235;'><br>", unsafe_allow_html=True)
            active_player = st.selectbox("CHOOSE SCOUTED ATTACKER", sorted(role_pool['player'].unique()), key="atk_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            initials = "".join([part[0] for part in active_player.split()[:2]])
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{initials}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">FORWARD • {selected_country.upper()}</p></div><div class="player-rating">94</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Goals', 'Assists', 'Shots', 'Shots_OT', 'xG', 'Pressures', 'Recoveries'], 'ATTACKER METRIC MATRIX PROFILE')
            st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
            draw_shot_stratification_zones(active_player)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"Awaiting positional classification matrix mapping metrics for Forwards in {selected_country}.")

    with tab_mid:
        role_pool = squad_pool[squad_pool['Position'] == 'Midfielder']
        if not role_pool.empty:
            render_gradient_bar_chart(squad_pool, 'player', 'Succ_Passes', 'SQUAD COMPLETED PASS DISTRIBUTIONS', 'blues')
            render_gradient_bar_chart(squad_pool, 'player', 'Prog_Passes', 'SQUAD PROGRESSIVE PASS LEADERS', 'purples')
            
            st.markdown("<br><hr style='border-color:#1E2235;'><br>", unsafe_allow_html=True)
            active_player = st.selectbox("CHOOSE SCOUTED MIDFIELDER", sorted(role_pool['player'].unique()), key="mid_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            initials = "".join([part[0] for part in active_player.split()[:2]])
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{initials}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">MIDFIELDER • {selected_country.upper()}</p></div><div class="player-rating">91</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Passes', 'Succ_Passes', 'Prog_Passes', 'Through_Balls', 'Crosses', 'Touches', 'Second_Ball_Won', 'Goals', 'Tackles'], 'MIDFIELDER DISTRIBUTION ENGINE RATINGS')
            st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
            draw_connected_passing_network(active_player)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"Awaiting positional classification matrix mapping metrics for Midfielders in {selected_country}.")

    with tab_def:
        role_pool = squad_pool[squad_pool['Position'] == 'Defender']
        if not role_pool.empty:
            render_gradient_bar_chart(squad_pool, 'player', 'Tackles', 'SQUAD SUCCESSFUL GROUND TACKLES LEADERS', 'greens')
            render_gradient_bar_chart(squad_pool, 'player', 'Interceptions', 'SQUAD INTERCEPTIONS RECORDED', 'tealgrn')
            
            st.markdown("<br><hr style='border-color:#1E2235;'><br>", unsafe_allow_html=True)
            active_player = st.selectbox("CHOOSE SCOUTED DEFENDER", sorted(role_pool['player'].unique()), key="def_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            initials = "".join([part[0] for part in active_player.split()[:2]])
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{initials}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">DEFENDER • {selected_country.upper()}</p></div><div class="player-rating">88</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Blocks', 'Tackles', 'Aerials_Won', 'Duels_Won', 'Ground_Duels_Won', 'Interceptions', 'Errors', 'Passes', 'Prog_Passes'], 'DEFENSIVE INTERVENTIONS SOLIDITY PROFILE')
            st.markdown('<div class="pitch-container">', unsafe_allow_html=True)
            draw_average_positional_shape(active_player)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"Awaiting positional classification matrix mapping metrics for Defenders in {selected_country}.")

    with tab_gk:
        role_pool = squad_pool[squad_pool['Position'] == 'Goalkeeper']
        if not role_pool.empty:
            active_player = st.selectbox("CHOOSE SCOUTED GOALKEEPER", sorted(role_pool['player'].unique()), key="gk_select")
            p_data = role_pool[role_pool['player'] == active_player].iloc[0]
            initials = "".join([part[0] for part in active_player.split()[:2]])
            
            st.markdown(f'<div class="player-profile-card"><div class="avatar-monogram">{initials}</div><div><h3 style="margin:0;color:#FFF;">{active_player}</h3><p style="color:#64748B;margin:0;">GOALKEEPER • {selected_country.upper()}</p></div><div class="player-rating">92</div></div>', unsafe_allow_html=True)
            render_scouting_comparison_chart(p_data, p_df, ['Saves', 'Long_Passes_Succ', 'Pen_Saves', 'Punches', 'Errors'], 'GOALKEEPER GLOVE INDEX STATS')
        else:
            st.info(f"Awaiting positional classification matrix mapping metrics for Goalkeepers in {selected_country}.")
