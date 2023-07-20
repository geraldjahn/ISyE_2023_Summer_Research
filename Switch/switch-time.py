import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from munkres import Munkres

def perform_bernoulli_trial(p):
    '''
    Performs a single Bernoulli trial with success probability 'p'.
    Function returns a boolean of the trial's success.
    '''
    return random.random() < p

'''
Simple Packet Switch with size 3, initially empty.
Creates a 3x3 matrix with independent dynamic queues
'''
packetSwitch = np.zeros((3,3))

'''
Independent Variable: Traffic Intensity
* This simulation is setting the service rate to a constant value 1.

Constraints:
    1. the n x n constant matrix with the value lambda must be doubly substochastic. <=> λ <= 1 / 3
    2. the traffic intensity and the derived service rate must have a value between [0, 1).
'''

rho = float(sys.argv[1])    # traffic intensity
lamb = rho / 3              # arrival trial success rate
mu = 1                      # service trial success rate -> here, 1 assumes that it dequeues every phase when the VOQ is not empty.

N = 10000

m = Munkres()
actual_queue = []
size = 0
sample = []

# Simulation
for t in range(N):

    '''
    Arrival: Processed after Passing the Bernoulli trial
    '''
    add = 0
    for x in range(len(packetSwitch)):
        for y in range(len(packetSwitch[x])):
            if perform_bernoulli_trial(lamb):
                # weight of the job is fixed to 1.
                packetSwitch[x][y] += 1
                size += 1
                add += 1

    print(f"\n{add} new jobs were added.")
    print("Current status of the switch is:")   # remove this later
    print(packetSwitch)

    
    '''
    Service: also bernoulli trial
    if not empty, process the Hungarian algorithm to find Max-Weight permutation matrix for selection
    set the packetSwitch of selected VOQs to zero after service
    '''
    if size > 0 and perform_bernoulli_trial(mu):

        print("\nRemoval is proceeded.")

        # returns a list of tuples of the matrix's corrdinates
        maxWeight = m.compute((-1 * packetSwitch))
        print(f"The schedule for phase {t} is {maxWeight}.")

        # Variable saving the weight of chosen schedule (Purpose: eliminates future inefficiencies)
        remWeight = 0

        # removal & update queue length
        for remove in maxWeight:
            remWeight += packetSwitch[remove[0]][remove[1]]
            if packetSwitch[remove[0]][remove[1]] > 0:  # edge case of removing from zeros.
                    packetSwitch[remove[0]][remove[1]] -= 1
                    size -= 1
        print(f"The total weight of jobs chosen in Phase {t}'s schedule is {remWeight}.")
        # Hypothesis: W(t) --> λn

        # Additional Task 1. Compute the total number of non-empty queues 
        filled_queues = packetSwitch[np.where(packetSwitch > 0)]
        print(f"There is/are {filled_queues.size} non-empty queue(s) in the switch in phase {t}.")

        # 2. Compute the maximum sum between the maximum sum of columns and that of rows
        # Hypothesis: C(t) --> ln(n)
        row_sums = np.sum(packetSwitch, axis = 1)
        col_sums = np.sum(packetSwitch, axis = 0)
        max_sum = np.maximum(np.max(row_sums), np.max(col_sums))
        print(f"The maximum axial sum recorded in the matrix in phase {t} is {max_sum}.")

    # Recording Process --> Actual Queue Length
    actual_queue.append(size)

# Overview
print(f"\nWhile the traffic intensity is {rho}, the average queue length for each VOQ is .")
plt.title("Average Queue Length over Time")
plt.plot(range(N), actual_queue)
plt.xlabel("t")
plt.ylabel("μ[q(t)]")
plt.show()