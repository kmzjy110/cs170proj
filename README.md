The two main methods to run are output_gen.py and splitSolver.py.

***For these methods to work you must have all the input files in the folder "inputs", and have the folder "outputs" created.***

**You will need the python libraries 'numpy' and 'disjoint-set'. To do this setup, run:**
```
pip3 install numpy
pip3 install disjoint-set
```

### output_gen.py
For output_gen.py, you can run either a single file or all files in the "inputs" folder.

Single file:
```
python3 output_gen.py 20_50
```
This takes in inputs/20_50.in and puts a solution in outputs/20_50.out. **(Please note that there is no '.in' in the input to output_gen.py!)**

All files:
```
python3 output_gen.py all
```
This parses all the inputs in the 'inputs' folder, and parses solutions for them all into their respective output files in the 'outputs' folder.


### splitSolver.py
splitSolver.py uses multiple threads to split all the files and generate all outputs in a shorter amount of time (this is if you want to do a large portion of the inputs together).

There are three main variables to note in splitSolver.py: left, right, and threads. left and right represent the left and right bounds on the input files array for files to parse. So, splitSolver takes all the files in 'inputs', puts it in a list called onlyfiles, and takes the sublist onlyfiles[left:right] (to do all files, then, left = 0, and right = len(onlyfiles)). threads can be set as well, to the number of processes you want to run concurrently. It will chunk the input list between the threads. To configure all these variables, you must modify splitSolver.py itself, as they aren't args you pass in when running the file.

To ultimately run splitSolver.py, run:
```
python3 splitSolver.py
```