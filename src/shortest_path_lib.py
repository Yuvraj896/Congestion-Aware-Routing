import networkx as nx
from src.shortest_path import congestion_weight, path_cost

def shortest_path_nx(G, source, target):
    try:
        path = nx.shortest_path(G, source=source, target=target, weight=congestion_weight)
        # print(path)
        print(f"Length of path: {len(path)}")
        print(f"Cost of path: {path_cost(G, path)}")
        
        return path

    except nx.NetworkXNoPath:
        print("No path found between source and target.")
        return []
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
