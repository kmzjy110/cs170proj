import sys
sys.path.append('..')
sys.path.append('../..')
import os
import argparse
import utils
import networkx as nx
import numpy as np
from student_utils import *
import output_validator


def gen_output(input_file):
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    file = open('200.out','w') 
    file.write(str(starting_car_location) + '\n')
    file.write(str(1)  + '\n')
    file.write(str(starting_car_location) + ' ')
    for loc in list_houses[:len(list_houses)-1]:
        file.write(loc + ' ')
    file.write(list_houses[len(list_houses)-1] + '\n')
    file.close()

def all_pairs_shortest_path (adjacency, num_locations):
    dist = [[[0 for k in range(num_locations)] for j in range(num_locations)    ] for i in range(num_locations +1)]
    for i in range(num_locations):
        for j in range(num_locations):
            if(adjacency[i][j]=='x'):
                dist[0][i][j] = float("inf")
            else:
                dist[0][i][j] = adjacency[i][j]
    for k in range(1, num_locations + 1):
        for i in range(num_locations):
            for j in range(num_locations):
                dist[k][i][j] = min(dist[k-1][i][k]+ dist [k-1][k][j], dist[k-1][i][j])

    return dist[num_locations]






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the input validator is run on all files in the input directory. Else, it is run on just the given input file.')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    input_file = args.input
    gen_output(input_file)
    output_validator.validate_output(input_file, '200.out')