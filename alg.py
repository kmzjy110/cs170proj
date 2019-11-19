""" BRUTE FORCE SOLUTION """
from collections import defaultdict
from heapq import *
import sys
distances = {}
edges = []
def main(locations, homes):
    """
    start is the starting location
    locations will be a list of the strings of the locations
    homes will be a list of the strings of the homes
    distances will be a dictionary mapping tuples of (u, v) to distance value 
    """

    others_vertices = locations[:]
    others_vertices.pop(0)
    current_best = None
    for subset in subsets(others_vertices):
        for path in permutations(subset):
            if valid([start] + path + [start]):
                best_strategy = optimal_dropping(path, homes[:])
                if current_best is None or best_strategy.energy < current_best.energy:
                    current_best = best_strategy

    return current_best

class Tour:
    def __init__(self, path, homes, energy = 0):
        # we also want to keep track of how we drop people off
        self.path = path
        self.homes = homes
        self.energy = energy + float(add_up([start] + path + [start])) * (2/3)

    def __cmp__(self, other):
        return self.energy > other.energy

def valid(path):
    for i in range(1, len(path)):
        if distances[(path[i - 1], path[i])] is None:
            return False
    return True


def optimal_dropping(path, remaining_homes):
    """ Calculate the optimal dropping through more brute force """
    if not path:
        homes_dropped = {}
        if remaining_homes:
            homes_dropped[start] = remaining_homes
        return Tour(path, homes_dropped, sum([distance(start, home) for home in remaining_homes]))

    best_tour = None
    location = path[0]
    for homes_sent in subsets(remaining_homes):
        energy_used = sum([distance(location, home) for home in homes_sent])
        homes_available = [home for home in remaining_homes if home not in homes_sent]
        recursed_tour = optimal_dropping(path[1:], homes_available)
        if recursed_tour is not None:
            homes_dropped = recursed_tour.homes
            if homes_sent:
                homes_dropped[location] = homes_sent
            min_energy = energy_used + recursed_tour.energy
            if best_tour is None or min_energy < best_tour.energy:
                best_tour = Tour(path, homes_dropped, min_energy)
    
    return best_tour

def distance(f, t):
    """ Run Dijsktra's to find the minimum distance from the start to the end """
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: 
                return cost

            for c, v2 in g.get(v1, ()):
                if v2 in seen: 
                    continue
                prev = mins.get(v2, None)
                next_val = cost + c
                if prev is None or next_val < prev:
                    mins[v2] = next_val
                    heappush(q, (next_val, v2, path))

    return float("inf")

def add_up(path):
    if len(path) <= 1:
        return 0
    return distances[(path[0], path[1])] + add_up(path[1:])

def subsets(lst):
    """Yield all subsets of the given lst"""
    if not lst:
        yield lst
    else:
        for x in subsets(lst[1:]):
            yield x
            yield [lst[0]] + x

def permutations(lst):
    if len(lst) <= 1:
        yield lst
        return
    for p in permutations(lst[1:]):
        for i in range(len(p)):
            yield p[:i] + [lst[0]] + p[i:]

if __name__ == "__main__":
    global start
    locations = "Soda Dwinelle Wheeler Campanile Cory RSF Barrows".split()         # input("Enter Locations\n").split()
    homes = "Wheeler Campanile Cory RSF".split()                                    # input("Enter Homes\n").split()
    start = "Soda"                                                                 # input("Enter Start\n")
    distances = {}
    matrix = ["x1x1xx1", "1xx1xxx", "xxx1xxx", "111x111", "xxx1xxx", "xxx1xxx", "1xx1xxx"]
    for x, s in enumerate(locations):
        for y, end in enumerate(locations):
            val = matrix[x][y]
            if s == end:
                edges.append((s, end, 0))
                distances[(s, end)] = 0
            elif val == 'x':
                edges.append((s, end, sys.maxsize))
                distances[(s, end)] = None
            else:
                val = int(val)
                edges.append((s, end, val))
                distances[(s, end)] = val
    answer = main(locations, homes)
    print("answer:", answer.path, "; energy:", answer.energy, "; homes sent:", answer.homes)
    