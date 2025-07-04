from src.parse_map import loadGraph, load_cached_graph
from src.congestion_sim import assign_congestion, congestion_color ,save_congestion_map
from src.shortest_path import custom_Dijkstra, congestion_weight, path_cost
from src.shortest_path_lib import shortest_path_nx
from src.visualise import show_folium_map
from src.suggestions import get_place_suggestion


import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from streamlit_folium import folium_static

#  set the page title
st.set_page_config(page_title="Traffic Visualizer", layout="centered")
st.title("🚦 Traffic Congestion Visualizer")

place = st.text_input("🗺️ Enter city/place:", value="Indore, India")
source_loc = st.text_input("📍 Source location:", value="Rajwada Palace, Indore")
if source_loc:
    source_suggest = get_place_suggestion(source_loc)
    source_choice = st.selectbox("🔎 Choose Source", [s[0] for s in source_suggest])
    source_coord = dict(source_suggest)[source_choice] if source_suggest else None
else:
    source_coord = None

target_loc = st.text_input("📍 Destination location:", value="Indore Junction")
if target_loc:
    target_suggest = get_place_suggestion(target_loc)
    target_choice = st.selectbox("🔎 Choose Source", [s[0] for s in target_suggest])
    target_coord = dict(target_suggest)[target_choice] if target_suggest else None
else:
    target_coord = None


if st.button("🚗 Find Best Route"):
    if place and source_loc and target_loc:
        with st.spinner("⏳ Loading..."):
            # load the graph
            G = load_cached_graph(place)
            
            if G is None:
                st.error("Error loading graph")
                st.stop()

            # assign congestion to the graph
            assign_congestion(G)

            save_congestion_map(G, place)

            try:
                if not source_coord or not target_coord:
                    st.warning("⚠️ Please select valid source and destination.")
                    st.stop()



                print(f"Source coordinates: {source_coord}")
                print(f"Target coordinates: {target_coord}")


                source_node = ox.distance.nearest_nodes(G, X=source_coord[1], Y=source_coord[0])
                target_node = ox.distance.nearest_nodes(G, X=target_coord[1], Y=target_coord[0])


                print(f"Source node: {source_node}")
                print(f"Target node: {target_node}")
                # find the shortest path
                # shortest_path = custom_Dijkstra(G, source_node, target_node, congestion_weight)

                shortest_path = shortest_path_nx(G, source_node, target_node)


                if not shortest_path:
                    st.warning("⚠️ Path not found")
                
                else :
                    edge_colors = []
                    for u, v, k, data in G.edges(data=True, keys=True):  # ✅ CORRECT
                        edge_colors.append(congestion_color(data.get("congestion", 1)))

                    map = show_folium_map(G, shortest_path, place)


                    folium_static(map, width=1000, height=650)


                    st.markdown("### Path Visualization")
                    st.write("Click on the map to zoom in and out.")
                    st.write("The path is highlighted in green.")
                    st.write("The congestion of each edge is represented by the color of the edge.")

                    #show path cost
                    total_cost = path_cost(G,shortest_path)
                    st.success(f"✅ Path found! Total cost: {total_cost:.2f}")


            except Exception as e:
                st.error(f"⚠️ Error: {e}") 
    
    else:
        st.warning("⚠️ Please enter a valid source and target location")
    
st.markdown("---")
st.caption("Made with ❤️ by Yuvraj Mandrah")
