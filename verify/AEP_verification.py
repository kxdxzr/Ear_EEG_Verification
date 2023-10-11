# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 12:52:19 2023

@author: yulep
"""
import sys
import numpy as np
from EDFlib import edfreader
import matplotlib.pyplot as plt 

def mins_to_points(mins,sampling_rate):
    ls = mins.split(".")
    total = (int(ls[0]) * 60 + int(ls[1])) * sampling_rate
    return total
    
def average_EEG(channel,sampling_rate,last,time,hdl,title):
    data = np.array([0 for i in range(0,int(last * sampling_rate))])
    for i in time:
        first_point = mins_to_points(i,sampling_rate)
        hdl.fseek(channel,first_point,0)
        arr1 = np.array([0 for i in range(0,int(last * sampling_rate))])
        hdl.readSamples(channel, arr1, int(last * sampling_rate))
        data += arr1
    output = np.zeros_like(data, dtype=float)  # create a float array with the same shape as data
    output = data / len(time)  # perform the division operation and store the result in output
    
    x = np.linspace(0,last,int(last * sampling_rate))
    f = plt.figure("{} for channel {}".format(title, channel + 1)) 
    plt.title("{} for channel {}".format(title, channel + 1))
    plt.plot(x,output)
    plt.show()
    


time = ['0.25','0.45','1.05','1.25']
time_2 = ['0.35','0.55','1.15']
'''
0.20-0.30
0.40-0.50
1.00-1.10
1.20-1.30
'''

path = "AEP/NeoRec_2023-03-14_14-36-59.bdf"

hdl = edfreader.EDFreader(path)

print("Number of signals: %d" %(hdl.getNumSignals()))
print("Number of datarecords: %d" %(hdl.getNumDataRecords()))

filetype = hdl.getFileType()

edfsignals = hdl.getNumSignals()

n = edfsignals
# channel number starts with 0
channel = 5
sampling_rate = 5000
last = 1

average_EEG(channel,sampling_rate,last,time,hdl,"AEP")
average_EEG(channel,sampling_rate,last,time_2,hdl,"Normal")