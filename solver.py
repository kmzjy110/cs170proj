import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from networkx.algorithms import approximation
# from wqu import *
from student_utils import *
from disjoint_set import DisjointSet
"""
======================================================================
  Complete the following function.
======================================================================
"""

# Given the steiner tree, return a path that traverses all the edges twice
# Similar to MST idea from travelling salesman
def make_path_of(tree, graph, starting_car_location):
    
    edges = list(nx.dfs_edges(tree, source = starting_car_location))
    
    shortest_edges = dict(nx.algorithms.shortest_paths.all_pairs_shortest_path(graph))
    first = edges.pop(0)
    answer = [first[0], first[1]]
    for edge in edges:
        if answer[-1] != edge[0]:
            path = shortest_edges[answer[-1]][edge[1]]
            answer.extend(path[1:-1])
        answer.append(edge[1])
    get_back_to_home = shortest_edges[answer[-1]][answer[0]]
    return answer + get_back_to_home[1:]
    

# OPTIMAL POINT 
def optimal_point(clusters, shortest):
    """ Given a list of clusters, return a list where element i denotes the shortest path to the end 
    >>> optimal_point([]
    """
    answer = []
    for cluster in clusters:
        answer.append(min([point for point in cluster], key = lambda point: sum([shortest[point][other] for other in cluster])))
    return answer


def greedy_clusters(graph, homes, homes_to_index, shortest, k):
    """ We will return the solution for all values of k """

    # Create all pairs of homes
    pairs = []
    for i in range(len(homes)):
        for j in range(i + 1, len(homes)):
            pairs.append((i, j))
    
    # Sort the pairs
    pairs = sorted(pairs, key = lambda pair: shortest[homes_to_index[homes[pair[0]]]][homes_to_index[homes[pair[1]]]])

    # Create a WQU for clustering
    quick_union = DisjointSet()
    for i in range(len(homes)):
        quick_union.find(i)

    # print(list(quick_union.itersets()))
    # Greedy combine pairs together until all the homes are together
    while len(list(quick_union.itersets())) > k:
        curr = pairs.pop(0)
        quick_union.union(curr[0], curr[1])

    
    # map home to the cluster that it is in
    home_to_cluster = {}
    cluster_index_homes = list(quick_union.itersets())
    clusters_answer = []

    # We just want to move from indices back to homes
    for lst in cluster_index_homes:
        new_lst = []
        for i in lst:
            new_lst.append(homes_to_index[homes[i]])
            home_to_cluster[homes[i]] = new_lst
        clusters_answer.append(new_lst)

    # Now with these cluster_homes, we can add to all the surrounding neighbors 
    # We look at each node, and then we add the node to the cluster of its nearest home
    vals = list(homes_to_index.values())
    for node in graph.nodes:
        if node not in vals: #if it is not a home
            closest_home = min(homes, key = lambda home: shortest[homes_to_index[home]][node])
            home_to_cluster[closest_home].append(node)

    return clusters_answer
    

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

    homes_to_index = {home: list_of_locations.index(home) for home in list_of_homes}
    start = list_of_locations.index(starting_car_location)

    # 0. SET UP GRAPH
    graph, adj_message = adjacency_matrix_to_graph(adjacency_matrix)
    shortest = dict(nx.floyd_warshall(graph))


    potential_answers = []
    for k in range(1, len(list_of_homes)):
        # 1. CLUSTER
        print(k)
        clusters = greedy_clusters(graph, list_of_homes, homes_to_index, shortest, k)
        values = homes_to_index.values()
        assert all([any([val in cluster for val in values]) for cluster in clusters]), "Greedy clusters failed"

        # 2. FIND OPTIMAL POINTS
        # print(len(clusters))
        # print(clusters)
        optimal_points = optimal_point(clusters, shortest)

        assert all([optimal_points[i] in clusters[i] for i in range(len(optimal_points))]), "Optimal point failed"

        # 3. APPROXIMATE PATH THROUGH OPTIMAL POINTS
        # print(list_of_locations)
        # print(terminal_nodes)

        terminal_nodes = optimal_points + [start]
        if len(optimal_points) == 1 and optimal_points[0] == start:
            path_to_go = [start]
        else:
            steiner_tree = nx.algorithms.approximation.steinertree.steiner_tree(graph, terminal_nodes)

            path_to_go = make_path_of(steiner_tree, graph, start)

        # 4. CREATE ANSWER DICTIONARY
        final_map = {optimal_point: [x for x in cluster if x in values] for optimal_point, cluster in zip(optimal_points, clusters)}

        # print(path_to_go)
        # print(final_map)
    
    #DROPPING PEOPLE OFF?
        potential_answers.append([path_to_go, final_map])

    print('finding best answer')
    #drop all at start
    # path_to_go = [starting_car_location]
    # dropoff_mapping = {}

    answer = min(potential_answers, key = lambda answer: cost_of_solution(graph, answer[0], answer[1]))
    return answer[0], answer[1]


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
