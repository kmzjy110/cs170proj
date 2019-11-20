import random
import numpy
def gen_strings(n):
    strings=[]
    nums = list(map(chr, range(48,58)))
    lower = list(map(chr, range(97,123)))
    upper = list(map(chr, range(65,91)))
    strings.extend(nums)
    strings.extend(lower)
    strings.extend(upper)

    i=0
    j=0
    k=0
    while(True):
        while(i<10):
            while(j<26):
                while(k<26):
                    if(len(strings)>=n):
                        strings.sort()
                        return strings[:n]

                    strings.append(nums[i]+lower[j]+upper[k])
                    k+=1
                j+=1
                k=0
            i+=1
            j=0
strings = gen_strings(200)
print(strings)
def gen_homes(n, strings):
    homes = random.choices(strings, k=n)
    homes.sort()
    return homes

homes = gen_homes(100, strings)
print(homes)

def gen_matrix(n):
    percentage = 0.5
    matrix = [[0 for i in range(n)] for i in range(n)]
    i = 0
    while(i<n):
        j=i+1
        matrix[i][i]=0
        while(j<n):
            if(random.uniform(0,1)<percentage):
                ran = get_triangle_inequality_range(matrix,i,j,n)
                if(ran[0]>=ran[1]):
                    continue
                if(ran[1] == float("inf")):
                    ran[1] = 20
                weight = int(round(random.uniform(ran[0], ran[1]),0))
                #weight = round(random.uniform(0.00001, 2000000000),5)
                matrix [i][j] = weight
                matrix [j] [i] = weight
            j+=1

        i+=1
    i=0
    is_connected = check_connected(matrix,n)
    while(not is_connected):
        randi = int(round(random.uniform(0, n-1),0))
        randj= int(round(random.uniform(0, n-1),0))
        while(randj==randi):
            randj=int(round(random.uniform(0, n-1),0))
        weight = round(random.uniform(1, 10), 0)
        matrix [randi] [randj] = weight
        matrix [randj] [randi] = weight
        is_connected=check_connected(matrix,n)


    return matrix
#returns -1 if it satisfies,
def get_triangle_inequality_range(matrix,i,j,n):
    min_val = 0
    max_val = float("inf")
    for y in range(n):
        weight_u = matrix[i][y]
        weight_v = matrix[y][j]
        if(weight_u ==0 or weight_v ==0):
            continue
        min_val = max(min_val, abs(weight_u-weight_v))
        max_val = min(max_val, weight_u+weight_v)

    return [min_val, max_val]


def check_connected(matrix,n):
    k = 0
    numpy_matrix = numpy.asarray(matrix)
    new_matrix = numpy.asarray(matrix)
    while (k <= n):
        new_matrix = numpy.matmul(new_matrix, numpy_matrix)
        k += 1

    is_connected = False
    for i in range(n):
        flag = False
        for j in range(n):
            if new_matrix[i][j] == 0:
                flag = True
                break
        if not flag:
            is_connected = True
            return is_connected
    return is_connected
matrix = gen_matrix(5)
i=0
while(i<5):
    print(matrix[i])
    i+=1