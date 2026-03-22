######################################################
# Non-invasive Brain-Computer Interfaces, KU [709.028]
#             Assignment 1, Exercise 2
#----------------------------------------------------
#           Group: XY
#               Member 1:
#               Member 2:
######################################################

# -- Python imports --
from scipy.io import loadmat
import matplotlib.pyplot as plt
import mne
from mne.preprocessing import ICA
from mne_icalabel import label_components

# -- Parameter Definitions --
sfreq = 200 # Hz
ch_names = [
    "Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FT7", "FC3", "FCz",
    "FC4", "FT8", "T7", "C3", "Cz", "C4", "T8", "TP7", "CP3", "CPz",
    "CP4", "TP8", "P7", "P3", "Pz", "P4", "P8", "O1", "Oz", "O2"
]

# -- Functions --
def pipeline_1(raw, bad_channels):
    # TODO
    raw_1 = ...
    return raw_1

def pipeline_2(raw):
    # TODO
    raw_2 = ...
    return raw_2

def main():
    # -- 1. Data Import and Channel Localization --
    # Load Data
    data = loadmat('eegdata.mat')['eegdata'] # Numpy array of shape (n_channels x n_samples) = (30 x 1600)
    data = data*1e-6  # Rescale to muV from V

    # Create MNE raw object
    info = mne.create_info(ch_names=ch_names,
                           sfreq=sfreq,
                           ch_types="eeg")
    raw = mne.io.RawArray(data, info)

    # Set channel montage
    montage = mne.channels.make_standard_montage("standard_1020")
    raw.set_montage(montage)

    # TODO: -- 2. Data Visualization and Identification of Noisy Channels --
    ...
    bad_channels = [] # After the visualization you should have a list with the bad channels
    
    # TODO: -- 3. Preprocessing Pipeline 1 (Removing Noisy Channels) --
    raw_1 = pipeline_1(raw=raw, bad_channels=bad_channels)

    # TODO: -- 4. Preprocessing Pipeline 2 (Without Removing Noisy Channels) --
    raw_2 = pipeline_2(raw=raw)

# -- Main --
if __name__ == "__main__":
    main()
    plt.show()