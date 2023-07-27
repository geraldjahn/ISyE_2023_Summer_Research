import numpy as np
import random
import matplotlib.pyplot as plt
from munkres import Munkres

'''
This code observes several quantities that can be measured from the simulation of queueing with a single n x n switch.

The simulation is assuming the size of the switch is small (< 30) that sampling is made from the n^2 / (1 - ρ)^2 th datum
The  n^2 / (1 - ρ)^2 is the value
'''


def perform_bernoulli_trial(p):
    '''
    Performs a single Bernoulli trial with success probability 'p'.
    Function returns a boolean of the trial's success.
    '''
    return random.random() < p

'''
By switching the value of n below, the code will run simulation with different sizes of switches.
The recommended size for the simulation is below 30.
'''
n = 15       # Size of the Switch

'''
Simple Packet Switch with size n, initially empty.
'''
packetSwitch = np.zeros((n,n))

'''
This simulation is setting the service rate and traffic intensity to constant.

Constraints:
    1. the n x n constant matrix with the value lambda must be doubly substochastic.
    2. the traffic intensity and the derived service rate must have a value between [0, 1).
'''

rho = 0.7                   # traffic intensity
lamb = rho / n              # arrival trial success rate
mu = 1                      # service trial success rate

N = 10000
k = int(n ** 2 / (1 - rho) ** 2)        # Equilibrium Constant

m = Munkres()
size = 0                    # Variable Counting the Total Queue Length

total_queue_length = []
schedule_weight = []
non_empty_queue = []
clear_time = []
max_job_queue = []

# Simulation
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

    '''
    Service: Processed after passing the Bernoulli trial, but this simulation will always run the service.
    if not empty, process the Hungarian algorithm to find Max-Weight permutation matrix for selection
    set the packetSwitch of selected VOQs to zero after service
    '''
    if size > 0 and perform_bernoulli_trial(mu):

        # returns a list of tuples of the matrix's corrdinates
        maxWeight = m.compute((-1 * packetSwitch))

        # Variable saving the weight of chosen schedule (Purpose: eliminates future inefficiencies)
        remWeight = 0

        # removal & update queue length
        for remove in maxWeight:
            if packetSwitch[remove[0]][remove[1]] > 0:      # edge case of removing from zeros.
                    remWeight += packetSwitch[remove[0]][remove[1]]
                    packetSwitch[remove[0]][remove[1]] -= 1
                    size -= 1


    # Sampling Target Quantities
    if t >= k:

        # Total Queue Length
        total_queue_length.append(size)
        
        # Recording the Schedule's Weight
        # Hypothesis: W(t) --> λn
        schedule_weight.append(remWeight)
        remWeight = 0       # Edge Case of having an empty switch

        # Additional Task 1. Compute the total number of non-empty queues 
        # Hypothesis: Number of non empty queues should converge when renormalized by n
        filled_queues = packetSwitch[np.where(packetSwitch > 0)]
        non_empty_queue.append(filled_queues.size)

        # 2. Clearing Time: Compute the maximum sum between the maximum sum of columns and that of rows
        # Hypothesis: C(n) --> ln(n)
            # 2 - i) Finding the queue with maximum weight (jobs) loaded
            # Hypothesis: M(t) --> 1 / 1 - ρ
        row_sums = np.sum(packetSwitch, axis = 1)
        col_sums = np.sum(packetSwitch, axis = 0)
        maxWeight_queue = np.max(row_sums)
        max_sum = np.maximum(maxWeight_queue, np.max(col_sums))

        clear_time.append(max_sum)
        max_job_queue.append(maxWeight_queue)

# Overview
print(f"\n<<Statistics for {n} x {n} Switch>>")
print("--------------------------------------------------------------")
print(f"Mean Queue Length for Switch with size {n}: {np.average(total_queue_length)}")
print(f"Mean Weight of Schedule for Switch with size {n}: {np.average(schedule_weight)}")
print(f"Mean number of Non-Empty Queues for Switch with size {n}: {np.average(non_empty_queue)}")
print(f"Mean Clearing Time for Switch with size {n}: {np.average(clear_time)}")
print(f"Mean Weight of the Max-Weighted Queue for Switch with size {n}: {np.average(max_job_queue)}\n")

# Data Visualization
plt.figure(1)
plt.title("Total Queue Length")
plt.xlabel("t")
plt.ylabel("q(t)")
plt.plot(range(k, N), total_queue_length)

plt.figure(2)
plt.title("Schedule's Weight")
plt.xlabel("t")
plt.ylabel("W(t)")
plt.plot(range(k, N), schedule_weight)

plt.figure(3)
plt.title("Total Number of Non-Empty Queues")
plt.xlabel("t")
plt.ylabel("E(t)")
plt.plot(range(k, N), non_empty_queue)

plt.figure(4)
plt.title("Clearing Time")
plt.xlabel("t")
plt.ylabel("C(t)")
plt.plot(range(k, N), clear_time)

plt.figure(5)
plt.title("Weight of the Max-Weight Queue")
plt.xlabel("t")
plt.ylabel("M(t)")
plt.plot(range(k, N), max_job_queue)

plt.show()
