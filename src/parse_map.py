import os
import osmnx as ox
import streamlit as st
import traceback
from shapely.geometry import box

@st.cache_data(show_spinner="📦 Loading map...", persist=True)
def load_cached_graph(src, dst):
    print("🧪 OSMnx version:", ox.__version__)
    return load_graph(src, dst)

def load_graph(src, dst, save_dir="data/graph/"):
    try:
        lat1, lon1 = src
        lat2, lon2 = dst

        file_name = f"{lat1}_{lon1}_{lat2}_{lon2}".replace(" ", "_")
        graph_path = os.path.join(save_dir, file_name)
    
        # try cache
        if(os.path.exists(graph_path)):
            return ox.load_graphml(graph_path)
        

        margin  = 0.01
        north = max(lat1, lat2) + margin
        south = min(lat1, lat2) - margin
        east = max(lon1, lon2) + margin
        west = min(lon1, lon2) - margin

        bbox = (west, south, east, north)

        G = ox.graph_from_bbox(bbox, network_type="drive", simplify=True) 
        os.makedirs(save_dir, exist_ok=True)
        ox.save_graphml(G, filepath=graph_path)

        return G
        
    except Exception as e:
        print("❌ Error loading graph:", e)
        traceback.print_exc()
        return None