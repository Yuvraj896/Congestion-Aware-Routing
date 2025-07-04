import random
import osmnx as ox
import os

from src.live_traffic import get_live_congestion

# assign random congestions to each edges , will add real time in deployment

def assign_congestion(G):
    for u, v, key, data in G.edges(keys=True, data=True):
        data['congestion'] = random.randint(1,10)

    print("Congestions assigned to edges")

def congestion_color(c):
    if c<= 3:
        return 'green'
    elif c<= 7:
        return 'yellow'
    else:
        return 'red'
    
def save_congestion_map(G, place, save_dir="data/images/"):
    # create a new graph with the same nodes and edges as the original graph
    edge_colors = []

    for u, v, key, data in G.edges(data=True, keys=True):
        color = congestion_color(data['congestion'])
        edge_colors.append(color)

    fig, ax = ox.plot_graph(G, edge_color=edge_colors, edge_linewidth=1.2, node_size=0, bgcolor='white', figsize=(10,10))
    
    file_path = os.path.join(save_dir, f"{place}_congestion_map.png")
    print("Saving congestion map to:", file_path)

    fig.savefig(file_path)


def assign_realtime_congestion(G):
    for u, v, key, data in G.edges(keys=True, data=True):
        try:
            lat1,lon1 = G.nodes[u]['y'], G.nodes[u]['x']
            lat2,lon2 = G.nodes[v]['y'], G.nodes[v]['x']

            mid_lat = (lat1 + lat2) / 2
            mid_lon = (lon1 + lon2) / 2

            congestion = get_live_congestion(mid_lat,mid_lon)

            if congestion > 10: congestion=10
            data['congestion'] = congestion

        except Exception as e:
            print(f"⚠️ Couldn't assign congestion to edge ({u}-{v}):", e)
            data['congestion'] = 1  # fallback

        print("✅ Real-time congestion assigned to edges")