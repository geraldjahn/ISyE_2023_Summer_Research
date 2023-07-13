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


lamb = float(sys.argv[1])   # average arrival rate: mean number of enqueues made per unit time. Lambda must be set less than min(ρ)
print("Arrival Rate: " + str(lamb))
print()
x = []
y = []

# Simulation: This file needs to run a parameter (arrival rate) through the terminal.
# The simulation aims to compute the average queue length in respect to the traffic intensity.
for rho in np.arange(0.9, 1.0, 0.01):
    mu = lamb / rho             # average service rate: mean number of dequeues made per unit time, (0.0, 1.0)
    N = int(10 / ((1 - rho) ** 2))  # sample size
    queue_length = []
    queue = []
    wait = 0
    x.append(rho)
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

    # Sampling the Queue-Length statistics from the simulation
    print("Traffic Intensity: " + str(rho))
    print("Average Queue Length: " + str(np.average(queue)))
    print("--------------------------------------------------")
    y.append(np.average(queue))

plt.title("Average Queue Length relative to Traffic Intensity")
plt.plot(x, y)
plt.xlabel("ρ")
plt.ylabel("μ[q(t)]")
plt.show()
