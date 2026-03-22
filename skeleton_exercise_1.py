######################################################
# Non-invasive Brain-Computer Interfaces, KU [709.028]
#             Assignment 1, Exercise 1
#----------------------------------------------------
#           Group: XY
#               Member 1:
#               Member 2:
######################################################

# -- Python imports --
from scipy.io import loadmat
import matplotlib.pyplot as plt
import mne

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

# TODO: Write a function to apply laplacian derivative
...

# TODO: Write a function to apply CAR
...

def main():
    # Load Data
    data_1 = loadmat('data1.mat')
    data1_noisy = data_1['noisy_data1']*1e-6 # Rescale the data from V to muV
    data1_clean = data_1['clean_data1']*1e-6
    data_2 = loadmat('data2.mat')
    data2_noisy = data_2['noisy_data2']*1e-6
    data2_clean = data_2['clean_data2']*1e-6

    # Visualize noisy data
    eeg_plot(data1_noisy, ch_names=ch_names, sfreq=sfreq)
    eeg_plot(data2_noisy, ch_names=ch_names, sfreq=sfreq)

    # TODO: Apply spatial filters according to the assignment sheet
    ...
    

if __name__ == "__main__":
    main()
    plt.show()