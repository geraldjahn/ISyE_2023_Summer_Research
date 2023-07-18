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

lamb = float(sys.argv[1])    # arrival trial success rate
N = 10000

m = Munkres()
traf = []
qlen = []

# Simulation
for rho in np.arange(0.9, 1.0, 0.01):   # rho: traffic intensity, noted as (ρ).
    mu = lamb / rho                     # service trial success rate -> here, 1 assumes that it dequeues every phase when the VOQ is not empty
    size = 0
    queue_length = []
    sample = []
    traf.append(rho)

    '''
    Simple Packet Switch with size 3, initially empty.
    Creates a 3x3 matrix with independent dynamic queues
    '''
    packetSwitch = np.zeros((3, 3))

    for t in range(N):
        '''
        Arrival: Processed after Passing the Bernoulli trial
        '''
        for x in range(len(packetSwitch)):
            for y in range(len(packetSwitch[x])):
                if perform_bernoulli_trial(lamb):
                    # weight of the job is fixed to 1.
                    packetSwitch[x][y] += 1
                    size += 1

        # Checking the status of the switch after arrival
        '''print("Current status of the switch is:")   # remove this later
        print(packetSwitch)'''

        # Additional Tasks
        # 1. Compute the total number of non-empty queues 
        '''empty_queues = packetSwitch[np.where(packetSwitch == 0)]
        print(f"There is/are {empty_queues.size} empty queue(s) in the switch in phase {t}.")'''

        # 2. Compute the maximum sum between the maximum sum of columns and that of rows
        '''row_sums = np.sum(packetSwitch, axis = 1)
        col_sums = np.sum(packetSwitch, axis = 0)
        max_sum = np.maximum(np.max(row_sums), np.max(col_sums))
        print(f"The maximum axial sum recorded in the matrix in phase {t} is {max_sum}.")'''

        '''
        Service: also bernoulli trial
        if not empty, process the Hungarian algorithm to find Max-Weight permutation matrix for selection
        set the packetSwitch of selected VOQs to zero after service
        '''
        if size > 0 and perform_bernoulli_trial(mu):

            # returns a list of tuples of the matrix's corrdinates
            maxWeight = m.compute((-1 * packetSwitch))
            '''
            Munkres algorithm is designed to schedule the minimum cost of the system,
            requiring to set the weights to be negative for computing max-weight
            '''

            # Variable saving the weight of chosen schedule (Purpose: eliminates future inefficiencies)
            remWeight = 0

            # removal & update queue length
            for remove in maxWeight:
                remWeight += packetSwitch[remove[0]][remove[1]]
                if packetSwitch[remove[0]][remove[1]] > 0:  # edge case of removing from zeros.
                    packetSwitch[remove[0]][remove[1]] -= 1
                    size -= 1
            #print(f"The total weight of jobs chosen in Phase {t}'s schedule is {remWeight}.")

        # Sampling Process
        queue_length.append(size)   # Actual Population
        if t > N / 2:               # Sample
            sample.append(size)

    # Recording Sampling
    mean = np.average(sample)

    # Sampling the Queue-Length statistics from the simulation
    print("Traffic Intensity: " + str(rho))
    print("Average Queue Length: " + str(mean))
    print("E[q(t)] / (1 / (1 - ρ)): " + str(mean / (1 / (1 - rho))))    # testing convergence of the constant
    print("--------------------------------------------------")
    qlen.append(mean)
    
# Overview
plt.title("Average Queue Length relative to Traffic Intensity")
plt.plot(traf, qlen)
plt.xlabel("ρ")
plt.ylabel("μ[q(t)]")
plt.show()

    
