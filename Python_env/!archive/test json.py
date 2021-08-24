import os
from pathlib import Path
import json

test_dict = {'StormNumber':None,
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

def rename_dictionary_keys(ugly_dict):
    with open(os.path.join(Path(__file__).parent, "../adcirc_fieldnames.json")) as f:
        replacement_keys = json.load(f)

    pretty_dict = {replacement_keys.get(k, k): v for k, v in ugly_dict.items()}

    return pretty_dict

if __name__ == "__main__":
    x = rename_dictionary_keys(test_dict)
    for key in x:
        print(key)