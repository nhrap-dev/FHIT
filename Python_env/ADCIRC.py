'''2021 colin lindeman clindeman@niyamit.com colin.lindeman@hawaii.edu
Python 3, hazus_env
'''
import os
from pathlib import Path
import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import json
import xml.etree.ElementTree as ET
import pandas as pd


class ADCIRC:
    def __init__(self):
        self.data = self.get_data()

    def get_awss3bucket_name(self):
        """ Checks the Hazus settings.xml for the name to AwsBucket

            Keyword Arguments:
                None

            Returns:
                ADCIRCAwsBucket: str -- The path to ADCIRC AWS S3 bucket.

            Note: This reads the fhit_settings.json file for the bucket name. User
            can edit the fhit_settings.json if the value changes.
        
        """
        with open(os.path.join(Path(__file__).parent, "fhit_settings.json")) as f:
            fhit_settings = json.load(f)
        return fhit_settings['ADCIRCAwsBucket']

    def connect_to_awss3(self, bucket_name):
        """ Creates a s3 boto client from a given AWS S3 Bucket

            Keyword Arguments:
                bucketname: str -- the subdomain of the url.
                I.E. hazus for https://hazus.s3.us-east-2.amazonaws.com/

            Returns:
                s3Objects: s3 Boto client -- 

            Note: 
        
        """
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        s3_Objects = s3.list_objects(Bucket=bucket_name)
        return s3_Objects

    def parse_adcirc_filename(self, file_name):
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
            file_path = Path(file_name)
            file_stem = file_path.stem #remove suffix; i.e. .tiff
            
            file_dict = {}
            file_stem_split = file_stem.split('_')
            if len(file_stem_split) == 11:
                raster_info = file_stem_split[10].split('.')
                if len(raster_info) == 5:
                    file_dict['StormNumber'] = file_stem_split[0]
                    file_dict['Advisory'] = file_stem_split[1]
                    file_dict['GridNameAbbrev'] = file_stem_split[2]
                    file_dict['Machine'] = file_stem_split[3]
                    file_dict['WindModel'] = file_stem_split[4]
                    file_dict['WaveModel'] = file_stem_split[5]
                    file_dict['EnsName'] = file_stem_split[6]
                    file_dict['Operator'] = file_stem_split[7]
                    file_dict['Machine'] = file_stem_split[8]
                    file_dict['Other'] = file_stem_split[9]
                    file_dict['res'] = raster_info[0]
                    file_dict['ulla'] = raster_info[1]+'.'+raster_info[2]
                    file_dict['nx'] = raster_info[3]
                    file_dict['ny'] = raster_info[4]
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
                    return None
            else:
                return None
        except Exception as e:
            return None

    def parse_adcirc_key(self, key):
        '''Parses a ADCIRC amazonaws s3 Key for metadata. Uses parseADCIRCFileName().

        Keyword Arguments:
            key: str -- Key value

        Returns:
            key_dict: dict -- a set dictionary of metadata

        Notes:
            Synoptic keys do not contain basin. Need to determine somehow.
            Tropical keys do not contain day, hour. Need to lookup via advisory number.
        '''
        try:
            key_path = Path(key)
            try:
                int(key_path.parts[0]) #if the first value is not an integer, i.e. a year value, then skip that key
                key_dict = self.parse_adcirc_filename(key_path.name)
                key_dict['filename'] = key_path.name
                key_dict['year'] = key_path.parts[0]
                key_dict['filetype'] = key_path.suffix[1:]
                return key_dict
            except:
                return None
        except Exception as e:
            return None

    def get_adcirc_data(self, s3_objects):
        """ Create an empty dataframe to append s3object keys to it. Only keys
            with a filetype of 'tif' and 'tiff' are appended.

            Keyword Arguments:
                s3_objects: s3Objects -- s3object from boto3

            Returns:
                storm_dataframe: pandas dataframe -- A dataframe of the s3ojbects keys
        """
        try:
            storm_dataframe = pd.DataFrame(columns = ['key']) 
            for s3_object in s3_objects['Contents']:
                key_file_type = Path(s3_object['Key']).suffix[1:]
                if key_file_type in ('tif','tiff'):
                    try:
                        key_dict = self.parse_adcirc_key(s3_object['Key'])
                        key_dict['key'] = s3_object['Key']
                        key_dict['size'] = s3_object['Size']
                        key_dict['lastmodified'] = s3_object['LastModified']
                        storm_dataframe = storm_dataframe.append(key_dict, ignore_index=True)
                    except:
                        continue
            return storm_dataframe
        except Exception as e:
            print('Exception getHazusKeys:', e)

    def get_data(self):
        '''Get the ADCIRC Data

            Returns:
                storm_dataframe: pandas dataframe -- A dataframe of the s3ojbects keys
        '''
        return self.get_adcirc_data(self.connect_to_awss3(self.get_awss3bucket_name()))

    def get_year_list(self):
        '''Get a list of years data that are availalbe

            Returns:
                year_list: python list -- a list of years available
        '''
        year_list = self.data.year.unique().tolist()
        return year_list

    def get_storm_list(self, year):
        '''Get a list of stormNumbers that are available given a year

            Keyword Arguments:
                year: string -- the year to filter data

            Returns:
                storm_number_list: python list -- a list of stormNumber values
        '''
        try:
            storm_numbers = self.data.query(f"year == '{year}'")
            storm_number_list = storm_numbers.StormNumber.unique().tolist()
            if len(storm_number_list) > 0:
                return storm_number_list
            else:
                return None
        except:
            return None

    def get_advisory_list(self, year, storm_number):
        '''Get a list of advisories that are available for a given year and stormNumber

            Keyword Arguments:
                year: string -- the year to filter data
                stormNumber: string -- the stormNumber to filter data

            Returns:
                advisory_list: python list -- a list of advisories for the filtered year and stormNumber
        '''
        try:
            advisories = self.data.query(f"year == '{year}' and StormNumber == '{storm_number}'")
            advisory_list = advisories.Advisory.unique().tolist()
            if len(advisory_list) > 0:
                return advisory_list
            else:
                return None
        except:
            return None

    def get_file_list(self, year, storm_number, advisory):
        '''Get a list of files that are available given a year, stormNumber and advisory

            Keyword Arguments:
                year: string -- the year to filter data
                storm_number: string -- the stormNumber to filter data
                advisory: string -- the advisory to filter data

            Returns:
                file_list: python list -- a list of files for the year, stormNumber, advisory
        '''
        try:
            files = self.data.query(f"year == '{year}' and StormNumber == '{storm_number}' and Advisory == '{advisory}'")
            file_list = files.filename.unique().tolist()
            if len(file_list) > 0:
                return file_list
            else:
                None
        except:
            None

    def get_file_attributes(self, key):
        '''
            Keyword Arguments:
                key: string -- the aws key value

            Returns:
                file_dictionary: dictionary -- a key:value pairing
        '''
        key_dataframe = self.data.query(f"key == '{key}'")
        file_dictionary = key_dataframe.to_dict('records')
        return file_dictionary[0]

    def get_awskey_from_filename(self, year, storm_number, advisory, file_name):
        """ Parses an ADCIRC file name for attributes.

            Keyword Arguments:
                year: string -- the year to filter data
                storm_number: string -- the stormNumber to filter data
                advisory: string -- the advisory to filter data
                file_name: string -- the name of the file

            Returns:
                aws_key: str -- a AWS S3 key

            Note: See the ASGS Raster AWS conventions pdf
        """
        file = self.data.query(f"year == '{year}' and StormNumber == '{storm_number}' and Advisory == '{advisory}' and filename == '{file_name}'")
        aws_key = file.key.unique()
        return aws_key[0]

    def download_awss3_file(self, bucket_name, key, download_path):
        """ Downloads specified file from AWS S3 buckets

            Keyword Arguments:
                bucket_name: str -- name of s3 bucket, ie 'hazus'
                key: str -- name of file to download, ie 'laura/00/laura_hc00.tif'
                download_path: str -- path of folder to download to ie 'C:/HazusData/HazardInput/Riverine'
                download_path_file_name: str -- name of downloaded file

            Note: 
        """   
        s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
        file_name = key.split('/')[-1]
        download_path_file_name = os.path.join(download_path, file_name)
        try:
            s3.Bucket(bucket_name).download_file(key, download_path_file_name)
            popupmsgNextSteps(f'''File "{key}" is now available in Hazus''')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise



if __name__ == "__main__":

    test = ADCIRC()

    print('TEST 1')
    print(test.data)
    print()
    
    print('TEST 2')
    print(test.get_year_list())
    print()

    print('TEST 3')
    for year in test.get_year_list():
        print(year, test.get_storm_list(year))
    print()

    print('TEST 4')
    for year in test.get_year_list():
        for storm in test.get_storm_list(year):
            print(year, storm, test.get_advisory_list(year, storm))
    print()

    print('TEST 5')
    for year in test.get_year_list():
        for storm in test.get_storm_list(year):
            for advisory in test.get_advisory_list(year, storm):
                print(year, storm, advisory, test.get_file_list(year, storm, advisory))
    print()

    print('TEST 6')
    for year in test.get_year_list():
        for storm in test.get_storm_list(year):
            for advisory in test.get_advisory_list(year, storm):
                for file in test.get_file_list(year, storm, advisory):
                    fileAttributes = test.get_file_attributes(test.get_awskey_from_filename(year, storm, advisory, file))
                    print(fileAttributes['filename'])
                    print(fileAttributes['WeatherType'], fileAttributes['nx'], fileAttributes['ny'], fileAttributes['res'], fileAttributes['size'])
    print()