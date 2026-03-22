######################################################
# Non-invasive Brain-Computer Interfaces, KU [709.028]
#             Assignment 1, Exercise 1
#----------------------------------------------------
#           Group: 14
#               Member 1: Niklas Peterek
#               Member 2: Lukas Springer
######################################################

# -- Python imports --
from scipy.io import loadmat
import matplotlib.pyplot as plt
import mne
import numpy as np

# -- Parameter Definitions --
sfreq = 200 # Hz
ch_names = [
    "Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FT7", "FC3", "FCz",
    "FC4", "FT8", "T7", "C3", "Cz", "C4", "T8", "TP7", "CP3", "CPz",
    "CP4", "TP8", "P7", "P3", "Pz", "P4", "P8", "O1", "Oz", "O2"
]

neighbors = {
    "Fp1": ["F3"],
    "Fp2": ["F4"],
    "F7": ["F3", "FT7"],
    "F3": ["Fp1", "F7", "Fz", "FC3"],
    "Fz": ["F3", "F4", "FCz"],
    "F4": ["Fp2", "Fz", "FC4", "F8"],
    "F8": ["F4", "FT8"],
    "FT7": ["F7", "T7", "FC3"],
    "FC3": ["FT7", "F3", "C3", "FCz"],
    "FCz": ["Fz", "Cz", "FC3", "FC4"],
    "FC4": ["FCz", "F4", "C4", "FT8"],
    "FT8": ["FC4", "F8", "T8"],
    "T7": ["C3", "FT7", "TP7"],
    "C3": ["T7", "FC3", "CP3", "Cz"],
    "Cz": ["C3", "CPz", "C4", "FCz"],
    "C4": ["Cz", "T8", "FC4", "CP4"],
    "T8": ["C4", "TP8", "FT8"],
    "TP7": ["CP3", "P7", "T7"],
    "CP3": ["TP7", "C3", "P3", "CPz"],
    "CPz": ["CP3", "CP4", "Cz", "Pz"],
    "CP4": ["CPz", "P4", "TP8", "C4"],
    "TP8": ["T8", "CP4", "P8"],
    "P7": ["TP7", "P3"],
    "P3": ["CP3", "P7", "Pz", "O1"],
    "Pz": ["P3", "P4", "Oz", "CPz"],
    "P4": ["Pz", "P8", "O2", "CP4"],
    "P8": ["P4", "TP8"],
    "O1": ["Oz", "P3"],
    "Oz": ["O1", "O2", "Pz"],
    "O2": ["P4", "Oz"]
}

# -- Functions --
def eeg_plot(data, ch_names, sfreq, title="EEG"):
    """
    Wrapper for MNE raw.plot()
    """

    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(data, info)

    raw.plot(
        duration=8,       # show full signal
        n_channels=len(ch_names),
        scalings=dict(eeg=50e-6),
        title=title,
        show=True
    )

# Function to apply laplacian rereferencing

def apply_laplacian(data, neighbors= neighbors, ch_names = ch_names, g_j = 0.5):
    """applies laplacian re-referencing on the given data

    Args:
        data: EEG data, seperated into channels
        neighbors (dict, optional): dict of every electrode as key and its list of neighbours as value. Defaults to neighbors.
        ch_names (list, optional): list of recorded channels. Defaults to ch_names.
        g_j (float, optional): weighing factor. Defaults to 0.5.

    Returns:
        EEG data that is laplacian re-referenced
    """
    
    n_channels, n_samples = data.shape # get number of channels and samples from the data
    data_lap = np.empty((n_channels, n_samples)) # generate an empty matrix for the rereferenced values to go into

    for idx, ch_name in enumerate(ch_names): #iterate over channels
        channel_data = data[idx] #select the recording of the current channel
        channel_neighbours = neighbors[ch_name] #  get the list of neighbours for that channel

        n_neighbours = len(channel_neighbours) # how many neighbours
        neighbour_weigthed_sum = np.zeros(n_samples) # preallocate space for th ewieghted sum used for substraction

        for channel in channel_neighbours: # iterate over neighbours
            neighbour_idx = ch_names.index(channel) # get the index for the chosen channel name
            neighbor_data = data[neighbour_idx] # get the recorded data for that index

            neighbour_weigthed_sum += g_j * neighbor_data # sum up the recordings of all neighbours 
            
        channel_laplace_data = channel_data - ((1/n_neighbours) * neighbour_weigthed_sum) # substract the weighted average of the neighbours from the channel

        data_lap[idx] = channel_laplace_data # insert the data into the preallocated matrix


    return data_lap

# Function to apply CAR

def apply_car(data, ch_names):

    n_channels, n_samples = data.shape # get number of channels and samples from the data
    data_car = np.empty((n_channels, n_samples)) # generate an empty matrix for the rereferenced values to go into

    all_weigthed_sum = np.zeros(n_samples) # preallocate space for th ewieghted sum used for substraction

    for idx, _ in enumerate(ch_names): #iterate over channels
        current_channel_data = data[idx] # get the recorded data for that index
        all_weigthed_sum += current_channel_data # sum up the recordings of all neighbours 
        common_average = ((1/n_channels) * all_weigthed_sum) # average over all channels

    for idx, _ in enumerate(ch_names): #iterate over channels
        channel_data = data[idx] #select the recording of the current channel
        channel_car_data = channel_data - common_average # substract the common average from the channel
        data_car[idx] = channel_car_data # insert the data into the preallocated matrix

    return data_car


def main():
    # Load Data
    data_1 = loadmat('data1.mat')
    data1_noisy = data_1['noisy_data1']*1e-6 # Rescale the data from V to muV
    data1_clean = data_1['clean_data1']*1e-6
    data_2 = loadmat('data2.mat')
    data2_noisy = data_2['noisy_data2']*1e-6
    data2_clean = data_2['clean_data2']*1e-6


    # Visualize noisy data
    # eeg_plot(data1_noisy, ch_names=ch_names, sfreq=sfreq, title="EEG 1 noisy")

    eeg_plot(data2_noisy, ch_names=ch_names, sfreq=sfreq, title="EEG 2 noisy")

    # TODO: Apply spatial filters according to the assignment sheet
    
    
    data1_lap = apply_laplacian(data1_noisy, neighbors, ch_names, 0.5)
    data1_car = apply_car(data1_noisy, ch_names)

    data2_lap = apply_laplacian(data2_noisy, neighbors, ch_names, 0.5)
    data2_car = apply_car(data2_noisy, ch_names)

    # eeg_plot(data1_lap, ch_names=ch_names, sfreq=sfreq, title="EEG 1 noisy - Laplacian re-referencing applied")
    # eeg_plot(data1_car, ch_names=ch_names, sfreq=sfreq, title="EEG 1 noisy - Car re-referencing applied")
    # eeg_plot(data1_clean, ch_names=ch_names, sfreq=sfreq, title="EEG 1 Clean")

    eeg_plot(data2_lap, ch_names=ch_names, sfreq=sfreq, title="EEG 2 noisy - Laplacian re-referencing applied")
    eeg_plot(data2_car, ch_names=ch_names, sfreq=sfreq, title="EEG 2 noisy - Car re-referencing applied")
    eeg_plot(data2_clean, ch_names=ch_names, sfreq=sfreq, title="EEG 2 Clean")




if __name__ == "__main__":
    main()
    plt.show()