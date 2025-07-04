from src.parse_map import loadGraph
from src.congestion_sim import assign_congestion, congestion_color ,save_congestion_map
from src.shortest_path import custom_Dijkstra, congestion_weight, path_cost
from src.shortest_path_lib import shortest_path_nx
from src.visualise import show_folium_map

import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import streamlit_folium as st_folium

#  set the page title
st.set_page_config(page_title="Traffic Visualizer", layout="centered")
st.title("🚦 Traffic Congestion Visualizer")

place = st.text_input("🗺️ Enter city/place:", value="Indore, India")
source_loc = st.text_input("📍 Source location:", value="Rajwada Palace, Indore")
target_loc = st.text_input("📍 Destination location:", value="Indore Junction")

if st.button("🚗 Find Best Route"):
    if place and source_loc and target_loc:
        with st.spinner("⏳ Loading..."):
            # load the graph
            G = loadGraph(place)
            
            if G is None:
                st.error("Error loading graph")
                st.stop()

            # assign congestion to the graph
            assign_congestion(G)

            save_congestion_map(G, place)

            try:
                source_coord = ox.geocode(source_loc)
                target_coord = ox.geocode(target_loc)

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

                    map = show_folium_map(G, shortest_path)
                    st_folium(map, width=700, height=500, use_container_width=True, fit_bounds=True, zoom=12)
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
