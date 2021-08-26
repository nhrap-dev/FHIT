'''2021 colin lindeman clindeman@niyamit.com, colin.lindeman@gmail.edu
Python 3, hazus_env
'''

import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import tkinter as tk
import tkinter.ttk as ttk

def popupmsgNextSteps(msg):
    """ Creates a tkinter popup message window

        Keyword Arguments:
            msg: str -- The message you want to display

        Note: this one is intended to have the next steps graphic
        and instructions
    """
    popup = tk.Toplevel()
    popup.grab_set()
    popup.wm_title("!")
    popup.resizable(0,0)

    label = ttk.Label(popup, text=msg)
    label.grid(row=1,column=0,padx=10,pady=10)
    
    okayButton = ttk.Button(popup, text="Okay", command = popup.destroy)
    okayButton.grid(row=3,column=0,padx=10,pady=20)
    
    popup.mainloop()

def GetHazusHazardInputPath():
    """ Checks the Hazus settings.xml for the path to HazardInput

        Returns:
            HazusHazardInputPath: str -- The path to HazardInput directory.

        Note: This reads the fhit_settings.json file for the hazus path. User
        can edit the fhit_settings.json if their install didn't use the default path.
    """
    try:
        with open("config.json") as f:
            fhitSettings = json.load(f)
    except:
        with open("./Python_env/config.json") as f:
            fhitSettings = json.load(f)
    settingsPath = fhitSettings['hazus_settings_path']
    
    tree = ET.parse(settingsPath)
    root = tree.getroot()
    for element in root.findall('General/HazardFolderPath'):
        HazusHazardInputPath = element.text
    return HazusHazardInputPath

def CreateHazardInputTypeFolder(HazusHazardInputPath, hazardInputType):
    """ Checks if 'Surge' or 'Riverine' folders exist in HazardInput folder, creates
            them if they don't exist.

        Keyword Arguments:
            HazusHazardInputPath: str -- the path to hazus HazardInput directory
            hazardInputType: str -- 's' for surge, 'r' for riverine

        Returns:
            nothing: na -- Creates a directory
    """
    if hazardInputType.lower() == 'riverine':
        hazardInputType = 'riverine'
    elif hazardInputType.lower() == 'storm surge':
        hazardInputType = 'surge'
    elif hazardInputType.lower() == 'coastal':
        hazardInputType = 'coastal'
    else:
        raise Exception(f"Enter 'surge' for surge or 'riverine' for riverine or 'Coastal' for Coastal. You entered {hazardInputType}.") 
    hazardInputPath = os.path.join(HazusHazardInputPath, hazardInputType)
    if not os.path.exists(hazardInputPath):
        print(f"{hazardInputPath} does not exist, creating...")
        os.mkdir(hazardInputPath)
        print(f"{hazardInputPath} created.")
    else:
        print(f"{hazardInputPath} exists.")

def HazardFolderPath(HazusHazardInputPath, hazardInputType):
    """Creates the full directory string for the hazardinputtype.

        Keyword Arguments:
            HazusHazardInputPath: str -- the path to hazus HazardInput directory
            hazardInputType: str -- the user selected hazard input type

        Returns:
            hazardInputPath: str -- full path to given hazard input folder

        Note: 
            C:\HazusData\HazardInput\Surge
            C:\HazusData\HazardInput\Riverine
    """
    if hazardInputType.lower() == 'riverine':
        hazardInputType = 'riverine'
    elif hazardInputType.lower() == 'coastal':
        hazardInputType = 'coastal'
    elif hazardInputType.lower() == 'storm surge':
        hazardInputType = 'surge'
    else:
        raise Exception(f"Enter 'Surge' for surge or 'Riverine' for riverine or 'Coastal' for Coastal. You entered {hazardInputType}.")
    hazardInputPath = os.path.join(HazusHazardInputPath, hazardInputType)
    return hazardInputPath

if __name__ == "__main__":
    print(GetHazusHazardInputPath())
    print()
