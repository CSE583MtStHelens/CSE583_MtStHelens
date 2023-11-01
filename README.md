# CSE583_MtStHelens

## Background

## Products

## Goal

## Installation

## Data structure
This project is structured in the way that we have a folder ```code``` where you can find the jupyter notebooks or python scripts. The folder ```data``` contains some example files. In our case we do have .csv files of the preprocessed seismic data. Each file contains the data of one seismic station and one year. The column headers indicate different parameters extracted from seismic time series. The rows represent time windows of 10 minutes. The ```doc``` folder contains some informations about the project.<br>

Some abbreviations:<br>
- **RSAM:** Real-Time Seismic Amplitude Measurement is a measure of seismic power. We get it by taking seismic groud velocity (that is what a seismometer measures) and apply a bandpass filter to end. The filtered time series then is cut into 10 minute long time windows and the mean of the absolute values than is the RSAM. Our example data has three different RSAM time series (RSAM, MF, HF). Each time series is filtered in a different frequency range (2-5 Hz, 4.5-8 Hz, 8-16Hz). These frequency bands are typical for volcano seismology.
- **DSAR:** Displacement Seismic Amplitude Ratio is a measure for attenuation. We get ground displacement by integrating seismic ground velocity. We apply the same bandpass filters as for RSAM. To get an wave attenuation (we assume that the seismic source does not change and the wave attenuation is simply due to changes of the underground) we devide a low frequency band by a high frequency band. For DSAR it is MF/HF, lDSAR is RSAM/MF, lhDSAR is RSAM/HF. VSAR and lhVSAR follows the same procedure without the convertion from ground velocity to ground displacement.
- **RMS:**
- **RMeS:**
- **PGV:**
- **PGA:**
- **zsc:**

## Code strucutre

## Tutorial
