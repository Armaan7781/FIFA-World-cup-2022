import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PREMIUM UI CUSTOM CONFIGURATION ---
st.set_page_config(page_title="Qatar 2022 - Elite Analytics Hub", layout="wide")

# CSS Injection for Glassmorphism, Neon Accents, and Sleek Cards
st.markdown("""
    <style>
        /* Global Background and Typography */
        .stApp {
            background: radial-gradient(circle at 50% 10%, #1a1c24 0%, #0d0e12 80%);
            color: #E2E8F0;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        /* Modern Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #090a0d !important;
            border-right: 1px solid #1e222b;
        }
        
        /* Top Navigation Custom Tab Bar */
        .stTabs [data-baseweb="tab"] {
            color: #64748B !important;
            font-size: 15px;
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
        }
        .stTabs [aria-selected="true"] {
            color: #38BDF8 !important;
            border-bottom: 2px solid #38BDF8 !important;
        }
        
        /* Custom UI Dribbble-Style Cards */
        .metric-card {
            background: linear-gradient(135deg, #161920 0%, #111318 100%);
            border: 1px solid #222733;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            border-color: #38BDF8;
            transform: translateY(-2px);
        }
        .metric-header {
            color: #94A3B8;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .metric-value {
            color: #FFFFFF;
            font-size: 36px;
            font-weight: 800;
            font-family: 'Space Grotesk', sans-serif;
        }
        .metric-sub {
            color: #38BDF8;
            font-size: 13px;
            margin-top: 4px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA EXTRACTION ENGINE ---
@st.cache_data
def load_advanced_data():
    try:
        teams = pd.read_csv('wc_team_advanced.csv')
        players = pd.read_csv('wc_player_advanced.csv')
    except FileNotFoundError:
        teams = pd.DataFrame({
            'team': ['Argentina', 'France', 'Croatia', 'Morocco', 'Brazil', 'England', 'Spain', 'Netherlands'],
            'Goals': [15, 16, 8, 6, 8, 13, 9, 10],
            'xG': [15.2, 13.8, 7.9, 5.2, 10.4, 11.2, 6.8, 7.1],
            'Total_Passes': [3989, 3421, 4102, 2891, 3105, 3240, 4210, 2980],
            'Completed_Passes': [3410, 2890, 3512, 2340, 2710, 2850, 3810, 2490],
            'Key_Passes': [48, 45, 31, 22, 38, 41, 35, 26],
            'Defensive_Actions': [410, 380, 521, 594, 320, 290, 310, 360],
            'Saves': [12, 17, 25, 21, 9, 8, 6, 14]
        })
        players = pd.DataFrame({
            'player': ['Kylian Mbappé', 'Lionel Messi', 'Olivier Giroud', 'Julián Álvarez', 'Antoine Griezmann', 'Luka Modrić'],
            'team': ['France', 'Argentina', 'France', 'Argentina', 'France', 'Croatia'],
            'Goals': [8, 7, 4, 4, 0, 1],
            'xG': [5.8, 6.4, 3.2, 2.9, 1.8, 0.9],
            'Key_Passes': [11, 18, 5, 4, 22, 14],
            'Completed_Passes': [182, 241, 72, 85, 210, 415]
        })
    return teams, players

team_df, player_df = load_advanced_data()

# --- 3. DYNAMIC CHART HELPER ---
def apply_premium_chart_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#94A3B8"),
        title=dict(font=dict(size=16, color="#FFFFFF", family="Space Grotesk")), # <-- Fixed layout attribute mapping
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#1E293B", zeroline=False)
    )
    return fig

# --- 4. HEADER ACCENT ---
st.markdown("<h1 style='font-size: 32px; font-weight: 800; letter-spacing: -1px; margin-bottom: 0;'>STATS & ANALYTICS HUB</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; margin-top:-5px;'>Qatar FIFA World Cup 2022 Core Performance Index</p>", unsafe_allow_html=True)

# --- 5. VIEW TOGGLE ---
view_mode = st.sidebar.radio("VIEW MODE", ["Squad Overviews", "Individual Profiles"])

# --- VIEW: SQUAD OVERVIEWS ---
if view_mode == "Squad Overviews":
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-header">🏆 Gold Medalist</div><div class="metric-value">Argentina</div><div class="metric-sub">3rd Star Secured</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-header">🎯 Top Firepower</div><div class="metric-value">France</div><div class="metric-sub">16 Goals Scored</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-header">📈 Peak xG Engine</div><div class="metric-value">15.2</div><div class="metric-sub">Argentina Control</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-header">🛡️ Defensive Wall</div><div class="metric-value">Morocco</div><div class="metric-sub">594 Hard Interventions</div></div>', unsafe_allow_html=True)

    tab_atk, tab_mid, tab_def, tab_gk = st.tabs(["ATTACK", "MIDFIELD", "DEFENSE", "GOALKEEPERS"])
    
    with tab_atk:
        col1, col2 = st.columns([1, 1])
        with col1:
            fig = px.bar(team_df.sort_values(by="Goals", ascending=False), x="team", y="Goals", title="Attacking Output by Squad")
            fig.update_traces(marker_color='#F43F5E', marker_line_color='#FB7185', marker_line_width=1)
            st.plotly_chart(apply_premium_chart_theme(fig), use_container_width=True)
        with col2:
            fig = px.scatter(team_df, x="xG", y="Goals", text="team", size="Goals", title="Conversion Efficiency Profile (Actual vs Expected)")
            fig.update_traces(marker=dict(color='#38BDF8', line=dict(width=1, color='#7DD3FC')), textposition='top center')
            st.plotly_chart(apply_premium_chart_theme(fig), use_container_width=True)
            
    with tab_mid:
        col1, col2 = st.columns(2)
        with col1:
            df_mid = team_df.assign(Pass_Acc=((team_df['Completed_Passes'] / team_df['Total_Passes']) * 100).round(1))
            fig = px.bar(df_mid.sort_values(by="Pass_Acc", ascending=False), x="team", y="Pass_Acc", title="Distribution Accuracy Rating (%)")
            fig.update_traces(marker_color='#6366F1')
            st.plotly_chart(apply_premium_chart_theme(fig), use_container_width=True)
        with col2:
            fig = px.bar(team_df.sort_values(by="Key_Passes", ascending=False), x="team", y="Key_Passes", title="Chances Created (Key Passes)")
            fig.update_traces(marker_color='#A855F7')
            st.plotly_chart(apply_premium_chart_theme(fig), use_container_width=True)

    with tab_def:
        fig = px.bar(team_df.sort_values(by="Defensive_Actions", ascending=False), x="team", y="Defensive_Actions", title="Defensive Volume Index")
        fig.update_traces(marker_color='#10B981')
        st.plotly_chart(apply_premium_chart_theme(fig), use_container_width=True)
        
    with tab_gk:
        fig = px.bar(team_df.sort_values(by="Saves", ascending=False), x="team", y="Saves", title="Crucial Conversions Saved")
        fig.update_traces(marker_color='#F59E0B')
        st.plotly_chart(apply_premium_chart_theme(fig), use_container_width=True)

# --- VIEW: INDIVIDUAL PROFILES ---
else:
    st.markdown("<h3 style='margin-bottom:15px;'>Player Index</h3>", unsafe_allow_html=True)
    
    col_side, col_main = st.columns([1, 3])

    with col_side:
        players_list = sorted(player_df['player'].unique()) if not player_df.empty else []
        if not players_list:
            st.info("No player data available")
            selected_player = None
            p_data = None
        else:
            selected_player = st.selectbox("CHOOSE PLAYER PROFILE", players_list)
            sel_rows = player_df[player_df['player'] == selected_player]
            p_data = sel_rows.iloc[0] if not sel_rows.empty else None
        
        if p_data is not None:
            st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #38BDF8;">
                    <div class="metric-header">Squad Role</div>
                    <div class="metric-value" style="font-size:24px;">{p_data['player']}</div>
                    <div class="metric-sub">{p_data['team']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No player data available")
        
    with col_main:
        categories = ['Goals', 'xG', 'Key_Passes', 'Completed_Passes']
        
        fig = go.Figure()
        if p_data is not None:
            vals = [
                float(p_data.get('Goals', 0)) * 5,
                float(p_data.get('xG', 0)) * 5,
                float(p_data.get('Key_Passes', 0)),
                float(p_data.get('Completed_Passes', 0)) / 10
            ]
        else:
            vals = [0, 0, 0, 0]

        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=categories,
            fill='toself',
            fillcolor='rgba(56, 189, 248, 0.2)',
            line=dict(color='#38BDF8', width=2),
            name=selected_player if p_data is not None else 'N/A'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=False),
                bgcolor='rgba(22, 25, 32, 0.7)',
                gridshape='circular'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8")
        )
        st.plotly_chart(fig, use_container_width=True)
