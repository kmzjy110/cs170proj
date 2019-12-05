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
from solver import solve, convertToFile
from os import listdir
from os.path import isfile, join
from multiprocessing import Pool

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def gen_output(input_file):
    if input_file != 'all':
        inputfilename = 'inputs/' + input_file + '.in'
        outputfilename = 'outputs/' + input_file + '.out'
        input_data = utils.read_file(inputfilename)
        num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
        path, dropoff_mapping = solve(list_locations, list_houses, starting_car_location, adjacency_matrix)
        convertToFile(path, dropoff_mapping, outputfilename, list_locations)
        # file = open('200.out','w') 
        # file.write(str(starting_car_location) + '\n')
        # file.write(str(1)  + '\n')
        # file.write(str(starting_car_location) + ' ')
        # for loc in list_houses[:len(list_houses)-1]:
        #     file.write(loc + ' ')
        # file.write(list_houses[len(list_houses)-1] + '\n')
        # file.close()
        output_validator.validate_output(inputfilename, outputfilename)
    else:
        onlyfiles = [f for f in listdir('inputs/') if isfile(join('inputs/', f))]
        onlyfiles.sort()
        numfiles = len(onlyfiles)
        counter = 1
        for fl in onlyfiles:
            print('progress: ' + str(counter) + ' out of ' + str(numfiles))
            inputfilename = 'inputs/' + fl
            outputfilename = 'outputs/' + fl.split('.')[0] + '.out'
            input_data = utils.read_file(inputfilename)
            if file_len(outputfilename) != 3:
                print("skipped")
                counter += 1
            else:
                num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
                print(inputfilename + ' file parsed')
                path, dropoff_mapping = solve(list_locations, list_houses, starting_car_location, adjacency_matrix)
                print('converting to file')
                convertToFile(path, dropoff_mapping, outputfilename, list_locations)
                output_validator.validate_output(inputfilename, outputfilename)
                counter += 1


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