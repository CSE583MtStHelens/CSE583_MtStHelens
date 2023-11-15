# CSE583_MtStHelens

## Background
<img align="right" width="400" src=https://github.com/CSE583MtStHelens/CSE583_MtStHelens/assets/107423514/87e29a01-e5bd-45ab-be13-c0c8d70b653f>
Mount St. Helens, located in the Cascade Range, is a stratovolcano with a significant eruption history. The eruption of 2004 lasted for four years and began with a notable shallow earthquake swarm on September 23, 2004. Just one week later, the first explosion occurred on October 1, 2004. Subsequent months saw increased seismic activity at the volcano, including volcanic earthquakes, tremors, and debris flow. These volcanic events exhibited a dominant frequency of approximately 10 Hz. This heightened volcanic activity continued over the next two years (2005 and 2006), during which multiple domes formed within the crater. From image data, the magma extrusion rate was estimated. However, in line with the decreased seismicity, the magma extrusion rates also declined. Volcanologists officially declared the end of the eruption in February 2008.<br/>

The seismic data collected during the volcanic activity is just one part of a more extensive dataset. Even before the eruption, a network of seismometers was monitoring the underground. During the eruption, the seismic network underwent dynamic changes involving instrument failures, replacements, and density enhancements. Post-eruption, some instruments were removed. Overall, the seismic network boasts remarkable data density, with time series spanning over 22 years. These time series provide insights into long-term underground changes, which will serve as a foundation for further analyses.
<img src=https://github.com/CSE583MtStHelens/CSE583_MtStHelens/assets/107423514/e48949a2-3148-4007-8dd9-0b0c07f8aaf5>


## Goals
1. **Correlation of Seismic Attenuation and Magma Extrusion**: This project aims to investigate whether seismic attenuation, resulting from near-surface changes, correlates with the magma extrusion rate. Such correlation is expected due to the impact of infiltrating magma on the material properties along the seismic wave path, which should be discernible and linked to the rate of dome growth. Beyond magma influx, various factors like heavy rainfall or snowfall can alter underground pore pressure. To distinguish these dominant influences, which often exhibit strong seasonal patterns, two methods will be tested. First, a high-pass filter will be applied to remove all periods longer than one year. Second, data will be stacked in time, meaning the average waveform over all years for each station. This station-specific average seasonality will be subtracted from the attenuation data. This process should enable the correlation of seismic attenuation with the rate of dome extrusion.<br>

2. **Analysis of Changing Climatic Patterns**: The long-term seismic data is crucial for understanding the broader environmental context. The hypothesis suggests that weather conditions have become more extreme over recent years, potentially resulting in an overall trend. Determining such trends is challenging because local effects often dominate. To mitigate this, data is spatially stacked, involving averaging all seismic data for a given year. This approach generates robust attenuation time series, allowing for trend analysis and the identification of annual minima and maxima. However, it does not enable the identification of potential subpatterns within the region. The study will use both the raw attenuation data and the processed data to explore these subpatterns, as distinct variations may exist between the crater region and the area surrounding the lake, among others.<br>

By addressing these goals, this project aims to contribute to our understanding of seismic and climatic influences on the Mt. St. Helens region, providing valuable insights into volcanic and environmental changes. The analysis mostly bases on originally seismic ground velocity data which are converted in a measure for seismic attenuation. This convertion is not part of this project.

## Installation

## Data structure
This project is structured in the way that we have a folder ```code``` where you can find the jupyter notebooks or python scripts. The folder ```data``` contains some example files. In our case we do have .csv files of the preprocessed seismic data. Each file contains the data of one seismic station and one year. The column headers indicate different parameters extracted from seismic time series. The rows represent time windows of 10 minutes. The ```doc``` folder contains some informations about the project.<br>

Some abbreviations:<br>
- **RSAM:** Real-Time Seismic Amplitude Measurement is a measure of **seismic energy**. We get it by taking seismic groud velocity (that is what a seismometer measures) and apply a bandpass filter to end. The filtered time series then is cut into 10 minute long time windows and the mean of the absolute values than is the RSAM. Our example data has three different RSAM time series (RSAM, MF, HF). Each time series is filtered in a different frequency range (2-5 Hz, 4.5-8 Hz, 8-16Hz). These frequency bands are typical for volcano seismology.
- **DSAR:** Displacement Seismic Amplitude Ratio is a measure for **attenuation**. We get ground displacement by integrating seismic ground velocity. We apply the same bandpass filters as for RSAM. To get an wave attenuation (we assume that the seismic source does not change and the wave attenuation is simply due to changes of the underground) we devide a low frequency band by a high frequency band. For DSAR it is MF/HF, lDSAR is RSAM/MF, lhDSAR is RSAM/HF. VSAR and lhVSAR follows the same procedure without the convertion from ground velocity to ground displacement.
- **RMS:** Root Mean Square is also a measure of emitted **seismic energy** but over the whole detectable frequency range. The RMS is calculated over 10 minute long time windows.
- **RMeS:** Root Median Square is similar to RMS but more robust to individual outliers because we take the median instead of the mean.
- **PGV:** Peak Ground Velocity is giving you the maximum absolute value in the 10 minute time window of the seismig ground velocity time series.
- **PGA:** Peak Ground Acceleration is giving you the maximum absolute value in the 10 minute time window after deviate the seismig ground velocity time series.
- **zsc:** z-score normalization is a technique that scales the measurement point of a feature to have a mean of 0 and a standard deviation of 1. This is done by subtracting the mean of the feature from each measurement point, and then dividing by the standard deviation. We do this in the log-space

## Code strucutre

## Tutorial
