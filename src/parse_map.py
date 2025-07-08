import os
import osmnx as ox
import streamlit as st

def haversine_midpoint(lat1, lon1, lat2, lon2):
    return ((lat1 + lat2) / 2.0, (lon1 + lon2) / 2.0)

@st.cache_data(show_spinner="📦 Loading map...", persist=True)
def load_cached_graph(src, dst):
    return load_graph_buffered(src, dst)

def load_graph_buffered(src, dst, save_dir="data/graph/"):
    lat1, lon1 = src
    lat2, lon2 = dst

    # File-safe name
    file_name = f"{lat1}_{lon1}_{lat2}_{lon2}".replace(".", "_")
    graph_path = os.path.join(save_dir, f"{file_name}.graphml")

    # If exists already, load it
    if os.path.exists(graph_path):
        print("✅ Loaded cached graph")
        return ox.load_graphml(graph_path)

    try:
        # Midpoint between source and destination
        mid_lat, mid_lon = haversine_midpoint(lat1, lon1, lat2, lon2)

        # Distance estimate in degrees → meters
        dist_deg = max(abs(lat1 - lat2), abs(lon1 - lon2))
        buffer_m = int(dist_deg * 111000 * 1.5)  # Add margin
        buffer_m = max(10000, min(buffer_m, 50000))  # clamp between 10km - 50km

        print(f"🧭 Midpoint: ({mid_lat}, {mid_lon}), buffer: {buffer_m} meters")

        # Load road network within buffer around midpoint
        G = ox.graph_from_point((mid_lat, mid_lon), dist=buffer_m, network_type='drive')

        # Save for future use
        os.makedirs(save_dir, exist_ok=True)
        ox.save_graphml(G, filepath=graph_path)
        print("✅ Graph saved:", graph_path)

        return G

    except Exception as e:
        print("❌ Error in load_graph_buffered:", e)
        return None
