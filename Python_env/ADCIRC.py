'''2021 colin lindeman clindeman@niyamit.com, colin.lindeman@gmail.edu
Python 3, hazus_env
'''

import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import pandas as pd

#TODO update all documentation

class ADCIRC:
    def __init__(self):
        #get pandas dataframe
        self.data = get_adcirc_data().adcirc_dataframe

    def get_year_list(self):
        '''Get a list of years data that are availalbe

            Returns:
                year_list: python list -- a list of years available
        '''
        year_list = self.data.Year.unique().tolist()
        return year_list

    def get_storm_list(self, year:str, weathertype:str):
        '''Get a list of stormNumbers that are available given a year

            Keyword Arguments:
                year: string -- the year to filter data
                weathertype: string -- the weathertype (Synoptic|Tropical)

            Returns:
                storm_number_list: python list -- a list of stormNumber values
        '''
        try:
            storm_numbers = self.data.query(f"Year == '{year}' and WeatherType == '{weathertype}'")
            storm_number_list = storm_numbers.StormNumber.unique().tolist()
            if len(storm_number_list) > 0:
                return storm_number_list
            else:
                return None
        except Exception as e:
            print("Exception get_storm_list: ", e)
            return None

    def get_advisory_list(self, year:str, weathertype:str, storm_number:str):
        '''Get a list of advisories that are available for a given year and stormNumber

            Keyword Arguments:
                year: string -- the year to filter data
                weathertype: string -- the weathertype (synoptic|tropical)
                stormNumber: string -- the stormNumber to filter data

            Returns:
                advisory_list: python list -- a list of advisories for the filtered year and stormNumber
        '''
        try:
            advisories = self.data.query(f"Year == '{year}' and WeatherType == '{weathertype}' and StormNumber == '{storm_number}'")
            advisory_list = advisories.Advisory.unique().tolist()
            if len(advisory_list) > 0:
                return advisory_list
            else:
                return None
        except:
            return None

    def get_file_list(self, year:str, weathertype:str, storm_number:str, advisory:str):
        '''Get a list of files that are available given a year, stormNumber and advisory

            Keyword Arguments:
                year: string -- the year to filter data
                weathertype: string -- the weathertype (synoptic|tropical)
                storm_number: string -- the stormNumber to filter data
                advisory: string -- the advisory to filter data

            Returns:
                file_list: python list -- a list of files for the year, stormNumber, advisory
        '''
        try:
            files = self.data.query(f"Year == '{year}' and WeatherType == '{weathertype}' and StormNumber == '{storm_number}' and Advisory == '{advisory}'")
            file_list = files.FileName.unique().tolist()
            if len(file_list) > 0:
                return file_list
            else:
                return None
        except Exception as e:
            print("Exception get_file_list: ", e)
            return None

    def get_file_attributes(self, key:str):
        ''' FIXME

            Keyword Arguments:
                key: string -- the aws key value

            Returns:
                file_dictionary: dictionary -- a key:value pairing
        '''
        key_dataframe = self.data.query(f"key == '{key}'")
        if key_dataframe.empty:
            raise
        else:
            file_dictionary = key_dataframe.to_dict('records')
            return file_dictionary[0]

    def download_asws3_file(self, key, download_path):
        pass

class get_awss3bucket_name:
    """ Checks the Hazus settings.xml for the name to AwsBucket

    Keyword Arguments:
        None

    Returns:
        ADCIRCAwsBucket: str -- The path to ADCIRC AWS S3 bucket.

    Note: This reads the fhit_settings.json file for the bucket name. User
    can edit the fhit_settings.json if the value changes.
        
    """
    def __init__(self):
        with open(os.path.join(Path(__file__).parent, "config.json")) as f:
            config_json = json.load(f)
        self.aws_s3_bucket_name = config_json['adcirc']['aws_s3_bucket_name']

class validate_adcirc_key:
    '''Parses a ADCIRC amazonaws s3 Key for metadata. Uses parseADCIRCFileName().

    Notes:
        Synoptic keys do not contain basin. Need to determine somehow.
        "2021/synoptic/20210803/00Z/nam/20210803_00Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_50.-00776.000367.1700.9500.tiff"

        Tropical keys do not contain day, hour. Need to lookup via advisory number.
        "2021/tropical/al05/30/GAHM/al05_30_wlmax_EGOMv20b_GAHM_None_nhcConsensus_estrabd_frontera_None_50.-00840.000305.6000.10000.tiff"
    '''
    def __init__(self, key:str):
        self.is_valid = self._validate(key)

    def _validate(self, key:str) -> bool:
        try:
            key_path = Path(key)
            try:
                #TODO read config for pattern/validation parameters
                if not int(key_path.parts[0]): 
                    return False #first value should be a year:
                elif not key_path.suffix[1:] in ['tif','tiff']:
                    return False
                #elif ...
                     #return False #should break into x parts
                else:
                    return True
            except:
                return False
        except Exception as e:
            print('Exception validate_adcirc_key:', e)

class validate_adcirc_keys:
    '''FIXME

        Keyword Arguments:
            keys: list -- a list of dictionaries

        Returns:
            valid_keys: list -- a list of dictionaries
    '''
    def __init__(self, keys):
        self.valid_keys = self.validate(keys)

    def validate(self, keys:list) -> list:
        valid_keys = []
        for key in keys:
            if validate_adcirc_key(key['key']).is_valid:
                valid_keys.append(key)
        return valid_keys

class parse_adcirc_key:
    def parse(self, key):
        '''Parses a ADCIRC Depth Grid file name for metadata

        Keyword Arguments:
            fileName: str -- name of ADCIRC depth grid file

        Returns:
            fileDict: dict -- a set dictionary of metadata

        Notes:
            See Docs for more info on ADCIRC file name structure
            Synoptic:
"2021/synoptic/20210803/00Z/nam/20210803_00Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_50.-00776.000367.1700.9500.tiff"

            Tropical:
"2021/tropical/al05/30/GAHM/al05_30_wlmax_EGOMv20b_GAHM_None_nhcConsensus_estrabd_frontera_None_50.-00840.000305.6000.10000.tiff"
    
        '''
        file_dict = {'StormNumber':None,
                    'Advisory':None,
                    'VarName':None,
                    'GridNameAbbrev':None,
                    'Machine':None,
                    'WindModel':None,
                    'WaveModel':None,
                    'EnsName':None,
                    'Operator':None,
                    'Machine':None,
                    'Other':None,
                    'res':None,
                    'ulla':None,
                    'ullo':None,
                    'nx':None,
                    'ny':None,
                    'WeatherType':None,
                    'advYear':None,
                    'advMonth':None,
                    'advDay':None,
                    'Basin':None,
                    'FileType':None,
                    'FileName':None,
                    'Year':None}
        try:
            file_path = Path(key)
            file_name = file_path.name
            file_stem = file_path.stem #remove suffix; i.e. .tiff
            file_stem_split = file_stem.split('_')
            if len(file_stem_split) == 11: #Validation should be moved
                raster_info = file_stem_split[10].split('.')
                if len(raster_info) == 5: #Validation should be moved
                    file_dict['StormNumber'] = file_stem_split[0]
                    file_dict['Advisory'] = file_stem_split[1]
                    file_dict['VarName'] = file_stem_split[2]
                    file_dict['GridNameAbbrev'] = file_stem_split[3]
                    file_dict['WindModel'] = file_stem_split[4]
                    file_dict['WaveModel'] = file_stem_split[5]
                    file_dict['EnsName'] = file_stem_split[6]
                    file_dict['Operator'] = file_stem_split[7]
                    file_dict['Machine'] = file_stem_split[8]
                    file_dict['Other'] = file_stem_split[9]
                    file_dict['res'] = raster_info[0]
                    file_dict['ullo'] = str(float(raster_info[1])*0.1)
                    file_dict['ulla'] = str(float(raster_info[2])*0.1)
                    file_dict['nx'] = raster_info[3]
                    file_dict['ny'] = raster_info[4]
                    file_dict['FileType'] = file_path.suffix[1:]
                    file_dict['FileName'] = file_name
                    file_dict['Year'] = file_path.parts[0]
                    try:
                        int(file_dict['StormNumber'])
                        file_dict['WeatherType'] = 'Synoptic'
                        file_dict['advYear'] = file_dict['StormNumber'][0:4]
                        file_dict['advMonth'] = file_dict['StormNumber'][4:6]
                        file_dict['advDay'] = file_dict['StormNumber'][6:8]
                        file_dict['advHour'] = file_dict['Advisory'][0:2]
                    except:
                        file_dict['WeatherType'] = 'Tropical'
                        file_dict['Basin'] = file_dict['StormNumber'][0:2]
                        #need a lookup of year, stormname and advisory number to get month, day, hour
                    return file_dict
                else:
                    return file_dict
            else:
                return file_dict #default None dictionary
        except Exception as e:
            print('Exception parse_adcirc_key', e)

class attribute_keys:
    def __init__(self, keys:list):
        self.attributed_keys = self.attribute_keys(keys)

    def attribute_keys(self, keys:list) -> list:
        attributed_keys = []
        for key in keys:
            attributes_dict = parse_adcirc_key().parse(key['key'])
            attributed_keys.append({**key, **attributes_dict}) #merge, dictionaries, for python < 3.9
            #attributed_keys.append(key|attributes_dict) #merge dictionaries, requires python 3.9
        return attributed_keys

class get_adcirc_keys:
    def __init__(self, bucket_name):
        self.bucket_connection = self._connect_to_awss3(bucket_name)
        self.adcirc_keys = self.get_adcirc_keys(self.bucket_connection)

    def _connect_to_awss3(self, bucket_name):
        """ Creates a s3 boto client from a given AWS S3 Bucket

            Keyword Arguments:
                bucketname: str -- the subdomain of the url.
                I.E. hazus for https://hazus.s3.us-east-2.amazonaws.com/

            Returns:
                bucket: s3 Boto s3.resource -- 
        """
        try:
            s3 = boto3.resource('s3', config=Config(signature_version=botocore.UNSIGNED))
            bucket = s3.Bucket(bucket_name)
            return bucket
        except Exception as e:
            print("Exception _connect_to_awss3", e)

    def get_adcirc_keys(self, bucket):
        """ Create an empty dataframe to append s3object keys to it. Only keys
            with a filetype of 'tif' and 'tiff' are appended.

            Keyword Arguments:
                bucket: s3.bucket -- s3 bucket from boto3

            Returns:
                ADCIRC_keys: python list -- A list of dictionaries
        """
        try:
            ADCIRC_keys = []
            for obj in bucket.objects.all():
                try:
                    key_dict = {}
                    key_dict['key'] = obj.key
                    key_dict['size'] = obj.size
                    key_dict['last_modified'] = obj.last_modified
                    ADCIRC_keys.append(key_dict)
                except Exception as e:
                    print('Exception obj:', e)
            return ADCIRC_keys
        except Exception as e:
            print('Exception getHazusKeys:', e)

class get_adcirc_data:
    def __init__(self):
        self.bucket_name = get_awss3bucket_name().aws_s3_bucket_name
        self.adcirc_keys = get_adcirc_keys(self.bucket_name).adcirc_keys
        self.adcirc_valid_keys = validate_adcirc_keys(self.adcirc_keys).valid_keys
        self.adcirc_attributed_keys = attribute_keys(self.adcirc_valid_keys).attributed_keys
        self.adcirc_dataframe = pd.DataFrame()
        self.adcirc_dataframe = self.adcirc_dataframe.append(self.adcirc_attributed_keys, ignore_index=True)

class aws:#FIXME
    def get_awskey_from_filename(self, year, weathertype, storm_number, advisory, file_name):
        """ Parses an ADCIRC file name for attributes.

            Keyword Arguments:
                year: string -- the year to filter data
                weathertype: string -- the weathertype (synoptic|tropical)
                storm_number: string -- the stormNumber to filter data
                advisory: string -- the advisory to filter data
                file_name: string -- the name of the file

            Returns:
                aws_key: str -- a AWS S3 key

            Note: See the ASGS Raster AWS conventions pdf
        """
        file = self.data.query(f"year == '{year}' and WeatherType == '{weathertype}' and StormNumber == '{storm_number}' and Advisory == '{advisory}' and filename == '{file_name}'")
        if file.empty:
            print(f"Empty Query Results!: year == '{year}' and WeatherType == '{weathertype}' and StormNumber == '{storm_number}' and Advisory == '{advisory}' and filename == '{file_name}'")
        else:
            aws_key = file.key.unique()
            return aws_key[0]

    def download_awss3_file(self, key, download_path):
        """ Downloads specified file from AWS S3 buckets

            Keyword Arguments:
                key: str -- name of file to download, ie 'laura/00/laura_hc00.tif'
                download_path: str -- path of folder to download to ie 'C:/HazusData/HazardInput/Riverine'
                download_path_file_name: str -- name of downloaded file

            Note: 
        """   
        bucket_name = self.get_awss3bucket_name()
        s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
        file_name = key.split('/')[-1]
        download_path_file_name = os.path.join(download_path, file_name)
        try:
            s3.Bucket(bucket_name).download_file(key, download_path_file_name)
            fhit.popupmsgNextSteps(f'''File "{key}" is now available in Hazus''')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

if __name__ == "__main__":
    component_tests = False
    ADCIRC_class_tests = True

    if component_tests:
        bucket_name = get_awss3bucket_name().aws_s3_bucket_name
        print(bucket_name)
        print()

        keys = get_adcirc_keys(bucket_name).adcirc_keys
        print(f"Number of Keys for {bucket_name}: {len(keys)}")
        print()

        valid_keys = validate_adcirc_keys(keys).valid_keys
        print(f"Number of Valid Keys for {bucket_name}: {len(valid_keys)}")
        print()

        test_key = "2021/synoptic/20210803/00Z/nam/20210803_00Z_inunmax_ncv999wr_nam_swan_namforecast_bob_hatteras_None_50.-00776.000367.1700.9500.tiff"
        print(parse_adcirc_key().parse(test_key))
        print()

        attributed_keys = attribute_keys(valid_keys).attributed_keys
        x = 0
        for key in attributed_keys:
            print(key) 
            x += 1
            if x == 5: 
                break #there can be too many to view
        print()

        dataframe = get_adcirc_data().adcirc_dataframe
        pd.set_option("max_columns", None)
        print(dataframe.head())
        pd.reset_option("max_columns")
        print()

    if ADCIRC_class_tests:
        test = ADCIRC()
        print(test.data.keys())
        print()
        print(test.get_year_list())
        print()
        print(test.get_storm_list("2021", "Synoptic"))
        print()
        print(test.get_storm_list("2021", "Tropical"))
        print()
        print(test.get_advisory_list("2021", "Tropical", "al05"))
        print()
        print(test.get_file_list("2021", "Tropical", "al05", "30"))
        print()
        print(test.get_file_attributes("2021/tropical/al05/30/GAHM/al05_30_wlmax_EGOMv20b_GAHM_None_nhcConsensus_estrabd_frontera_None_50.-00840.000305.6000.10000.tiff"))
        print()

