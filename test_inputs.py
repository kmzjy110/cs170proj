from input_generation import gen_matrix, gen_strings, gen_homes
from staff_test import *

def test_inputs(homes, locations, start, matrix):
    """We will create tests to test the legitimacy of the inputs """

    # TEST HOMES IS SUBSET 
    assert all([x in locations for x in homes]), "not all the homes are in locations"

    # TEST SYMMETRY
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            assert matrix[i][j] == matrix[j][i], "the matrix is not symmetric"
            if not isinstance(matrix[i][j], str):
                for k in range(len(matrix)):
                    if matrix[i][k]!='x' and matrix[k][j] != 'x':
                        assert matrix[i][k] + matrix[k][j] > matrix[i][j], "triangle inequality: " + str(matrix[i][k]) + " " + str(matrix[k][j]) + " >= " + str(matrix[i][j])

    #i, i must always be 'x'
    assert all([matrix[i][i] == 'x' for i in range(len(matrix))]), "Diagonal not x filled"


    
        
if __name__ == "__main__":
    global start
    loc_size = 200
    home_size = 169
    locations = gen_strings(loc_size)
    homes = gen_homes(home_size, locations)
    start = locations[0]                                                                 # input("Enter Start\n")
    distances = {}
    matrix = gen_matrix(loc_size)
    file = open('200.in','w') 
    file.write(str(len(locations)) + '\n')
    file.write(str(len(homes)) + '\n')
    for l in locations:
        file.write(str(l) + " ")
    file.write('\n')
    for h in homes:
        file.write(str(h)+ " ")
    file.write('\n')
    file.write(str(locations[0]))
    file.write('\n')
    for line in matrix:
        for el in line:
            file.write(str(el) + " ")
        file.write('\n')
    file.close()
    while (validate_input('100.in')):
        matrix = gen_matrix(loc_size)
        file = open('100.in','w') 
        file.write(str(len(locations)) + '\n')
        file.write(str(len(homes)) + '\n')
        for l in locations:
            file.write(str(l) + " ")
        file.write('\n')
        for h in homes:
            file.write(str(h)+ " ")
        file.write('\n')
        file.write(str(locations[0]))
        file.write('\n')
        for line in matrix:
            for el in line:
                file.write(str(el) + " ")
            file.write('\n')
        file.close()
    test_inputs(homes, locations, start, matrix)