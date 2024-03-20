import pandas as pd
import numpy as np


data = pd.read_csv(r'D:\Walmart_Bits_Pilani\part_a_input_dataset_1.csv')

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 
    return c * r

depot = pd.DataFrame({'order_id': [0], 'lng': [data['depot_lng'].iloc[0]], 'lat': [data['depot_lat'].iloc[0]]})
data = pd.concat([depot, data[['lng', 'lat']]]).reset_index(drop=True)

distances = np.zeros((data.shape[0], data.shape[0]))
for i in range(data.shape[0]):
    for j in range(data.shape[0]):
        distances[i][j] = haversine(data.loc[i, 'lng'], data.loc[i, 'lat'], data.loc[j, 'lng'], data.loc[j, 'lat'])

def nearest_neighbor_tsp(distances):
    path = [0]  
    number_of_nodes = len(distances)
    total_distance = 0
    unvisited = set(range(1, number_of_nodes))
    
    def find_nearest_neighbor(current_node, unvisited, distances):
        nearest_neighbor = None
        shortest_distance = float('inf')
        for neighbor in unvisited:
            if distances[current_node][neighbor] < shortest_distance:
                nearest_neighbor = neighbor
                shortest_distance = distances[current_node][neighbor]
        return nearest_neighbor, shortest_distance

    while unvisited:
        current_node = path[-1]
        nearest_neighbor, distance_to_neighbor = find_nearest_neighbor(current_node, unvisited, distances)
        path.append(nearest_neighbor)
        total_distance += distance_to_neighbor
        unvisited.remove(nearest_neighbor)

    # Final step back to the depot
    total_distance += distances[path[-1]][0]
    path.append(0)

    return path, total_distance

path, minimum_distance = nearest_neighbor_tsp(distances)
path, minimum_distance
