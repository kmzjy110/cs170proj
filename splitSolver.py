
from os import listdir
from os.path import isfile, join
from multiprocessing import Pool
from output_gen import gen_output

onlyfiles = [f for f in listdir('inputs/') if isfile(join('inputs/', f))]
onlyfiles.sort()
numfiles = len(onlyfiles)

def solveAll(file):
    gen_output(file)

poolObj = Pool(processes=50)
poolObj.map(solveAll, [filename.split('.')[0] for filename in onlyfiles])