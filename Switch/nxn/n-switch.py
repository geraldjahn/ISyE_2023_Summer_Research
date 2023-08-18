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

This file is highly recommended to run with small range of x_n.
The runtime for large switch is not adequate for household computers nor the simulation is suitable for large switch simulations (Python inefficiencies)
'''

'''
Independent Variable: Switch Size [n]
Constants: Traffic Intensity, Service Rate

The arrivals and services are independent events.
'''
x_n = list(range(2, 65))      # value of n for n x n switch. n: [2, 64]

rho = 0.7                       # traffic intensity (load)
mu = 1                          # service trial success rate -> here, 1 assumes that it dequeues every phase when the VOQ is not empty.

total_queue_length = []
schedule_weight = []
clear_time = []
non_empty_queue = []
max_length_voq = []
convergence = []

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
    

    N = max(50000, int(2 * n ** 2 / (1 - rho)))           # if the switch's sizes increase, the value needs to be increased to have all switches' simulation to reach equilibrium.

    # Setting the equilibrium constant for sampling
    k = int(N / 2)

    m = Munkres()
    size = 0            # Variable counting the Total Queue Length
    tql_mean = 0
    sw_mean = 0
    ct_mean = 0
    neq_mean = 0
    mlv_mean = 0

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
        Recording Observables
        '''
        if t >= k:
            # Total Queue Length
            tql_mean *= (t - k)
            tql_mean += size
            tql_mean /= (t - k + 1)

            # Schedule's Weight
            # Hypothesis: lim t -> inf W(t) = W(n) --> λn
            sw_mean *= (t - k)
            sw_mean += remWeight
            sw_mean /= (t - k + 1)
            remWeight = 0       # Edge Case of having an empty switch
            

            # Additional Task 1. Total number of non-empty queues
            filled_queues = nSwitch[np.where(nSwitch > 0)]
            neq_mean *= (t - k)
            neq_mean += filled_queues.size
            neq_mean /= (t - k + 1)

            # Additional Task 2. Clearing Time: Compute the maximum sum between the maximum sum of columns and that of rows
            # Hypothesis: C(n) --> ln(n)
                # 2 - i) Finding the length of the VOQ with max weight
                # Hypothesis: M(n) --> 1 / 1 - ρ
            row_sums = np.sum(nSwitch, axis = 1)
            col_sums = np.sum(nSwitch, axis = 0)
            max_sum = np.maximum(np.max(row_sums), np.max(col_sums))

            ct_mean *= (t - k)
            ct_mean += max_sum
            ct_mean /= (t - k + 1)

            mlv_mean *= (t - k)
            mlv_mean += np.amax(nSwitch)
            mlv_mean /= (t - k + 1)

    # Recording the Overview Statistics
    total_queue_length.append(tql_mean)
    schedule_weight.append(sw_mean)
    non_empty_queue.append(neq_mean)
    clear_time.append(ct_mean)
    max_length_voq.append(mlv_mean)

    # Testing the convergence of Total Queue Length in a linear trend
    # Assumption: the plot should return a constant function close to 1.
    convergence.append((tql_mean) * (1 - rho) / n)


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
plt.title("Length of the Max-Length Virtual Output Queue")
plt.xlabel("n")
plt.ylabel("M(n)")
plt.plot(x_n, max_length_voq)

plt.figure(6)
plt.title("Convergence of Total Queue Length's Linear Trend")
plt.xlabel("n")
plt.ylabel("C(n)")
plt.plot(x_n, convergence)


plt.show()
