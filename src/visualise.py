import folium
from streamlit_folium import st_folium
from src.congestion_sim import congestion_color

def show_folium_map(G, path):
    node = path[0]
    lat = G.nodes[node]['y']
    lon = G.nodes[node]['x']

    map = folium.Map(location=[lat, lon], zoom_start=10 ,tiles="cartodbpositron")

    for u, v, key, data in G.edges(data=True, keys=True):
        color = congestion_color(data.get("congestion",1))
        points = [(G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])]
        folium.PolyLine(points, color=color, weight=2, opacity=0.7).add_to(map)

    route_points = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]
    folium.PolyLine(route_points, color="blue", weight=5, opacity=1).add_to(map)

    folium.Marker(route_points[0], tooltip="Source 📍", icon=folium.Icon(color='green')).add_to(map)
    folium.Marker(route_points[-1], tooltip="Destination 🎯", icon=folium.Icon(color='red')).add_to(map)

    return map

