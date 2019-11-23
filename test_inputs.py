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
                    if matrix[i][k]!='x' and matrix[k][j] != 'x':
                        assert matrix[i][k] + matrix[k][j] > matrix[i][j], "triangle inequality: " + str(matrix[i][k]) + " " + str(matrix[k][j]) + " >= " + str(matrix[i][j])

    #i, i must always be 'x'
    assert all([matrix[i][i] == 'x' for i in range(len(matrix))]), "Diagonal not x filled"


    
        
if __name__ == "__main__":
    global start
    loc_size = 50
    home_size = 25
    locations = gen_strings(loc_size)
    homes = gen_homes(home_size, locations)
    start = locations[0]                                                                 # input("Enter Start\n")
    distances = {}
    matrix = gen_matrix(loc_size)
    test_inputs(homes, locations, start, matrix)
    print(len(locations))
    print(len(homes))
    for l in locations:
        print(l,end=" ")
    print("")
    for h in homes:
        print(h,end=" ")
    print("")
    print(locations[0])
    for line in matrix:
        for el in line:
            print(el, end=" ")
        print("")
