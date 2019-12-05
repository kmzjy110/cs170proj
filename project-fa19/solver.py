import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

# Given the steiner tree, return a path that traverses all the edges twice
# Similar to MST idea from travelling salesman
def make_path_of(tree):
    pass

# OPTIMAL POINT 
def optimal_point(clusters):
    """ Given a list of clusters, return a list where element i denotes the shortest path to the end 
    >>> optimal_point([]
    """
    answer = []
    for cluster in clusters:
        answer.append(min([point for point in cluster], key = lambda point: sum([shortest[point][other] for other in cluster])))
    return answer

#K partition
def partition(graph, k, shortest_paths):
    nodes = list(graph.nodes)
    partition_centers = [nodes[0]]
    clusters  = [[] for i in range(k)]
    for i in range(k-1):
        max_distance = 0
        max_center = -1
        for j in nodes:
            total_distance = 0
            for x in partition_centers:
                total_distance += shortest_paths[j][x]
            if total_distance>max_distance:
                max_center = j
        partition_centers.append(max_center)
    for j in nodes:
        min_distance = float("inf")
        min_center_index = 0
        for i in range(k):
            if shortest_paths[j][partition_centers[i]]<min_distance:
                min_distance = shortest_paths[j][partition_centers[i]]
                min_center_index=i
        clusters[min_center_index].append(j)
    return clusters

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """


    """
    Clustering Algorithm:

    Clustering
        We will use the following approximation algorithm to partition the homes into the m clusters. 
        A cluster is a set of nearby locations from where one dropoff will occur.
        Set m to zero. 
        Keep incrementing m by one until the maximum average distance between points 
        within clusters is less than h, where h is some predetermined heuristic value. 
        We will call k-CLUSTER from the textbook to cluster the homes, setting k to m. 
    Optimal Point
        Next, within each cluster, we will find the optimal access point — where we will drop off
        all the people who have homes. 
        To solve the optimal access point problem, we will use the Floyd-Warshall ALL-PAIRS 
        algorithm from the textbook to compute the shortest path between any two points. 
        We will then iterate through all the points to find the point with the minimum distance 
        to each home. 
    Steiner Tree
        Finally, using the optimal access points calculated above, 
        we can create a steiner tree and run that
    Optimization
        We can potentially optimize the return path from the steiner tree by taking the shortest path
        between adjacent homes if such a path is available.  

    """

    # 0. SET UP GRAPH
    graph = adjacency_matrix_to_graph(adjacency_matrix)
    edge_list = adjacency_matrix_to_edge_list(adjacency_matrix)
    shortest = dict(nx.floyd_warshall(graph))

    # 1. CLUSTER
    clusters = partition(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, k, shortest)

    # 2. FIND OPTIMAL POINTS
    optimal_points = optimal_point(clusters)

    # 3. APPROXIMATE PATH THROUGH OPTIMAL POINTS
    steiner_tree = nx.steiner_tree(graph, optimal_points)
    nx.s
    path_to_go = make_path_of(steiner_tree)

    # 4. CREATE ANSWER DICTIONARY
    final_map = {optimal_point: cluster for optimal_point, cluster in zip(optimal_points, clusters)}

    return path_to_go, final_map


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
