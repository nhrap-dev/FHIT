# Flood Hazard Import Tool

The Flood Hazard Import Tool FHIT is used to download depth grids for use in Hazus.

## Requirements

The Flood Hazard Import Tool requires Python >3.6, Hazpy (with Boto3 python library), Hazus

## To Use

1. Download zip folder of tool from GitHub, unzip

2. Double click the FHIT.py to run it. It will check if you have the latest hazpy and tool version. 

3. Select your hazard type
4. Select your storm
5. Select your storm advisory
6. Select your depth grid
7. Import you selected depth grid. This will create a 'Riverine' or 'Surge' folder in your HazardInput folder and download the selected depth grid to it

## Documentation

This tool currently only supports ADCIRC depth grids.

## Contact

Issues can be reported through the repository on Github (https://github.com/nhrap-dev/FHIT)

For questions contact fema-hazus-support@fema.dhs.gov
