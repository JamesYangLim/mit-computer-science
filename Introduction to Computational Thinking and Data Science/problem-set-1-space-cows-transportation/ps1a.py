###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
from collections import OrderedDict
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = {}
    with open(filename, 'r') as f:
        for line in f:
            cow = line.split(',')
            assert(len(cow) == 2)
            assert(cows.get(cow[0]) == None)
            cows[cow[0]] = int(cow[1])
    f.close()
    return cows    


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    overall_trips = []
    ordered_cows = OrderedDict(sorted(cows.items(), key=lambda t: t[1]))
    while(len(ordered_cows) is not 0):
        trip = []
        weight_per_trip = 0
        for cow in reversed(ordered_cows):
            w = ordered_cows.get(cow)
            temp_w = weight_per_trip + w
            if temp_w <= limit:
                weight_per_trip = temp_w
                trip.append(cow)
                ordered_cows.popitem(cow)
        overall_trips.append(trip)
    return overall_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    for p in get_partitions(cows):
        partition_within_limit = True
        for c in p:
            weight_per_cell = 0
            for cow in c:
                weight_per_cell += cows.get(cow)
            if limit < weight_per_cell:
                partition_within_limit = False
                break
        if partition_within_limit:
            return p
    return []
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    filename = 'ps1_cow_data.txt'
    cows = load_cows(filename)

    start = time.time()
    overall_trips = greedy_cow_transport(cows)
    end = time.time()
    print('greedy_cow_transport took ', (end - start) * 1000, ' ms')
    print('greedy_cow_transport produce ', len(overall_trips), ' trips')

    start = time.time()
    overall_trips = brute_force_cow_transport(cows)
    end = time.time()
    print('brute_force_cow_transport took ', (end - start) * 1000, ' ms')
    print('brute_force_cow_transport produce ', len(overall_trips), ' trips')

if __name__ == '__main__':
    compare_cow_transport_algorithms()


#################################
# Problem A.5: Writeup
#################################

# 1. What were your results from compare_cow_transport_algorithms? Which
# algorithm runs faster? Why?
# Greedy algorithm runs roughly 20 times faster as it pick the highest weighted cow 
# first and the second highest weighted cow and so on. Meanwhile brute force algorithm 
# tries all possible combinations and find the combination that fit in 1 trip.


# 2. Does the greedy algorithm return the optimal solution? Why/why not?
# Not all the time greedy algorithm will return the optimal solution as it only picks
# what is best based on its current situation.

# 3. Does the brute force algorithm return the optimal solution? Why/why not?
# I can return the optimal solution as it tries out all the possible combition.