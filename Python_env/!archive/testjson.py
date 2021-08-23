import json
import os
from pathlib import Path

config_json = json.load(open(os.path.join(Path(__file__).parent, "config.json")))

#print(config_json)
#print()

print(config_json['data_sources'])
print()

for source in config_json['data_sources']:
    print(source)
    print(source["name"])
    print(source["hazard_types"])
print()

for source in config_json['data_sources']:
    if source["name"] == "ADCIRC":
        print()
print()

for type in config_json['hazard_types']:
    print(type)
    for source in config_json['data_sources']:
        if type in source["hazard_types"]:
            print(source["name"])
    print()

for source in config_json['data_sources']:
    if source["name"] == "ADCIRC":
        new_dictionary = source["name"] == "ADCIRC" 
print()

field_name = 'name'
print(dict(filter(lambda x: x[field_name] == "ADCIRC", config_json['data_sources'].items())))