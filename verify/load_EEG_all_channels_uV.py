# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:49:35 2023

@author: leyu3109
"""

import numpy as np
from NF import notch_filter
from C5_2 import Filtering_BPF
from EDFlib import edfreader

def load_EEG_all_channels(path, 
                          sampling_rate = 5000, 
                          filtering = True, 
                          BPFfc = [5,100], 
                          BPF_order = 3, 
                          BSF_order = 3, 
                          not_filtering_channels = []):
    '''
    path: Path of the .bdf file 
    sampling_rate: Sampling rate
    BPFfc: Cut-off frequencies for band-pass filter
    BSFfc: ~ band-stop filter
    BPF_order： Order for band-pass filter
    BSF_order： ~ band-stop filter
    last: length of the data which is going to load in seconds
    
    return: EEG_data after filtering
    '''
    
    hdl = edfreader.EDFreader(path)
    last = hdl.getNumDataRecords()
    print("Number of signals: %d" %(hdl.getNumSignals()))
    print("Number of datarecords: %d" %(hdl.getNumDataRecords()))
    
    number_of_signals = hdl.getNumSignals()
    channel_names = []
    scaling_factors = []  # Store scaling factors for each channel
    offset_list = []
    for i in range(number_of_signals):
        channel_names.append(hdl.getSignalLabel(i).strip())
        upb = (hdl.getPhysicalMaximum(i) - hdl.getPhysicalMinimum(i)) / (hdl.getDigitalMaximum(i) - hdl.getDigitalMinimum(i))
        scaling_factors.append(upb)
        offset_list.append(hdl.getPhysicalMaximum(i)/upb - hdl.getDigitalMaximum(i))
    print(channel_names)
    print(scaling_factors)
    print(offset_list)
    signal_list = list(range(0, number_of_signals))
    # Create a list to store arrays (2D array of EEG_data2)
    all_EEG_data2 = []
    BPF = Filtering_BPF(BPFfc[0],BPFfc[1],sampling_rate,BPF_order)
    
    for i in signal_list:
        channel = i
        hdl.fseek(channel, 0, 0)
        EEG_data = np.array([0 for i in range(0, last * sampling_rate)])
        hdl.readSamples(channel, EEG_data, last * sampling_rate)
        if filtering and i not in not_filtering_channels:
            EEG_data1 = notch_filter(EEG_data)
            EEG_data2 = BPF.butter_filter(EEG_data1)
            EEG_data2 = EEG_data2.astype(int)
            EEG_data2 = EEG_data2[5*sampling_rate:]
        else:
            EEG_data2 = EEG_data[5*sampling_rate:]

        # Apply scaling factor to convert to uV
        EEG_data2_uV = EEG_data2 * scaling_factors[i] - offset_list[i]

        # Append EEG_data2_uV to the list
        all_EEG_data2.append(EEG_data2_uV)
    
    # Convert the list of arrays to a 2D NumPy array
    all_EEG_data2_array = np.array(all_EEG_data2)
    
    hdl.close()

    return all_EEG_data2_array, channel_names
