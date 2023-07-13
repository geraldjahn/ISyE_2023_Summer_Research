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
packetSwitch = np.zeros(3,3)

lamb = float(sys.argv[1])   # arrival rate

a = 0.91    # arrival trial success rate
s = 1       # service trial success rate -> here, 1 assumes that it dequeues every phase when the VOQ is not empty
r = a / s   # traffic intensity
N = 100000

m = Munkres()
queue_length = []
size = 0

avg_queue_len = []

# Simulation
for t in range(N):

    '''
    Arrival: Processed after Passing the Bernoulli trial
    '''
    for x in range(len(packetSwitch)):
        for y in range(len(packetSwitch[x])):
            if perform_bernoulli_trial(a):
                # weight of the job is fixed to 1.
                packetSwitch[x][y] += 1
                size += 1

    
    '''
    Service: also bernoulli trial
    if not empty, process the Hungarian algorithm to find Max-Weight permutation matrix for selection
    set the packetSwitch of selected VOQs to zero after service
    '''
    if size > 0 and perform_bernoulli_trial(s):

        # returns a list of tuples of the matrix's corrdinates
        maxWeight = m.compute((-1 * packetSwitch))

        # Variable saving the weight of chosen schedule (Purpose: eliminates future inefficiencies)
        remWeight = 0

        # removal & update queue length
        for remove in maxWeight:
            remWeight += packetSwitch[remove[0]][remove[1]]
            packetSwitch[remove[0]][remove[1]] -= 1
        print("The total weight of jobs chosen in Phase %d's schedule is %d." % (t, remWeight))
        
        # Total number of non-empty queues
        # Maximum sum between maximum sum of columns and that of rows 

    empty_queues, row_sum, col_sum = 0
    for x in range(len(packetSwitch)):
        for y in range(len(packetSwitch[x])):
            if packetSwitch[x][y] == 0:
                print()

    # Recording Process
    queue_length.append(size)
    mean = np.average(queue_length)
    avg_queue_len.append(mean)
    
# Overview
plt.title("Average Queue Length")
plt.plot(range(N), avg_queue_len)
plt.xlabel("t")
plt.ylabel("μ[q(t)]")
plt.show()

    
