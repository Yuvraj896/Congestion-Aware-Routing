import folium
from streamlit_folium import st_folium
from src.congestion_sim import congestion_color

def show_folium_map(G, path, city_name):
    path_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]

    mid_lat = sum([p[0] for p in path_coords]) / len(path_coords)
    mid_lon = sum([p[1] for p in path_coords]) / len(path_coords)


    # south west and north east bounds
    sw = [min(p[0] for p in path_coords), min(p[1] for p in path_coords)]
    ne = [max(p[0] for p in path_coords), max(p[1] for p in path_coords)]

    # map build
    map = folium.Map(location=[mid_lat, mid_lon], zoom_start=13, tiles='CartoDB Positron')

    #draw route
    folium.PolyLine(path_coords, color='blue', weight=5, opacity=0.9).add_to(map)

    # markers
    folium.Marker(path_coords[0], popup="Source", icon=folium.Icon(color='green')).add_to(map)
    folium.Marker(path_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(map)

    map.fit_bounds([sw,ne])
    return map

