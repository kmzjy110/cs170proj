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
def make_path_of(tree, graph, starting_car_location, shortest_edges):
    
    edges = list(nx.dfs_edges(tree, source = starting_car_location))
    
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

def cost(tour):
    return sum([shortest[tour[i]][tour[i + 1]] for i in range(len(tour) - 1)])
    
def local_search(tour, shortest):
    """optimize finding an efficient tour """
    times = 0
    while True:
        choices = list(possibilities(tour, shortest))
        times += 1
        if not choices:
            break
        possible = min(choices, key = cost)
        if cost(possible) + 1 > cost(tour):
            break
        tour = possible

    return tour
 
def squash(lst):
    answer = []
    for x in lst:
        answer.append(x[0])
    answer.append(lst[-1][1])
    return answer

def possibilities(tour, shortest):
    """ Return all potentials solution in the neighborhood of the tour """
    edges = [[tour[i], tour[i + 1]] for i in range(len(tour) - 1)]

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            for k in range(j + 1, len(edges)):
                
                possibility = [edges[d] for d in range(len(edges)) if d != i and d != k and d != j]
                #print(edges[i], edges[j], edges[k])
                vertices = edges[i] + edges[j] + edges[k]
                #print("Vertex", vertices)
                for permutation in matchings(vertices):
                    if is_valid(permutation):
                        #print("perm", permutation)
                        f = reorder(possibility + [[permutation[i], permutation[i + 1]] for i in [0, 2, 4]])
                        if f:
                            #print('squashed', f, tour)
                            yield squash(f)

def reorder(pairs):
    """ Given a list of pairs, reorder them such that adjacent pairs go in order """
    #print("re", pairs)
    answer = [pairs.pop(0)]
    while pairs:
        i = 0
        try:
            while pairs[i][0] != answer[-1][1] and pairs[i][1] != answer[-1][1]:
                i += 1
            curr = pairs.pop(i)
            if curr[0] == answer[-1][1]:
                answer.append(curr[:])
            else:
                answer.append([curr[1], curr[0]])
        except IndexError:
            return False
    return answer

def matchings(vertices):
    if len(vertices) == 2:
        yield vertices
        return
    first = vertices.pop()
    for i in range(len(vertices)):
        call = vertices[:]
        pair = [call.pop(i), first]
        for answer in matchings(call):
            yield answer + pair            
    

def extrapolate_tour(tour):
    edges = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]
    answer = []
    for edge in edges:
        answer.extend(shortest_edges[edge[0]][edge[1]][:-1])
    return answer + shortest_edges[tour[-1]][tour[0]][:-1]

def is_valid(lst):
    # print("checking validy of " + str(lst))
    if lst[1] == lst[2] and lst[0] == lst[3]:
        return False
    if lst[0] == lst[5] and lst[1] == lst[4]:
        return False
    if lst[2] == lst[5] and lst[3] == lst[4]:
        return False

    if lst[0] == lst[2] and lst[1] == lst[3]:
        return False
    if lst[1] == lst[5] and lst[0] == lst[4]:
        return False
    if lst[3] == lst[5] and lst[2] == lst[4]:
        return False

    return all([lst[i] != lst[i + 1] for i in [0, 2, 4]]) and len(set(lst)) > 3

def naive_order(homes):
    answer = [homes.pop(0)]
    while homes:
        closest_index = min(range(len(homes)), key = lambda i: shortest[answer[-1]][homes[i]])
        answer.append(homes.pop(closest_index))
    return answer



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
    global shortest
    shortest = dict(nx.floyd_warshall(graph))
    global shortest_edges
    shortest_edges = dict(nx.algorithms.shortest_paths.all_pairs_shortest_path(graph))
    
    values = homes_to_index.values()



    potential_answers, my = [], []
    for k in range(1, len(list_of_homes)):
        # 1. CLUSTER
        print(k)
        clusters = greedy_clusters(graph, list_of_homes, homes_to_index, shortest, k)
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

            path_to_go = make_path_of(steiner_tree, graph, start, shortest_edges)


            if k >= 2:
                naive_ordering = naive_order(list(optimal_points)) 
                # print(naive_ordering)
                naive_ordering += [naive_ordering[0]]
                only_opt = extrapolate_tour(local_search(naive_ordering + [naive_ordering[0]], shortest))

                assert all([graph.has_edge(only_opt[i], only_opt[i + 1]) for i in range(len(only_opt) - 1)]), str([graph.has_edge(only_opt[i], only_opt[i + 1]) for i in range(len(only_opt) - 1)])

                opt_i = min(range(len(only_opt)), key = lambda i: shortest[only_opt[i]][start])
                if start not in only_opt:
                    # print('before', only_opt)
                    only_opt = shortest_edges[start][only_opt[opt_i]][:-1] + only_opt[opt_i:] + only_opt[:opt_i] + shortest_edges[only_opt[opt_i]][start]
                    # print(start, only_opt)
                else:
                    p = only_opt.index(start)
                    only_opt = only_opt[p:] + only_opt[:p + 1]
                assert all([graph.has_edge(only_opt[i], only_opt[i + 1]) for i in range(len(only_opt) - 1)]), str([graph.has_edge(only_opt[i], only_opt[i + 1]) for i in range(len(only_opt) - 1)])

                
                if cost(path_to_go) > cost(only_opt):
                    # print("WE BETTER", only_opt)
                    path_to_go = only_opt
                
        

        # if k:
        #     print("________________")
        #     print("PAth", path_to_go)
        #     normal_path = local_search(path_to_go, shortest)
        #     print(normal_path)
        #     if cost(path_to_go) > cost(normal_path):
        #         print("Nomral BETTER")
        #         path_to_go = normal_path
            


        # 4. CREATE ANSWER DICTIONARY
        final_map = {optimal_point: [x for x in cluster if x in values] for optimal_point, cluster in zip(optimal_points, clusters)}

        # print(path_to_go)
        # print(final_map)
    
    #DROPPING PEOPLE OFF?
        potential_answers.append([path_to_go, final_map])

    potential_answers.append(([start], {start: values}))

    print('finding best answer')
    #drop all at start
    # path_to_go = [starting_car_location]
    # dropoff_mapping = {}

    answer_index = min(list(range(len(potential_answers))), key = lambda i: cost_of_solution(graph, potential_answers[i][0], potential_answers[i][1])[0])
    print("K VALUE: ", answer_index)
    answer = potential_answers[answer_index]
    print(cost_of_solution(graph, answer[0], answer[1]))
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
