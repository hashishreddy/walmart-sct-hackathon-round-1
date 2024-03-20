import pandas as pd
from io import StringIO
import numpy as np


data_new = pd.read_csv(r"D:\Walmart_Bits_Pilani\part_b_input_dataset_2.csv")

depot_new = pd.DataFrame({'order_id': [0], 'lng': [data_new['depot_lng'].iloc[0]], 'lat': [data_new['depot_lat'].iloc[0]]})
data_new = pd.concat([depot_new, data_new[['lng', 'lat']]]).reset_index(drop=True)

distances_new = np.zeros((data_new.shape[0], data_new.shape[0]))
for i in range(data_new.shape[0]):
    for j in range(data_new.shape[0]):
        distances_new[i][j] = haversine(data_new.loc[i, 'lng'], data_new.loc[i, 'lat'], data_new.loc[j, 'lng'], data_new.loc[j, 'lat'])

def calculate_total_distance(path, distances):
    return sum(distances[path[i]][path[i+1]] for i in range(len(path) - 1))

def split_path_for_two_drivers(path, distances):
    split_index = len(path) // 2
    path_driver_1 = path[:split_index]
    path_driver_2 = path[split_index-1:] 

    if path_driver_1[-1] != 0:
        path_driver_1.append(0)
    if path_driver_2[-1] != 0:
        path_driver_2.append(0)

    distance_driver_1 = calculate_total_distance(path_driver_1, distances)
    distance_driver_2 = calculate_total_distance(path_driver_2, distances)

    return path_driver_1, distance_driver_1, path_driver_2, distance_driver_2

path_new, _ = nearest_neighbor_tsp(distances_new)

path_driver_1, distance_driver_1, path_driver_2, distance_driver_2 = split_path_for_two_drivers(path_new, distances_new)

path_driver_1, distance_driver_1, path_driver_2, distance_driver_2
