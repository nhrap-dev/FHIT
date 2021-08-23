import os
import json
from pathlib import Path

class tropical_storm_lookup:
    def __init__(self):
        self.atlantic = self._get_basin_names("atlantic.json")
        self.central_north_pacific = self._get_basin_names("centralnorthpacific.json")
        self.eastern_north_pacific = self._get_basin_names("easternnorthpacific.json")

    def _get_basin_names(self, file_name:str) -> dict:
        """
        """
        with open(os.path.join(Path(__file__).parent, "TropicalStormNames", file_name)) as f:
            basin_names = json.load(f)
        return basin_names

    def lookup_name(self, basin_abbr:str, storm_number:str, year:str):
        """
        """
        basin_abbr = str(basin_abbr)
        storm_number = str(storm_number)
        year = str(year)
        default_name = basin_abbr + storm_number + year
        if basin_abbr.lower() == "al":
            basin = "Atlantic "
            if int(storm_number) > 21:
                year = "supplemental"
                storm_number = str(int(storm_number) - 21).zfill(2)
            year_list = self.atlantic.get(year)
            if year_list:
                name = year_list.get(storm_number)
                if name:
                    return basin + name + f" [{default_name}]"
        if basin_abbr.lower() == "cp":
            basin = "Central Pacific "
            if int(storm_number) > 48:
                storm_number = str(int(storm_number) - 48).zfill(2)
            name = self.central_north_pacific.get(storm_number)
            if name:
                return basin + name + f" [{default_name}]"
        if basin_abbr.lower() == "ep":
            basin = "Eastern Pacific "
            if int(storm_number) > 21:
                year = "supplemental"
                storm_number = str(int(storm_number) - 21).zfill(2)
            year_list = self.eastern_north_pacific.get(year)
            if year_list:
                name = year_list.get(storm_number)
                if name:
                    return basin + name + f" [{default_name}]"
        return default_name

if __name__ == "__main__":
    test = tropical_storm_lookup()
    print('Atlantic (01-21, 21 supplemental):')
    print("al012021", test.lookup_name(basin_abbr="al", storm_number="01", year="2021"))
    print("al222021", test.lookup_name(basin_abbr="al", storm_number="22", year="2021"))
    print("al432021", test.lookup_name(basin_abbr="al", storm_number="43", year="2021"))
    print()
    print('Central North Pacific (01-48, repeats):')
    print("cp012021", test.lookup_name(basin_abbr="cp", storm_number="01", year="2021"))
    print("cp482021", test.lookup_name(basin_abbr="cp", storm_number="48", year="2021"))
    print("cp492021", test.lookup_name(basin_abbr="cp", storm_number="49", year="2021"))
    print()
    print("Eastern North Pacific (01-24, 24 supplemental):")
    print("ep012021", test.lookup_name(basin_abbr="ep", storm_number="01", year="2021"))
    print("ep252021", test.lookup_name(basin_abbr="ep", storm_number="25", year="2021"))
    print("ep492021", test.lookup_name(basin_abbr="ep", storm_number="49", year="2021"))
    print()
    print('These invalid inputs should return the input values, concatentated:')
    print("al011776", test.lookup_name(basin_abbr="al", storm_number="01", year="1776"))
    print("cp1002021", test.lookup_name(basin_abbr="cp", storm_number="100", year="2021"))
    print("ep12021", test.lookup_name(basin_abbr="ep", storm_number="1", year="2021"))
    print("ep",1,"2021", test.lookup_name(basin_abbr="ep", storm_number=1, year="2021"))
    print(8,1,0, test.lookup_name(basin_abbr=8, storm_number=1, year=0))
    print()
    #print("Example code to get value:")
    #print(tropical_storm_lookup().lookup_name(basin_abbr="al", storm_number="01", year="2021"))