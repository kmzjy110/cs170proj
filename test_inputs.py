from input_generation import gen_matrix, gen_strings, gen_homes

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
                    if not isinstance(matrix[i][k], str) and not isinstance(matrix[k][j], str):
                        assert matrix[i][k] + matrix[k][j] >= matrix[i][j], "triangle inequality: " + str(matrix[i][k]) + " " + str(matrix[k][j]) + " >= " + str(matrix[i][j])

    #i, i must always be 'x'
    assert all([matrix[i][i] == 'x' for i in range(len(matrix))]), "Diagonal not x filled"


    
        
if __name__ == "__main__":
    global start
    locations = gen_strings(50)
    homes = gen_homes(25, locations)
    start = locations[0]                                                                 # input("Enter Start\n")
    distances = {}
    matrix = gen_matrix(50)
    test_inputs(homes, locations, start, matrix)