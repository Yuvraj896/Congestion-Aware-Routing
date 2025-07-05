import osmnx as ox
import os
import streamlit as st

# store graph in cache , no need to rebuild until the location changes

@st.cache_data(show_spinner="Loading map...", persist=True)
def load_cached_graph(place_name):
    return loadGraph(place_name)

def loadGraph(place_name, save_dir="data/graph/", image_dir="data/images/"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        name = place_name.lower().replace(",","").replace(" ","_")

        graph_path = os.path.join(save_dir, f"{name}.graphml")
        image_path = os.path.join(image_dir, f"{name}.png")

        G= ox.graph_from_place(place_name, network_type="drive")

        # save the graph 
        ox.save_graphml(G, filepath=graph_path)
        print("Graph saved to: ", graph_path)

        # plot the graph    
        fig ,ax = ox.plot_graph(G, bgcolor='white', node_color='black', edge_color='blue', node_size=5, edge_linewidth=0.8)
        fig.savefig(image_path)

        print("Road map image saved at: ",image_path)
        return G
    
    except Exception as e:
        print("❌ Error in loadGraph:", e)
        return None