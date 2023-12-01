# This file is for manipulation functuions for the Mt St Helens Project

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

def filter_data(stack):

    def lowpass(cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='low', analog=False) #returns coefficients of transfer function of the low pass filter

    def lowp_filter(data, cutoff, fs, order=5):
        b, a = lowpass(cutoff, fs, order=order)
        return lfilter(b, a, data)
        
    filt_stack = np.zeros_like(stack)
    print(stack.shape)
    print(filt_stack.shape[1])
    order = 6
    fs = 30      #sampling rate
    cutoff = 0.02  #cutoff frequency

    b, a = lowpass(cutoff, fs, order)
    w, h = freqz(b, a, fs=fs, worN=8000) #Frequency response
    plt.subplot(2, 1, 1)
    plt.plot(w, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2))
    plt.axvline(cutoff)
    plt.xlim(0, 1)
    plt.xlabel('Frequency')

    for j in range (stack.shape[1]):
            data = stack[:,j]
            filt = lowp_filter(data, cutoff, fs, order)
            filt_stack[:,j] = filt
            
    return filt_stack


