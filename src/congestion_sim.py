import random
import osmnx as ox
import json, os

from src.live_traffic import get_live_congestion

CACHE_PATH = "data/congestion_cache.json"

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, 'r') as f:
            cache = json.load(f)
        return {tuple(map(float, k.split(","))): v for k, v in cache.items()}
    else:
        return {}
    
def save_cache(cache):
    os.makedirs("data", exist_ok=True)
    stringified = {f"{k[0]},{k[1]}": v for k, v in cache.items()}
    with open(CACHE_PATH, 'w') as f:
        json.dump(stringified, f)

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
        congestion = data.get('congestion', 1)
        color = congestion_color(congestion)
        edge_colors.append(color)

    fig, ax = ox.plot_graph(G, edge_color=edge_colors, edge_linewidth=1.2, node_size=0, bgcolor='white', figsize=(10,10))
    
    file_path = os.path.join(save_dir, f"{place}_congestion_map.png")
    print("Saving congestion map to:", file_path)

    fig.savefig(file_path)


def assign_realtime_congestion(G, maxEdges = None):

    processed = 0
    seen_coords = load_cache()

    fallback_congestion = 1.0

    print("Started Assigning")
    
    for u, v, key, data in G.edges(keys=True, data=True):

        if data.get("length", 0) < 30:
            data["congestion"] = 1.0
            continue

        if maxEdges and processed >= maxEdges:
            break

        try:
            lat1,lon1 = G.nodes[u]['y'], G.nodes[u]['x']
            lat2,lon2 = G.nodes[v]['y'], G.nodes[v]['x']

            mid = round((lat1 + lat2) / 2, 5), round((lon1 + lon2) / 2, 5)

            if mid in seen_coords:
                congestion = seen_coords[mid]
            
            else:
                congestion = get_live_congestion(*mid)
                congestion = min(10.0, congestion)

                # cache
                seen_coords[mid] = congestion
            
            data['congestion'] = congestion
            processed += 1

            if processed % 200 == 0:
                print(f"Processed {processed} edges")

        except Exception as e:
            print(f"⚠️ Couldn't assign congestion to edge ({u}-{v}):", e)
            data['congestion'] = fallback_congestion  # fallback

    # Assign fallback congestion to remaining unprocessed edges
    for u, v, key, data in G.edges(keys=True, data=True):
        if 'congestion' not in data:
            data['congestion'] = fallback_congestion

    save_cache(seen_coords)
    print("✅ Real-time congestion assigned to edges")


