import heapq
import networkx as nx

# def congestion_weight(u, v, data):
#     # min_cost = float('inf')
#     # for k in G[u][v]:  # loop through all edges between u and v
#     #     data = G[u][v][k]
#     #     cost = data.get('length', 1) * data.get('congestion', 1)
#     #     min_cost = min(min_cost, cost)
#     # return min_cost
    
#     # If this is a MultiGraph, find minimum cost among all parallel edges

#     if isinstance(data, dict):
#         return data.get('length', 1.0) * data.get('congestion', 1.0)
#     return 1.0  # fallback

def congestion_weight(u, v, data):
    try:
        return data.get("length", 1.0) * data.get("congestion", 1.0)
    except Exception as e:
        print(f"⚠️ congestion_weight error on edge ({u}, {v}):", e)
        return 1.0


def custom_Dijkstra(G, source, target):
    # init all to infinity
    dist = {node :float('inf') for node in G}

    parent = {}

    #init source dis 0
    dist[source] = 0

    # minheap
    pq = [(0, source)]

    while pq:
        curr_dis, curr_node = heapq.heappop(pq)

        if curr_dis > dist[curr_node]:
            continue

        for neighbors_node in G.neighbors(curr_node):
            #we have to handle multi edges which have diff key
            min_weight = float('inf')

            for key in G[curr_node][neighbors_node]:
                edge = G[curr_node][neighbors_node][key]
                length = edge.get('length')
                congestion = edge.get('congestion')

                weight = length * congestion

                if weight < min_weight:
                    min_weight = weight


            if dist[curr_node] + min_weight < dist[neighbors_node]:
                dist[neighbors_node] = dist[curr_node] + min_weight
                parent[neighbors_node] = curr_node
                heapq.heappush(pq, (dist[neighbors_node], neighbors_node))

    
    if target not in parent and source != target:
        print("Path not found")
        return []
    
    path = []
    while target != source:
        path.append(target)
        target = parent[target]
    path.append(source)
    path.reverse()

    return path

def path_cost(G, path):
    total = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        min_cost = float('inf')
        for key in G[u][v]:
            edge = G[u][v][key]
            cost = edge['length'] * edge['congestion']
            min_cost = min(min_cost, cost)
        total += min_cost
    return total