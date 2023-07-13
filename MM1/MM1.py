import random
import sys
import numpy as np
import matplotlib.pyplot as plt

# Simple design of a steady state M/M/1 Queue using Lindley equation.

# Lindley Equation: Computes the queue length with a discrete-time stochastic process.

def perform_bernoulli_trial(p):
    """Performs a single Bernoulli trial with success probability 'p'.
       Function returns a boolean of the trial's success."""
    return random.random() < p


lamb = float(sys.argv[1])   # average arrival rate: mean number of enqueues made per unit time, [0.0, 1.0)
rho = float(sys.argv[2])    # Traffic intensity
mu = lamb / rho             # average service rate: mean number of dequeues made per unit time, [0.0, 1.0)
N = int(10 / ((1 - rho) ** 2))  # sample size

queue_length = []
queue = []
wait = 0

# Simulation

for t in range(N):          # Simulating N random variables

    # Bernoulli trial for the arrival (Enqueueing)
    arrival = perform_bernoulli_trial(lamb)
    if arrival:
        wait += 1
    
    # Dequeueing the M/M/1 Queue
    service = perform_bernoulli_trial(mu)
    if service and wait > 0:
        wait -= 1
    
    # Sampling the data
    queue_length.append(wait)
    if t > N / 2:
        queue.append(wait)
    
    # Plotting the actual queue length throughout N-phases
    plt.plot(queue_length)
    plt.title("Waiting Time")
    plt.scatter(range(len(queue_length)), queue_length)

    # Draw, Pause, and Clear
    plt.draw()
    plt.pause(0.1)
    plt.clf()

# Sampling the Queue-Length statistics from the simulation
print("Traffic Intensity: " + str(rho))
print("Average Queue Length: " + str(np.average(queue)))
