import numpy as np
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
** IMPORTANT **

This file is highly recommended to run in PACE. The simulation is not adequate to be run in household computers.
'''

'''
Independent Variable: Switch Size [n]
Constants: Traffic Intensity, Service Rate

Currently, the range is set to [2, 10) for preventing overload issues.
'''
x_n = list(range(2, 10))      # value of n for n x n switch. n: [2, 1024]

rho = 0.7                       # traffic intensity (load)
mu = 1                          # service trial success rate -> here, 1 assumes that it dequeues every phase when the VOQ is not empty.

total_queue_length = []
schedule_weight = []
clear_time = []
non_empty_queue = []
max_job_queue = []

for n in x_n:

    '''
    Simple Packet Switch with size n, initially empty.
    Creates an n x n matrix.
    '''
    nSwitch = np.zeros((n,n))

    '''
    Constraints:
    1. the n x n constant matrix with the value lambda must be doubly substochastic.
    2. the traffic intensity and the derived service rate must have a value between [0, 1).
    '''
    lamb = rho / n      # arrival trial success rate
    

    N = 10000           # if the switch's sizes increase, the value needs to be increased to have all switches' simulation to reach equilibrium.

    m = Munkres()
    size = 0            # Variable counting the Total Queue Length

    tql_mean = []
    sw_mean = []
    ct_mean = []
    neq_mean = []
    mjq_mean = []

    # Simulation for 1 switch
    for t in range(N):
        '''
        Arrival: Processed after Passing the Bernoulli trial
        '''
        for x in range(len(nSwitch)):
            for y in range(len(nSwitch[x])):
                if perform_bernoulli_trial(lamb):
                    # weight of the job is fixed to 1.
                    nSwitch[x][y] += 1
                    size += 1
        
        '''
        Service: Processed after passing the Bernoulli trial, but this simulation will always run the service.
        if not empty, process the Hungarian algorithm to find Max-Weight permutation matrix for selection
        set the packetSwitch of selected VOQs to zero after service
        '''
        if size > 0 and perform_bernoulli_trial(mu):

            # returns a list of tuples of the matrix's corrdinates
            maxWeight = m.compute((-1 * nSwitch))

            # Variable saving the weight of chosen schedule (Purpose: eliminates future inefficiencies)
            remWeight = 0

            # removal & update queue length
            for remove in maxWeight:
                if nSwitch[remove[0]][remove[1]] > 0:  # edge case of removing from zeros.
                        remWeight += nSwitch[remove[0]][remove[1]]
                        nSwitch[remove[0]][remove[1]] -= 1
                        size -= 1


            '''
            Recording Quantities: Conditional Statement Needed!!
            '''

            # Total Queue Length
            tql_mean.append(size)

            # Schedule's Weight
            # Hypothesis: lim t -> inf W(t) = W(n) --> λn
            sw_mean.append(remWeight)
            remWeight = 0       # Edge Case of having an empty switch
            

            # Additional Task 1. Total number of non-empty queues
            filled_queues = nSwitch[np.where(nSwitch > 0)]
            neq_mean.append(filled_queues.size)

            # Additional Task 2. Clearing Time: Compute the maximum sum between the maximum sum of columns and that of rows
            # Hypothesis: C(n) --> ln(n)
                # 2 - i) Finding the length of the VOQ with max weight
                # Hypothesis: M(n) --> 1 / 1 - ρ
            row_sums = np.sum(nSwitch, axis = 1)
            col_sums = np.sum(nSwitch, axis = 0)
            maxWeight_queue = np.max(row_sums)
            max_sum = np.maximum(maxWeight_queue, np.max(col_sums))

            ct_mean.append(max_sum)
            mjq_mean.append(maxWeight_queue)

        # Recording Process --> Sampling is needed (Collecting Data Once the system reaches the equilibrium)
        # Assumption: N_eq = C * n / (1 - ρ)^2
        # if t >= k: k is an equilibrium constant

    # Recording the Overview Statistics
    total_queue_length.append(np.average(tql_mean))
    schedule_weight.append(np.average(sw_mean))
    non_empty_queue.append(np.average(neq_mean))
    clear_time.append(np.average(ct_mean))
    max_job_queue.append(np.average(mjq_mean))


# Data Visualization
plt.figure(1)
plt.title("Total Queue Length")
plt.xlabel("n")
plt.ylabel("q(n)")
plt.plot(x_n, total_queue_length)

plt.figure(2)
plt.title("Schedule's Weight")
plt.xlabel("n")
plt.ylabel("W(n)")
plt.plot(x_n, schedule_weight)

plt.figure(3)
plt.title("Total Number of Non-Empty Queues")
plt.xlabel("n")
plt.ylabel("E(n)")
plt.plot(x_n, non_empty_queue)

plt.figure(4)
plt.title("Clearing Time")
plt.xlabel("n")
plt.ylabel("C(n)")
plt.plot(x_n, clear_time)

plt.figure(5)
plt.title("Weight of the Max-Weight Queue")
plt.xlabel("n")
plt.ylabel("M(n)")
plt.plot(x_n, max_job_queue)

plt.show()
