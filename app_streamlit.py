import streamlit as st
from streamlit_folium import folium_static
import osmnx as ox

# our modules
from src.parse_map import load_cached_graph
from src.congestion_sim import assign_realtime_congestion, congestion_color, save_congestion_map, assign_congestion
from src.shortest_path_lib import shortest_path_nx
from src.shortest_path import path_cost
from src.visualise import show_folium_map
from src.suggestions import get_place_suggestion
from src.live_traffic import get_user_city

st.set_page_config(page_title="Traffic Visualizer", layout="centered")
st.title("🚦 Traffic Congestion Visualizer")

# ---- Input City ----
place = st.text_input("🗺️ Enter city/place:", value="Indore, India")


# ---- Input Source ----
default_city = get_user_city()
source_query = st.text_input("📍 Type source location", value=default_city)
source_suggestions = get_place_suggestion(source_query, place)
source_selected = st.selectbox("📍 Source Location (choose from suggestions)", [s[0] for s in source_suggestions]) if source_suggestions else None
source_coords = dict(source_suggestions).get(source_selected) if source_selected else None

# ---- Input Destination ----
target_query = st.text_input("📍 Destination location:")
target_suggestions = get_place_suggestion(target_query, place)
target_selected = st.selectbox("📍 Destination Location (choose from suggestions)", [s[0] for s in target_suggestions]) if target_suggestions else None
target_coords = dict(target_suggestions).get(target_selected) if target_selected else None


# ---- Main Logic ----
if st.button("🚗 Find Best Route"):

    if not (source_coords and target_coords):
        st.warning("⚠️ Please select valid source and destination.")
        st.stop()

    with st.spinner("⏳ Loading..."):

        G = load_cached_graph(source_coords, target_coords)
        if G is None:
            st.error("❌ Could not load map graph.")
            st.stop()


        assign_realtime_congestion(G,300)
        save_congestion_map(G, place)

        try:
            # nearest nodes to coordinates
            src_node = ox.distance.nearest_nodes(G, X=source_coords[1], Y=source_coords[0])
            dst_node = ox.distance.nearest_nodes(G, X=target_coords[1], Y=target_coords[0])

            shortest_path = shortest_path_nx(G, src_node, dst_node)

            if not shortest_path:
                st.warning("⚠️ Path not found.")
            else:
                map = show_folium_map(G, shortest_path, place)
                folium_static(map, width=1000, height=650)

                cost = path_cost(G, shortest_path)
                st.success(f"✅ Best route found. Estimated cost: {cost:.2f}")

        except Exception as e:
            st.error(f"⚠️ Error occurred: {e}")

st.markdown("---")
st.caption("Thankyou")
