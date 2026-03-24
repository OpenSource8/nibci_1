######################################################
# Non-invasive Brain-Computer Interfaces, KU [709.028]
#             Assignment 1, Exercise 2
#----------------------------------------------------
#           Group: 14
#               Member 1: Niklas Peterek
#               Member 2: Lukas Springer 
######################################################

# -- Python imports --
from scipy.io import loadmat
import matplotlib.pyplot as plt
import mne
from mne.preprocessing import ICA
from mne_icalabel import label_components
import numpy as np

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
    raw_1 = raw.copy()


    raw_1.info["bads"] = bad_channels
    print(raw_1.info["bads"])


    n_used_channels = len(ch_names) - len(bad_channels)

    raw_1.drop_channels(bad_channels)

    raw_1.set_eeg_reference(ref_channels = "average", projection = False)


    # as documentation gives a warning:
    # ICA is sensitive to low-frequency drifts and therefore 
    # requires the data to be high-pass filtered prior to fitting. 
    # Typically, a cutoff frequency of 1 Hz is recommended.
    raw_1.filter(1, None)

    ica = ICA(n_used_channels, random_state=7, method="fastica")

    ica.fit(raw_1)



    ica.plot_components(title = "ica components")
    ica.plot_sources(raw_1,title ="ica sources")

    ic_labels = label_components(raw_1, ica, method="iclabel")
    y_pred_proba = ic_labels["y_pred_proba"]
    labels = ic_labels["labels"]

    confidence_threshold = 0.8

    ica_high = {}
    ica_low = {}

    for idx, pred in enumerate(y_pred_proba):
        if pred >= confidence_threshold:
             ica_high[idx] = [labels[idx], pred]

    for idx, pred in enumerate(y_pred_proba):
        if pred < confidence_threshold:
             ica_low[idx] = [labels[idx], pred]


    
    high_c_brain = {}
    high_c_artifacts = {}
    for entry in ica_high:
        print(entry)
        if ica_high[entry][0] == "brain":
            high_c_brain[entry] = ica_high[entry]
        else:
            high_c_artifacts[entry] = ica_high[entry]

    low_c_brain = {}
    low_c_artifacts = {}
    for entry in ica_low:
        print(entry)
        if ica_low[entry][0] == "brain":
            low_c_brain[entry] = ica_low[entry]
        else:
            low_c_artifacts[entry] = ica_low[entry]

    print("__________________________________________\n")
    print("high cnfidence")
    print("Brain\n")
    print(high_c_brain)

    print("Artifacts\n")
    print(high_c_artifacts)

    print("__________________________________________\n")
    print("low confidence")
    print("Brain\n")
    print(low_c_brain)

    print("Artifacts\n")
    print(low_c_artifacts)


    keep = {**high_c_brain, **low_c_brain, **low_c_artifacts}.keys()
    exclude = high_c_artifacts.keys()


    return raw_1, keep, exclude

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

    # raw.plot(duration=24,       # show full signal
    #     n_channels=len(ch_names),
    #     scalings=dict(eeg=50e-6),
    #     title="Raw EEG data",
    #     show=True)
    
    # raw.plot_sensors(show_names = True)
    # raw.plot_psd_topomap()
    # raw.compute_psd().plot() # as .plot_psd is a legacy function

    bad_channels = ["F4", "T8"] # After the visualization you should have a list with the bad channels

    # T8 porbably electrode artifact -> electrode popping maybe?
    # F4 probably bad contact of electrode?

    # TODO: -- 3. Preprocessing Pipeline 1 (Removing Noisy Channels) --
    raw_1 = pipeline_1(raw=raw, bad_channels=bad_channels)


    # TODO: -- 4. Preprocessing Pipeline 2 (Without Removing Noisy Channels) --
    raw_2 = pipeline_2(raw=raw)

# -- Main --
if __name__ == "__main__":
    main()
    plt.show()