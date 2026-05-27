import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# --- Institutional UI Configuration (Deep Charcoal & Soft Pink Theme) ---
st.set_page_config(page_title="ARIDAQ | Multi-Particle Routing Terminal", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #070708; color: #f1f2f6; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .aridaq-header { font-family: 'Courier New', monospace; font-size: 30px; font-weight: 900; color: #ffb3d1; letter-spacing: 5px; margin-bottom: -5px; }
    div[data-testid="stForm"] { background-color: #0f0f12; border: 1px solid #1f1f24; border-radius: 8px; padding: 25px; }
    h1, h2, h3, h4 { color: #ffb3d1 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    
    .stButton>button { 
        background-color: #ffb3d1; color: #070708; border-radius: 4px; width: 100%; font-weight: bold;
        border: none; padding: 14px; font-size: 16px; letter-spacing: 2px; font-family: 'Courier New', monospace;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #ffa1c5; box-shadow: 0px 0px 20px rgba(255, 179, 209, 0.35); color: #070708; }
    
    div[data-testid="stTextInput"] input {
        background-color: #050506 !important; color: #ffb3d1 !important;
        font-family: 'Courier New', monospace !important; border: 1px solid #26262b !important;
        font-size: 14px !important; padding: 12px !important;
    }
    
    div[data-testid="stMetricValue"] { color: #ffb3d1; font-family: 'Courier New', monospace; font-size: 28px !important; }
    div[data-testid="stMetricLabel"] { color: #8e9297 !important; }
    
    .section-card { background-color: #0f0f12; border: 1px solid #1f1f24; padding: 25px; border-radius: 6px; margin-bottom: 25px; }
    .playbook-container { background-color: #0f0f12; border-left: 4px solid #ffb3d1; padding: 20px; border-radius: 4px; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="aridaq-header">ARIDAQ</div>', unsafe_allow_html=True)
st.caption("Topological Network Routing Engine // Electrostatic Screening Manifold Search")
st.write("---")

# ─────────────────────────────────────────────────────────────────
# 📥 COMMAND INTERFACE PORTAL
# ─────────────────────────────────────────────────────────────────
st.subheader("📟 Physics-Based Ingestion Terminal")

with st.form("tsp_physics_form"):
    instruction_code = st.text_input(
        "ENTER ROUTING INSTRUCTION CODE OR NODE STREAM:", 
        value="COMPILE TSP_DEBYE_LARGE //DEBYE_LENGTH:6500 //SHOW_MAP:TRUE",
    )
    
    map_url_input = st.text_input(
        "PASTE REAL MAP URL LOCATION COORDINATE MATRIX:",
        value="https://www.google.com/maps/place/@-1.2863,36.8172,15z",
        help="Paste a live Google Maps URL containing an @latitude,longitude coordinate vector."
    )
    
    with st.expander("📋 Edit Target Simulation Matrix Nodes (Auto-Populated Base)"):
        default_hubs = pd.DataFrame([
            {"Hub ID": "H01", "Location Name": "Nairobi Central Depot", "Latitude": -1.2863, "Longitude": 36.8172, "Payload Volume (m³)": 45},
            {"Hub ID": "H02", "Location Name": "Mombasa Port Core", "Latitude": -4.0435, "Longitude": 39.6682, "Payload Volume (m³)": 80},
            {"Hub ID": "H03", "Location Name": "Kisumu Terminal Facility", "Latitude": -0.1022, "Longitude": 34.7617, "Payload Volume (m³)": 35},
            {"Hub ID": "H04", "Location Name": "Eldoret Transit Node", "Latitude": 0.5143, "Longitude": 35.2697, "Payload Volume (m³)": 50},
            {"Hub ID": "H05", "Location Name": "Nakuru Junction Node", "Latitude": -0.3031, "Longitude": 36.0613, "Payload Volume (m³)": 60},
            {"Hub ID": "H06", "Location Name": "Malaba Border Point", "Latitude": 0.6343, "Longitude": 34.2746, "Payload Volume (m³)": 95},
        ])
        df_editable = st.data_editor(default_hubs, num_rows="dynamic", use_container_width=True)
        sim_nodes_count = st.number_input("Generate Synthetic Large-Scale Data Grid Size to Simulate", min_value=6, max_value=8000, value=500, step=100)

    run_engine = st.form_submit_button("COMPILE AND OPTIMIZE NETWORK VIA ARIDAQ SCREENING")

st.write("---")

# ─────────────────────────────────────────────────────────────────
# ⚙️ ARIDAQ DEBYE SCREENING & 1-5 HEURISTIC CORE BACKEND
# ─────────────────────────────────────────────────────────────────
if run_engine:
    start_clock = time.perf_counter()
    
    # Parse input strings
    debye_str = re.search(r"//DEBYE_LENGTH:([\d\.]+)", instruction_code)
    debye_length = float(debye_str.group(1)) if debye_str else 6500.0
    
    map_str = re.search(r"//SHOW_MAP:(\w+)", instruction_code)
    show_map = True if (map_str and map_str.group(1).upper() == "TRUE") else False
    
    screening_constant = 3.17 * (10**9)
    
    # Extract live center coordinates from the Map URL
    center_lat, center_long = -1.2863, 36.8172
    if map_url_input:
        url_coordinates = re.search(r"@(-?[\d\.]+),(-?[\d\.]+)", map_url_input)
        if url_coordinates:
            center_lat = float(url_coordinates.group(1))
            center_long = float(url_coordinates.group(2))

    # Assemble node coordinates array
    lats = list(df_editable["Latitude"].values)
    longs = list(df_editable["Longitude"].values)
    hub_ids = list(df_editable["Hub ID"].values)
    names = list(df_editable["Location Name"].values)
    volumes = list(df_editable["Payload Volume (m³)"].values)
    
    # Securely scale synthetic grid using cluster radii to prevent extreme kilometrage leaks
    if sim_nodes_count > len(lats):
        np.random.seed(42)
        additional_nodes = sim_nodes_count - len(lats)
        # Tightly bound the coordinates to simulate a highly congested logistical cluster space
        rand_lats = center_lat + np.random.normal(0, 0.25, additional_nodes)
        rand_longs = center_long + np.random.normal(0, 0.25, additional_nodes)
        
        for idx in range(additional_nodes):
            lats.append(rand_lats[idx])
            longs.append(rand_longs[idx])
            hub_ids.append(f"N{len(lats) + idx:04d}")
            names.append(f"Cluster Node Field Hub {len(lats) + idx}")
            volumes.append(int(np.random.uniform(15, 65)))
            
    n_total = len(lats)

    # True Non-Euclidean Haversine Calculator
    def haversine_km(lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
        return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    # --- ARIDAQ 1-TO-5 ENERGY STATE HEURISTIC MATRIX EXECUTION ---
    current_node = 0
