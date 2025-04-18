import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# constants
frequency = 440
sample_rate = 44100
duration = 5


def plot_signal(signal, time=None):
    plt.rcParams.update({'font.size':20})
    COLOR = '#967bb6'
    linewidth=3

    samples_count = signal.shape[0]

    plt.figure(figsize=(12,6))
    if time is None:
        xlim = [0, samples_count]
        plt.plot(singal, COLOR, linewidth=linewidth)
        plt.xlabel('samples')
    else:
        xlim = [time[0], time[-1]]
        plt.plot(time, signal, COLOR, linewidth=linewidth)
        plt.xlabel('time (s)')
    plt.hlines(0, xlim[0], xlim[1], 'k')
    plt.ylabel('amplitude')
    plt.xlim(xlim)
    plt.yticks([-1, 0, 1])

    axis = plt.gca()
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)


time = np.arange(sample_rate * duration) / sample_rate ##
sine = np.sin(2 * np.pi * frequency * time) ##
plot_signal(sine[:1000], time[:1000])
