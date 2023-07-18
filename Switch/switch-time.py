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

#lamb = float(sys.argv[1])   # arrival rate
lamb = 1 / 6
rho = 1 / 2   # traffic intensity
mu = lamb / rho * 3       # service trial success rate -> here, 1 assumes that it dequeues every phase when the VOQ is not empty

N = 10000

m = Munkres()
queue = []
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

    print(f"{add} new jobs were added.")
    print("Current status of the switch is:")   # remove this later
    print(packetSwitch)

    
    '''
    Service: also bernoulli trial
    if not empty, process the Hungarian algorithm to find Max-Weight permutation matrix for selection
    set the packetSwitch of selected VOQs to zero after service
    '''
    if size > 0 and perform_bernoulli_trial(mu):

        print("removal is proceeded.")

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
        print("The total weight of jobs chosen in Phase %d's schedule is %d." % (t, remWeight))

    # Recording Process
    queue.append(size)
    if t > N / 2:
        sample.append(size)

mean = np.average(sample)
    
    
# Overview
plt.title("Average Queue Length over Time")
plt.plot(range(N), queue)
plt.xlabel("t")
plt.ylabel("μ[q(t)]")
plt.show()