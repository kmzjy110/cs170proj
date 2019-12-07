from itertools import product
from sys import stdout as out
from mip import Model, xsum, BINARY, minimize, ConstrsGenerator, CutPool, INTEGER
from student_utils import *
from networkx.algorithms import number_strongly_connected_components
import networkx as nx

# # names of places to visit
# places = ['Antwerp', 'Bruges', 'C-Mine', 'Dinant', 'Ghent',
#           'Grand-Place de Bruxelles', 'Hasselt', 'Leuven',
#           'Mechelen', 'Mons', 'Montagne de Bueren', 'Namur',
#           'Remouchamps', 'Waterloo']

# # distances in an upper triangular matrix
# dists = [[83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57],
#          [161, 160, 39, 89, 151, 110, 90, 99, 177, 143, 193, 100],
#          [90, 125, 82, 13, 57, 71, 123, 38, 72, 59, 82],
#          [123, 77, 81, 71, 91, 72, 64, 24, 62, 63],
#          [51, 114, 72, 54, 69, 139, 105, 155, 62],
#          [70, 25, 22, 52, 90, 56, 105, 16],
#          [45, 61, 111, 36, 61, 57, 70],
#          [23, 71, 67, 48, 85, 29],
#          [74, 89, 69, 107, 36],
#          [117, 65, 125, 43],
#          [54, 22, 84],
#          [60, 44],
#          [97],
#          []]

# def genSol(x, startingloc):
#     validEdges = [[1 if x[i][j] >= 0.99 else 0 for j in range(len(x[i]))] for i in range(len(x))]
#     visitedEdges = set()
#     path = []
#     currloc = startingloc
#     while sum([sum(row) for row in validEdges]) > 0:
#         possibilities = 
#         for j in range(validEdges[currloc]):
#             if validEdges[i][j] == 1:

def custom_adjacency_matrix_to_graph(adjacency_matrix):
    node_weights = [adjacency_matrix[i][i] for i in range(len(adjacency_matrix))]
    adjacency_matrix_formatted = [[0 if entry == 'x' else entry for entry in row] for row in adjacency_matrix]

    for i in range(len(adjacency_matrix_formatted)):
        adjacency_matrix_formatted[i][i] = 0

    # print(adjacency_matrix_formatted)

    G = nx.convert_matrix.from_numpy_matrix(np.matrix(adjacency_matrix_formatted), create_using=nx.DiGraph())

    message = ''

    for node, datadict in G.nodes.items():
        if node_weights[node] != 'x':
            message += 'The location {} has a road to itself. This is not allowed.\n'.format(node)
        datadict['weight'] = node_weights[node]

    return G, message

class SubTourCutGenerator(ConstrsGenerator):
    """Class to generate cutting planes for the TSP"""
    def __init__(self, x_, locations_):
        # print(x_)
        # print(locations_)
        self.x = x_
        self.locations = locations_

    def generate_constrs(self, model: Model):
        adj_matrix = [[self.x[i][j].x if self.x[i][j].x is not None else 0 for j in self.locations] for i in self.locations]
        # print(adj_matrix)
        graph, adj_message = custom_adjacency_matrix_to_graph(adj_matrix)
        print("sccs")
        print(number_strongly_connected_components(graph))
        model += number_strongly_connected_components(graph) == 1

# # number of nodes and list of vertices
# n, V = len(dists), set(range(len(dists)))
def solve(input_data):
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)

    graph, adj_message = adjacency_matrix_to_graph(adjacency_matrix)
    # print(adj_message)
    shortest = dict(nx.floyd_warshall(graph))
    # print(shortest)

    model = Model(solver_name='GRB')

    locations = range(num_of_locations)
    houses = range(num_houses)

    starting_car_num = 0
    for i in range(len(locations)):
        if list_locations[i] == starting_car_location:
            starting_car_num = i

    edges = [(i, j) for j in locations for i in locations]

    # binary variables indicating if arc (i,j) is used on the route or not
    x = [[model.add_var(var_type=BINARY) for j in locations] for i in locations]

    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [model.add_var(var_type=INTEGER) for i in locations]

    z = [[model.add_var(var_type=BINARY) for i in locations] for k in houses]

    f = [[model.add_var(var_type=BINARY) for j in locations] for i in locations]

    # objective function: minimize the distance
    # for i,j in edges:
    #     print(adjacency_matrix[i][j])
    obj1 = xsum(adjacency_matrix[i][j]*(2/3)*x[i][j] for i, j in edges if adjacency_matrix[i][j] != 'x')
    obj2 = xsum(z[k][i]*shortest[houses[k]][locations[i]] for i in locations for k in houses)
    model.objective = minimize(obj1 + obj2)

    # constraint : leave each city only once
    for l in locations:
        model += xsum(x[i][j] for i, j in edges if i == l)  == y[l]

    # constraint : enter each city only once
    for l in locations:
        model += xsum(x[i][j] for i, j in edges if j==l) == y[l]

    # for l in locations:
    #     model += y[l] <= 2 #########

    for h in houses:
        model += xsum(z[h][l] for l in locations) == 1

    # for h in houses:
    #     for l in locations:
    #         model += z[h][l] <= 1

    for i in locations:
        for j in locations:
            model += x[i][j] <= 1
            model += f[i][j] >= x[i][j]
            model += f[i][j] == x[i][j]

    for l in locations:
        model += xsum(f[i][l] for i in locations) == xsum(f[l][i] for i in locations)

    for i in locations:
        for h in houses:
            model += z[h][i] <= y[i]

    model += xsum(x[starting_car_num][j] for j in locations) >= 1
    model += xsum(f[starting_car_num][j] for j in locations) == 4 * len(locations) * len(locations)
    model += xsum(f[j][starting_car_num] for j in locations) == 4 * len(locations) * len(locations)

    for i in range(len(x)):
        for j in range(len(x[i])):
            if adjacency_matrix[i][j] == 'x':
                model += x[i][j] == 0
                model += f[i][j] == 0

    # model.lazy_constrs_generator = SubTourCutGenerator(x, locations)

    model.optimize(max_seconds=30)

    # checking if a solution was found
    if model.num_solutions:
        out.write('route with total distance %g found: %s'
                % (model.objective_value, list_locations[starting_car_num]))
        currloc = starting_car_num
        nc = 0
        print([[str(i) + ' ' + str(j) + ' ' + str(x[i][j].x) for j in range(len(x[i])) if x[i][j].x != 0] for i in range(len(x))])
        print([[str(k) + ' ' + str(i) + ' ' + str(z[k][i].x) for i in locations if z[k][i].x != 0] for k in houses])
        # for j in x[currloc]:

        out.write('\n')
