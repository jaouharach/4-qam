import random
from signal import signal
import numpy as np
import matplotlib.pyplot as plt
import math 

qam = {
    '00' : complex(math.cos(math.pi/4), math.sin(math.pi/4)) ,
    '01' : complex(math.cos(7 * math.pi/4), math.sin(7 * math.pi/4)),
    '10' : complex(math.cos(3 * math.pi/4), math.sin(3 * math.pi/4)),
    '11' : complex(math.cos(5 * math.pi/4), math.sin(5 * math.pi/4)),
}

def euclidean_dist(p1, p2):
    return math.sqrt((p1.real-p2.real)**2+(p1.imag-p2.imag)**2)

# approximate a data point based on closest m in 4-QAM
def approximate(data_point, modulation):
    min_dist = 100000
    closest_mod = ""
    d = 0
    for m in modulation.keys():
        d = euclidean_dist(data_point, modulation.get(m))
        if(d < min_dist):
            min_dist = d
            closest_mod = m
    return closest_mod

# original vector
data = [ random.choice([0, 1]) for i in range(360)]
# print(data)

avg_ber = 0
num_iter = 1000
for k in range(num_iter):
    # generate the noise 
    mu, sigma = 0, math.sqrt(1/10 ** (3/10)) # mean and standard deviation
    nr = np.random.normal(mu, sigma,  int(len(data)/2))
    ni = np.random.normal(mu, sigma,  int(len(data)/2))
    noise = [complex(nr[i],ni[i]) for i in range(int(len(data)/2))]

    # print("\n\n\nNoise:\n\n\n")
    # print(noise)

    i = 0
    j = 0
    recieved_signal = []

    while(i < len(data)):
        data_point = str(data[i]) + str (data[i+1])
        recieved_signal.append(qam.get(data_point)+noise[j])
        i = i + 2
        j = j + 1

    # print(f"\n\n\nRecieved signal (length = {len(recieved_signal)}):\n\n\n")
    # print(recieved_signal)

    # approximate the original signal
    approx_signal = []
    for s in recieved_signal:
        bits = approximate(s, qam)
        approx_signal.append(int(bits[0]))
        approx_signal.append(int(bits[1]))

    # print(approx_signal)


    # compute the BER
    ber = 0
    for i in range(int(len(data))):
        if approx_signal[i] != data[i]:
            ber = ber + 1

    ber = ber/len(data)
    avg_ber = avg_ber + ber

print(f"Average bit error rate = {avg_ber/num_iter}")
