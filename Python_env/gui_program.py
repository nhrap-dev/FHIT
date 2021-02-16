'''
2021 Colin Lindman NiyamIT
Flood Hazard Import Tool FHIT GUI
Python 3

TODO:
-add code to main script to import actual data
-build up import button to set off processing of the chosen data
-icons https://teams.microsoft.com/_#/files/General?threadId=19%3A4f2ec634fe3245a1bcfec366f1bfb31d%40thread.skype&ctx=channel&context=NewGraphics&rootfolder=%252Fsites%252FHazusToolDevelopment%252FShared%2520Documents%252FGeneral%252FInterface%252FNewGraphics

Choosing the type sets the download location
Choosing the source sets off getting the list of files for that source
choosing the storm filters the file list
choosing the file to import sets off the settings check, dir check and creation, download
'''

import tkinter as tk
from tkinter import ttk
import fhit_functions as fhit
#from windows import set_dpi_awareness

#set_dpi_awareness()

class floodHazardImportTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Flood Hazard Import Tool")
        self.frames = dict()
        
        self.floodHazardType = tk.StringVar()
        self.floodHazardDataSource = tk.StringVar()
        self.stormSelection = tk.StringVar()
        self.advisorySelection = tk.StringVar()
        self.floodDepthGridSelection = tk.StringVar()
        
        self.stormList = ['Choose a storm...'] #if these are empty lists, it crashes the gui
        self.advisoryList = ['Choose an advisory...']
        self.fileList = ['Choose a file...']
        
        self.resizable(False, False)
        
        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky="EW")

        for frameClass in (floodHazardType, floodHazardDataSource, stormSelection, advisorySelection, floodDepthGridSelection):
            frame = frameClass(container, self)
            self.frames[frameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.showFrame(floodHazardType)

    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class floodHazardType(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.floodHazardType = tk.StringVar()

        self.labelFrame = ttk.Label(self, text="1. FLOOD HAZARD TYPE")
        self.labelDirections = ttk.Label(self, text="What type of flood hazard data are you looking for?")
        self.coastalSurgeRButton = ttk.Radiobutton(self, variable=self.floodHazardType,
                                              text="Storm Surge", value="Storm Surge")
        self.coastalSurgeRButton.invoke()
        self.riverineRButton = ttk.Radiobutton(self, variable=self.floodHazardType,
                                          text="Riverine", value="Riverine")
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(floodHazardDataSource)
                                                                   ,self.setFloodHazardType()
                                                                   ,self.printSelection()])

        self.labelFrame.grid(row=1, column=1, columnspan=2, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=2, sticky="EW")
        self.coastalSurgeRButton.grid(row=3, column=1)
        self.riverineRButton.grid(row=4, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}!")
        
    def setFloodHazardType(self):
        root.floodHazardType = self.floodHazardType


class floodHazardDataSource(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.floodHazardDataSource = tk.StringVar()

        self.labelFrame = ttk.Label(self, text="2. FLOOD HAZARD SOURCE")
        self.labelFiller = ttk.Label(self, text="")
        self.labelDirections = ttk.Label(self, text="Please select a data source")
        self.adcircRButton = ttk.Radiobutton(self, variable=self.floodHazardDataSource,
                                              text="ADCIRC", value="ADCIRC")
        self.adcircRButton.invoke()
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(stormSelection)
                                                                       ,self.setFloodHazardDataSource()
                                                                       ,self.setStormList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(floodHazardType))

        self.labelFrame.grid(row=1, column=1, columnspan=2, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=2, sticky="EW")
        self.adcircRButton.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}!")
        print(f"Available Storms: {root.stormList}")
        
    def setFloodHazardDataSource(self):
        root.floodHazardDataSource = self.floodHazardDataSource

    def setStormList(self):
        root.stormList = self.adcircStorms()
        page = self.controller.get_page(stormSelection)
        page.comboboxStorm['values'] = self.controller.stormList #update the list

    def adcircStorms(self):
        adcircKeys = fhit.connectToAwsS3(fhit.getAwsS3BucketName())
        stormDF = fhit.getHazusKeys(adcircKeys)
        storms = fhit.getStormNameList(stormDF)
        return storms


class stormSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.stormSelection = tk.StringVar()

        self.labelFrame = ttk.Label(self, text="3. STORM SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select a storm")
        self.labelFiller = ttk.Label(self, text="")
        self.comboboxStorm = ttk.Combobox(self)
        self.comboboxStorm['values'] = self.controller.stormList
        self.comboboxStorm.config(state='readonly')
        self.comboboxStorm.current(0)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(advisorySelection)
                                                                       ,self.setStormSelection()
                                                                       ,self.setAdvisoryList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(floodHazardDataSource))

        self.labelFrame.grid(row=1, column=1)
        self.labelDirections.grid(row=2, column=1)
        self.comboboxStorm.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}, {root.stormSelection.get()}!")
        print(f"Available Advisories: {root.advisoryList}")

    def setStormSelection(self):
        self.stormSelection.set(self.comboboxStorm.get())
        root.stormSelection = self.stormSelection

    def setAdvisoryList(self):
        root.advisoryList = self.adcircAdvisories()
        page = self.controller.get_page(advisorySelection)
        page.comboboxAdvisory['values'] = self.controller.advisoryList #update the list

    def adcircAdvisories(self):
        adcircKeys = fhit.connectToAwsS3(fhit.getAwsS3BucketName())
        stormDF = fhit.getHazusKeys(adcircKeys)
        advisories = fhit.getStormNameAdvisoryList(stormDF, root.stormSelection.get())
        return advisories


class advisorySelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.advisorySelection = tk.StringVar()
        
        self.labelFrame = ttk.Label(self, text="4. ADVISORY SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select an advisory")
        self.labelFiller = ttk.Label(self, text="")
        self.comboboxAdvisory = ttk.Combobox(self)
        self.comboboxAdvisory['values'] = self.controller.advisoryList
        self.comboboxAdvisory.config(state='readonly')
        self.comboboxAdvisory.current(0)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(floodDepthGridSelection)
                                                                       ,self.setAdvisorySelection()
                                                                       ,self.setFileList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(stormSelection))

        self.labelFrame.grid(row=1, column=1)
        self.labelDirections.grid(row=2, column=1)
        self.comboboxAdvisory.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}, {root.stormSelection.get()}, {root.advisorySelection.get()}!")
        print(f"Available Files: {root.fileList}")
        
    def setAdvisorySelection(self):
        self.advisorySelection.set(self.comboboxAdvisory.get())
        root.advisorySelection = self.advisorySelection

    def setFileList(self):
        root.fileList = self.adcircFiles()
        page = self.controller.get_page(floodDepthGridSelection)
        page.comboboxFloodDepthGrid['values'] = self.controller.fileList #update the list
        
    def adcircFiles(self):
        adcircKeys = fhit.connectToAwsS3(fhit.getAwsS3BucketName())
        stormDF = fhit.getHazusKeys(adcircKeys)
        files = fhit.getStormNameAdvisoryFileList(stormDF, root.stormSelection.get(), root.advisorySelection.get())
        print(f"{root.stormSelection.get()} {root.advisorySelection.get()}")
        return files

class floodDepthGridSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.floodDepthGridSelection = tk.StringVar()
        
        self.labelFrame = ttk.Label(self, text="5. FLOOD DEPTH GRIDS")
        self.labelDirections = ttk.Label(self, text="Please select a depth grid")
        self.labelFiller = ttk.Label(self, text="")
        self.comboboxFloodDepthGrid = ttk.Combobox(self)
        self.comboboxFloodDepthGrid.config(values=self.controller.fileList)
        self.comboboxFloodDepthGrid.config(state='readonly')
        self.comboboxFloodDepthGrid.current(0)
        self.importButton = ttk.Button(self, text="Import", command=lambda:[self.setFloodDepthGridSelection()
                                                                           ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(advisorySelection))

        self.labelFrame.grid(row=1, column=1)
        self.labelDirections.grid(row=2, column=1)
        self.comboboxFloodDepthGrid.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.importButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}, {root.stormSelection.get()}, {root.advisorySelection.get()}, {root.floodDepthGridSelection.get()}!")
        
    def setFloodDepthGridSelection(self):
        self.floodDepthGridSelection.set(self.comboboxFloodDepthGrid.get())
        root.floodDepthGridSelection = self.floodDepthGridSelection
        #root.floodDepthGridSelection.set(self.floodDepthGridSelection)  #this makes PY_VAR7

if __name__ == "__main__":
    root = floodHazardImportTool()
    root.mainloop()
