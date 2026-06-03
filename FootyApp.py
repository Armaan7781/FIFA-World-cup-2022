import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# --- 1. UI SETUP & HUMANIZED THEME ---
st.set_page_config(page_title="World Cup '22 Hub", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0F0508; color: #F4EAD4; }
        h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
        .stTabs [data-baseweb="tab"] { color: #A3937B !important; font-size: 16px; }
        .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #8A1538 !important; }
        div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 28px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 World Cup '22 Hub")
st.markdown("---")

# --- 2. SIDEBAR ---
st.sidebar.markdown("<h2 style='color:#D4AF37;'>Settings</h2>", unsafe_allow_html=True)
view_mode = st.sidebar.radio("View Mode", ["Team Overview", "Player Deep Dive"])

# --- 3. PITCH MAPPING FUNCTION (The Magic) ---
def draw_pass_network():
    # This is a template function showing how mplsoccer draws the pitch
    # You will feed your spatial X,Y data into this later
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0F0508', line_color='#A3937B')
    fig, ax = pitch.draw(figsize=(10, 7))
    
    # Placeholder for nodes (players) and edges (passes)
    # Example: Plotting a couple of positions just to show the pitch working
    ax.scatter([20, 40, 60], [40, 20, 60], c='#8A1538', edgecolors='#D4AF37', s=500, zorder=2)
    ax.text(20, 40, "LCB", color='white', ha='center', va='center', zorder=3, fontsize=10)
    ax.text(40, 20, "RDM", color='white', ha='center', va='center', zorder=3, fontsize=10)
    ax.text(60, 60, "LW", color='white', ha='center', va='center', zorder=3, fontsize=10)
    
    # Example line for a pass
    ax.plot([20, 40], [40, 20], color='#8A1538', linewidth=4, zorder=1)
    
    plt.title("Average Passing Network", color="#D4AF37", fontsize=16)
    fig.patch.set_facecolor('#0F0508')
    return fig

# --- 4. THE FOUR PILLARS (TABS) ---
tab_attack, tab_mid, tab_def, tab_gk = st.tabs(["⚔️ Attack", "🎯 Midfield", "🛡️ Defense", "🧤 Goalkeepers"])

with tab_attack:
    st.subheader("Attacking Output")
    st.write("Metrics: Goals, Assists, xG, Shots on Target, Presses, Heatmaps.")
    # You will plug your Plotly bar charts here just like the previous version
    
with tab_mid:
    st.subheader("The Engine Room")
    st.write("Metrics: Progressive Passes, Through Balls, Pass Accuracy, Second Balls.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Team Pass Network (Average Positions)**")
        # Render the pitch map we created above
        st.pyplot(draw_pass_network())
    with c2:
        st.write("**Touches & Heatmap**")
        st.info("Spatial Heatmap will render here.")

with tab_def:
    st.subheader("Defensive Solidity")
    st.write("Metrics: Tackles, Interceptions, Aerial Duels, Blocks, Errors leading to goals.")

with tab_gk:
    st.subheader("Between the Sticks")
    st.write("Metrics: Shots Saved, Crosses Claimed, Sweeper Actions, Passing accuracy.")
