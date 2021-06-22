'''2021 colin lindeman clindeman@niyamit.com colin.lindeman@hawaii.edu
Python 3, hazus_env
'''

from pathlib import Path

class adcirc:
    def __init__(self):
        self.data = self.getData()

    def getAwsS3BucketName(self):
        """ Checks the Hazus settings.xml for the name to AwsBucket

            Keyword Arguments:
                None

            Returns:
                ADCIRCAwsBucket: str -- The path to ADCIRC AWS S3 bucket.

            Note: This reads the fhit_settings.json file for the bucket name. User
            can edit the fhit_settings.json if the value changes.
        
        """
        try:
            with open("fhit_settings.json") as f:
                fhitSettings = json.load(f)
        except:
            with open("./Python_env/fhit_settings.json") as f:
                fhitSettings = json.load(f)
        return fhitSettings['ADCIRCAwsBucket']

    def connectToAwsS3(self, bucketname):
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

    def getHazusKeys(self, s3Objects):
        """ Create an empty dataframe to append s3object keys to it. Only keys
            with a filetype of 'tif' are appended.

            Keyword Arguments:
                s3Objects: s3Objects -- s3object from boto3

            Returns:
                stormDF: pandas dataframe -- A dataframe of the s3ojbects keys

            Note: 
                Beginning: laura/30/laura_adv30.tif
                Then:   Tropical/Storm#12/Advisory#30/laura_adv30.tif
                Now:    2020/Tropical/al12/28/GAHM/al12_28_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff
        """
        stormDF = pd.DataFrame(columns = ['year', 'weathertype', 'name', 'advisory', 'windmodel', 'tif', 'key']) 
        for x in s3Objects['Contents']:
            key = x['Key']
            keyFileType = key.split(".")[-1]
            if keyFileType in ('tif','tiff'):
                splitKey = key.split("/")
                if len(splitKey) >3:
                    try:
                        Name = splitKey[2]
                        Advisory = splitKey[3]
                        tif = splitKey[-1]
                        stormDF = stormDF.append({'name':Name,'advisory':Advisory,'tif':tif, 'key':key}, ignore_index=True)
                    except Exception as e:
                        print(f"{splitKey}:{e}")
                else:
                    pass
                    #raise Exception(f"splitKey not long enough: {splitKey}")#for debug
        return stormDF

    def getData(self):
        return self.getHazusKeys(self.connectToAwsS3(self.getAwsS3BucketName()))

    def getYearList(self):
        pass

    def getStormList(self, year):
        pass

    def getAdvisoryList(self, year, stormName):
        pass

    def getFileList(self, year, stormName, advisory):
        pass

    def getFileAttributes(self, year, stormName, advisory, fileName):
        pass

def parseADCIRCFileName(fileName):
    '''Parses a ADCIRC Depth Grid file name for metadata

    Keyword Arguments:
        fileName: str -- name of ADCIRC depth grid file

    Returns:
        fileDict: dict -- a set dictionary of metadata

    Notes:
        StormNumber_Advisory_GridNameAbbrev_Machine_WindModel_WaveModel_EnsName_Operator_Machine_Other_RasterCover.tiff
        <WaveModel> = Sqan, Stwave, WW3, None
        <EnsName> = nhcForecast, veerRight1, etc...
        <RasterCover> = $res_in_meters+m, e.g. 50m
    '''
    try:
        fileName = Path(fileName)
        fileName = fileName.stem #remove filetype i.e. .tiff
        
        fileDict = {}
        foo = fileName.split('_')
        if len(foo) == 11:
            rasterInfo = foo[10].split('.')
            if len(rasterInfo) == 5:
                fileDict['StormNumber'] = foo[0]
                fileDict['Advisory'] = foo[1]
                fileDict['GridNameAbbrev'] = foo[2]
                fileDict['Machine'] = foo[3]
                fileDict['WindModel'] = foo[4]
                fileDict['WaveModel'] = foo[5]
                fileDict['EnsName'] = foo[6]
                fileDict['Operator'] = foo[7]
                fileDict['Machine'] = foo[8]
                fileDict['Other'] = foo[9]
                fileDict['res'] = rasterInfo[0]
                fileDict['ulla'] = rasterInfo[1]+'.'+rasterInfo[2]
                fileDict['nx'] = rasterInfo[3]
                fileDict['ny'] = rasterInfo[4]
                try:
                    int(fileDict['StormNumber'])
                    fileDict['WeatherType'] = 'Synoptic'
                    fileDict['advYear'] = fileDict['StormNumber'][0:4]
                    fileDict['advMonth'] = fileDict['StormNumber'][4:6]
                    fileDict['advDay'] = fileDict['StormNumber'][6:8]
                    fileDict['advHour'] = fileDict['Advisory'][0:2]
                except:
                    fileDict['WeatherType'] = 'Tropical'
                    fileDict['Basin'] = fileDict['StormNumber'][0:2]
                    #need a lookup of year, stormname and advisory number to get month, day, hour
                return fileDict
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

def parseADCRICKey(keyValue):
    '''Parses a ADCIRC amazonaws s3 Key for metadata. Uses parseADCIRCFileName().

    Keyword Arguments:
        keyValue: str -- Key value

    Returns:
        keyDict: dict -- a set dictionary of metadata

    Notes:
        Synoptic keys do not contain basin. Needtto determine somehow.
        Tropical keys do not contain day, hour. Need to lookup via advisory number.
    '''
    try:
        keyValue = Path(keyValue)
        keyDict = parseADCIRCFileName(keyValue.name)
        keyDict['Year'] = keyValue.parts[0]
        keyDict['FileType'] = keyValue.suffix[1:]
        return keyDict
        
    except Exception as e:
        return None


if __name__ == "__main__":
##    fileNameTests = ['',
##                     'al12_28_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000',
##                     'al12_28_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff',
##                     'al12_29_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff',
##                     'al12_30_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff',
##                     'al19_18_inunmax_NGOMv19b_GAHM_Swan_nhcConsensus_bde_frontera_None_50.-00915.000310.10000.6000.tiff',
##                     '20180101_00Z_zetamax_ec95d_ERA5_None_reanalysis_bob_hatteras_None_1000.-00785.000355.100.60.tiff',
##                     '20210609_18Z_inunmax_ec95d_nam_swan_namforecast_bob_hatteras_None_1000.-00785.000355.100.60.tiff',
##                     '20210609_18Z_inunmax_ec95d_nam_swan_namforecast_bob_hatteras_None_1000.-00825.000360.500.500.tiff',
##                     '20210609_18Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_100.-00782.000345.1000.1000.tiff',
##                     '20210609_18Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_1000.-00785.000355.100.60.tiff',
##                     '20210609_18Z_zetamax_ec95d_nam_swan_namforecast_bob_hatteras_None_1000.-00785.000355.100.60.tiff'
##                     ]
##    
##    for test in fileNameTests:
##        print("fileName:", test)
##        pineapple = parseADCIRCFileName(test)
##        if pineapple:
##            for key in pineapple:
##                print(key, pineapple[key])
##        else:
##            print('Test Note: Not a valid ADCIRC file name')
##        print()
##
##    keyTests=['',
##              'index.html',
##              '2020/Synoptic/20180101/00Z/ERA5/20180101_00Z_zetamax_ec95d_ERA5_None_reanalysis_bob_hatteras_None_1000.-00785.000355.100.60.tiff',
##              '2020/Tropical/al12/28/GAHM/al12_28_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff',
##              '2020/Tropical/al12/29/GAHM/al12_29_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff',
##              '2020/Tropical/al12/30/GAHM/al12_30_inunmax_lav20a_GAHM_Swan_nhcConsensus_jgf_qbc_None_50.-00915.000310.10000.6000.tiff',
##              '2020/Tropical/al19/18/GAHM/al19_18_inunmax_NGOMv19b_GAHM_Swan_nhcConsensus_bde_frontera_None_50.-00915.000310.10000.6000.tiff',
##              '2021/synoptic/20210609/18Z/nam/20210609_18Z_inunmax_ec95d_nam_swan_namforecast_bob_hatteras_None_1000.-00785.000355.100.60.tiff',
##              '2021/synoptic/20210609/18Z/nam/20210609_18Z_inunmax_ec95d_nam_swan_namforecast_bob_hatteras_None_1000.-00825.000360.500.500.tiff',
##              '2021/synoptic/20210609/18Z/nam/20210609_18Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_100.-00782.000345.1000.1000.tiff',
##              '2021/synoptic/20210609/18Z/nam/20210609_18Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_1000.-00785.000355.100.60.tiff',
##              '2021/synoptic/20210609/18Z/nam/20210609_18Z_zetamax_ec95d_nam_swan_namforecast_bob_hatteras_None_1000.-00785.000355.100.60.tiff'
##              ]
##    for test in keyTests:
##        print("key:", test)
##        pineapple = parseADCRICKey(test)
##        if pineapple:
##            for key in pineapple:
##                print(key, pineapple[key])
##        else:
##            print('Test Note: Not a valid ADCIRC key')
##        print()
