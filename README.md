# Flood Hazard Import Tool (FHIT)

The Flood Hazard Import Tool FHIT is used to download depth grids for use in Hazus modelling of Coastal, Riverine and Storm Surge flooding.

## Requirements

The Flood Hazard Import Tool requires Python >3.6, Hazpy, Hazus, and an internet connection. See the the To Use section on how to install.

## To Use

1. Download zip folder of tool from GitHub, unzip

![Download Release FHIT](Python_env/assets/images/DownloadReleaseFHIT.jpg "Download Release FHIT")

2. Double click the FHIT.py to run it. It will check if you have the latest hazpy and tool version. 

![Run FHIT](Python_env/assets/images/DownloadReleaseFHIT.jpg "Run FHIT")

3. Select your hazard type

![Select Hazard Type](Python_env/assets/images/SelectHazardType.jpg "Select Hazard Type")

4. Select your data source. The search parameters will differ depending on data source

![Select Hazard Source](Python_env/assets/images/SelectHazardSource.jpg "Select Hazard Source")

ADCIRC:

  1. Select your year
    
  ![ADCIRC Select Year](Python_env/assets/images/ADCIRCSelectYear.jpg "ADCIRC Select Year")
    
  2. Select your weather type
    
  ![ADCIRC Select Weather Type](Python_env/assets/images/ADCIRCSelectWeatherType.jpg "ADCIRC Select Waeather Type")
    
  3. Select your storm
    
  ![ADCIRC Select Storm](Python_env/assets/images/ADCIRCSelectStorm.jpg "ADCIRC Select Storm")
    
  4. Select your storm advisory 
    
  ![ADCIRC Select Advisory](Python_env/assets/images/ADCIRCSelectAdvisory.jpg "ADCIRC Select Advisory")
  
 
5. Select Depth Grid File

![File List](Python_env/assets/images/FileList.jpg "File List")
 
You will see the selected files properties once you've selected a file

![File Properties](Python_env/assets/images/FileProperties.jpg "File Properties")

6. Import you selected depth grid. This will create a 'Coastal', 'Riverine' or 'Surge' folder in your HazardInput folder if they do not already exist and download the selected depth grid to it

![Download Success](Python_env/assets/images/DownloadSuccess.jpg "Download Success")

## Documentation

See the files in the Docs folder for additional information. 

This tool currently only supports ADCIRC depth grids.

![ADCIRC File Name FOrmat](images/adcirc_filename.png "ADCIRC File Name Format") 

**2021-Synoptic-20210609-18z**  = YYYYMMDD, 18 hour zulu

**2021-Tropical-al19-30** = 19th storm in the Atlantic in 2021, advisory 30

Avisory **00** is the hindcast data

## Contact

Issues can be reported through the repository on Github (https://github.com/nhrap-dev/FHIT)

For questions contact fema-hazus-support@fema.dhs.gov
