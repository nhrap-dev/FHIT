'''
2021 Colin Lindeman NiyamIT
Flood Hazard Import Tool FHIT

TODO: finalize download file
'''

import os
import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import json
import xml.etree.ElementTree as ET
import pandas as pd

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
        with open("./Python_env/fhit_settings.json") as f:
            fhitSettings = json.load(f)
    settingsPath = fhitSettings['HAZUSSettingsXmlPath']
    tree = ET.parse(settingsPath)
    root = tree.getroot()
    for element in root.findall('General/HazardFolderPath'):
        HazusHazardInputPath = element.text
    return HazusHazardInputPath

def getAwsS3BucketName():
    #get this from the settings file
    return "hazus"

def createHazardInputTypeFolder(HazusHazardInputPath, hazardInputType):
    """ Checks if 'Surge' or 'Riverine' folders exist in HazardInput folder, creates
            them if they don't exist.

        Keyword Arguments:
            HazusHazardInputPath: str -- the path to hazus HazardInput directory
            hazardInputType: str -- 's' for surge, 'r' for riverine

        Returns:
            nothing: na -- Creates a directory

        Note: 
    
    """
    if hazardInputType.lower() == 'riverine':
        hazardInputType = 'riverine'
    elif hazardInputType.lower() == 'storm surge':
        hazardInputType = 'surge'
    else:
        raise Exception(f"Enter 'surge' for surge or 'riverine' for riverine. You entered {hazardInputType}.") 
    hazardInputPath = os.path.join(HazusHazardInputPath, hazardInputType)
    if not os.path.exists(hazardInputPath):
        print(f"{hazardInputPath} does not exist, creating...")
        os.mkdir(hazardInputPath)
        print(f"{hazardInputPath} created.")
    else:
        print(f"{hazardInputPath} exists.")

def HazardInputTypeFolder(HazusHazardInputPath, hazardInputType):
    if hazardInputType.lower() == 'riverine':
        hazardInputType = 'riverine'
    elif hazardInputType.lower() == 'storm surge':
        hazardInputType = 'surge'
    else:
        raise Exception(f"Enter 'Surge' for surge or 'Riverine' for riverine. You entered {hazardInputType}.")
    hazardInputPath = os.path.join(HazusHazardInputPath, hazardInputType)
    return hazardInputPath

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

def getHazusKeys(s3Objects):
    stormDF = pd.DataFrame(columns = ['name', 'advisory', 'tif', 'key']) 
    for x in s3Objects['Contents']:
        key = x['Key']
        keyFileType = key.split(".")[-1]
        if keyFileType == 'tif':
            splitKey = key.split("/")
            Name = splitKey[0]
            Advisory = splitKey[1]
            tif = splitKey[2]
            stormDF = stormDF.append({'name':Name,'advisory':Advisory,'tif':tif, 'key':key}, ignore_index=True)
    return stormDF

def getStormNameList(stormDF):
    stormNameList = stormDF.name.unique().tolist()
    return stormNameList

def getStormNameAdvisoryList(stormDF, stormName):
    try:
        advisoryList = stormDF.loc[stormDF['name']==stormName].advisory.unique().tolist()
        if len(advisoryList) > 0:
            return advisoryList
        else:
            return ['No advisories found']
    except:
        return ['stormName is invalid']

def getStormNameAdvisoryFileList(stormDF, stormName, advisory):
    try:
        files = stormDF.query(f"name == '{stormName}' and advisory == '{advisory}'")
        fileList = files.key.unique().tolist()
        if len(fileList) > 0:
            return fileList
        else:
            return ['No files found']
    except:
        return ['stormName or advisory is invalid']

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
    pass
    
    
