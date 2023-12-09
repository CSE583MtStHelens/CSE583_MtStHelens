## Functional specification of the MtStHelens from SeismoMech
Team: Yash Bhangale, Shreeya Gadgil, Manuela Köpfli, Callum Keddie, Guiliang Zheng
Course Project: CSE 583 | Team Repo: https://github.com/CSE583MtStHelens/CSE583_MtStHelens

# Background
<img align="right" width="400" src=https://github.com/CSE583MtStHelens/CSE583_MtStHelens/assets/107423514/87e29a01-e5bd-45ab-be13-c0c8d70b653f>
Mount St. Helens, located in the Cascade Range, is a stratovolcano with a significant eruption history. The eruption of 2004 lasted for four years and began with a notable shallow earthquake swarm on September 23, 2004. Just one week later, the first explosion occurred on October 1, 2004. Subsequent months saw increased seismic activity at the volcano, including volcanic earthquakes, tremors, and debris flow. These volcanic events exhibited a dominant frequency of approximately 10 Hz. This heightened volcanic activity continued over the next two years (2005 and 2006), during which multiple domes formed within the crater (figure below, gray period). From image data, the magma extrusion rate was estimated. However, in line with the decreased seismicity, the magma extrusion rates also declined. Volcanologists officially declared the end of the eruption in February 2008. 
<br>
<br>
<br>
The seismic data collected during the volcanic activity is just one part of a more extensive dataset. Even before the eruption, a network of seismometers was monitoring the underground. During the eruption, the seismic network underwent dynamic changes involving instrument failures, replacements, and density enhancements. Post-eruption, some instruments were removed. Overall, the seismic network boasts remarkable data density, with time series spanning over 22 years. These time series provide insights into long-term underground changes, which will serve as a foundation for further analyses.
<img src=https://github.com/CSE583MtStHelens/CSE583_MtStHelens/assets/107423514/e48949a2-3148-4007-8dd9-0b0c07f8aaf5>

# User Profile
The users will be seismological researchers. Those researchers will want to apply our software tool to their specific data. The purpose of our software is to find the correlations between the seismic attenuation and magma extrusion and also to analyze the correlations between the change of the climatic patterns with volcanic activities. The user will need to feed their pre-processed seismological data in the software tool with same data structure as the example_data_eruption.csv file provided in the example_data folder. The expected user will have skills to distinguish the differences between their data structure and the data structure in our tool, and perform pre-processing process on their data using python. Our user will expect the tool to be easy to use and the tool would be able to handle input data that are scalable in time and space. 

# Data Souces
Our data source is from the seismological data of Mount St Helens from the year 2000 to the year 2022. We have 8 different types of seismological data that were taken from different seismological stations in the Mount St Helens areas. We also had extrusion rate data during its eruption estimated by photographs taken during the eruption period. Due to the size of our actual data sets, for the purpose of this project, we created synthetic data with the same data structure as the authentic data for demonstration purposes. The example_tutorial.ipynb demonstrates how the synthetic data was being processed by our functions, and the authentic data can be processed in the same way. The data was structured in such a way that there will be different .csv files for different types of seismic data, and in each .csv file, the index for each row will be time recorded for every ten minutes across more than two decades, and the columns will be data taken from different seismic stations scattered in a volcanic region. 

# Use Cases
- Objective of the user interaction
    1. A seismic researcher tries to find out the correlations between the seismic attenuation and the magma extrusion rate during the eruption of a volcano. 

    2. A seismic researcher tries to find out the correlations between the change in climatic patterns and different types of seismological data. 

 - the expected interactions between the user and your systems
    1. The researcher will have both the seismic attenuation data and the volcanic dome extrusion rate data, and generate a nice plot using our tool to find out the correlations between those two parameters. The research could also potentially predict the dome extrusion rate which is a strong indication of the volcanic activity from the cumulated seismic data. 

    2. The researcher will have different types of typical seismic data, and use our tool to find whether those data have correlations with the changes in climatic pattern. If a strong indication of correlations exists, the researcher can indicate that before the volcanic eruption, certain changes in climatic patterns over different times of the year might occur. 

