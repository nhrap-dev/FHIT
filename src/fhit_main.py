'''
2021 Colin Lindeman NiyamIT
Flood Hazard Import Tool FHIT

TODO: finalize creating storm,adv,file lists
'''

import os
import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import json
import xml.etree.ElementTree as ET

def getHazusHazardInputPath():
    """ Checks the Hazus settings.xml for the path to HazardInput

        Keyword Arguments:
            None

        Returns:
            HazusHazardInputPath: str -- The path to HazardInput directory.

        Note: This reads the fhit_settings.json file for the hazus path. User
        can edit the fhit_settings.json if their install didn't use default paths.
    
    """
    try:
        with open("fhit_settings.json") as f:
            fhitSettings = json.load(f)
    except:
        with open("./src/fhit_settings.json") as f:
            fhitSettings = json.load(f)
    settingsPath = fhitSettings['HAZUSSettingsXmlPath']
    tree = ET.parse(settingsPath)
    root = tree.getroot()
    for element in root.findall('General/HazardFolderPath'):
        HazusHazardInputPath = element.text
    return HazusHazardInputPath

def createHazardInputSurgeRiverineFolder(HazusHazardInputPath, hazardInputType):
    """ Checks if 'Surge' or 'Riverine' folders exist in HazardInput folder, creates
            them if they don't exist.

        Keyword Arguments:
            HazusHazardInputPath: str -- the path to hazus HazardInput directory
            hazardInputType: str -- 's' for surge, 'r' for riverine

        Returns:
            nothing: na -- Creates a directory

        Note: 
    
    """
    if hazardInputType == 'r':
        hazardInputType = 'Riverine'
    elif hazardInputType == 's':
        hazardInputType = 'Surge'
    else:
        raise Exception("hazardInputType Error: Enter 's' for surge or 'r' for riverine. You entered {hazardInputType}.") 
    hazardInputPath = os.path.join(HazusHazardInputPath, hazardInputType)
    if not os.path.exists(hazardInputPath):
        print(f"{hazardInputPath} does not exist, creating...")
        os.mkdir(hazardInputPath)
        print(f"{hazardInputPath} created.")
    else:
        print(f"{hazardInputPath} exists.")

def connectToAwsS3(bucketname):
    """ Creates a s3 boto client from a given AWS S3 Bucket

        Keyword Arguments:
            bucketname: str -- the subdomain of the url.
            I.E. hazus for https://hazus.s3.us-east-2.amazonaws.com/

        Returns:
            s3Objects: s3 Boto client -- 

        Note: 
    
    """
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3Objects = s3.list_objects(Bucket=bucketname)
    return s3Objects

def getListofKeys(s3Objects):
    """ Creates a table of storms, advisories and depth grid rasters

        Keyword Arguments:
            s3Objects: ? -- Data from the s3 bucket

        Note: THIS is not working, look into using pandas
    """
    stormDict = {}
    for x in s3Objects['Contents']:
        key = x['Key']
        keyFileType = key.split(".")[-1]
        if keyFileType == 'tif':
            splitKey = key.split("/")
            Name = splitKey[0]
            Advisory = splitKey[1]
            tifFile = splitKey[2]
            print(Name,Advisory,tifFile)
            stormDict[Name] = {Advisory:[tifFile]}
    return stormDict

def getStormList(stormDict):
    stormList = stormDict.keys()
    return stormList

def getAdvisoryList(stormDict, stormName):
    advisoryList = stormDict[stormName].keys()
    return advisoryList

def getFileList(stormDict, stormName, advisory):
    fileList = stormDict[stormName][advisory]
    return fileList

def downloadAwsS3File(bucketName, key, downloadPath):
    """ Downloads specified file from AWS S3 buckets

        Keyword Arguments:
            bucketName: str -- name of s3 bucket, ie 'hazus'
            key: str -- name of file to download, ie 'laura/00/laura_hc00.tif'
            downloadPath: str -- path of folder to download to ie 'C:/HazusData/HazardInput/Riverine'
            downloadFileName: str -- name of downloaded file

        Note: 
    """   
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    fileName = key.split('/')[-1]
    downloadPathFileName = os.path.join(downloadPath,fileName)
    try:
        s3.Bucket(bucketName).download_file(key, downloadPathFileName)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

if __name__ == "__main__":
    import json
    
    #get info from fhit settings file...
    try:
        with open("fhit_settings.json") as f:
            fhitSettings = json.load(f)
    except:
        with open("./src/fhit_settings.json") as f:
            fhitSettings = json.load(f)
    
    data = connectToAwsS3(fhitSettings['ADCIRCAwsBucket'])
    getStormAdvDepthGrids(data)
    downloadAwsS3File('hazus', 'laura/00/laura_hc00.tif', r'C:\HazusData\HazardInput')
    
