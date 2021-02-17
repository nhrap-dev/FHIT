'''
2021 Colin Lindman NiyamIT
Flood Hazard Import Tool FHIT GUI
Python 3, Boto3, Pandas

This is a GUI that has one main frame and multiple subframes to act like a multipage wizard.

TODO:
-prompt user to overwrite or not?
-give user feedback that file was downloaded successfully or not
-give user feedback/status that the app is doing something, like getting list of storms or downloaded data
-show just the file name and not the key/path at step 5
-adcirc made changes to their folder structure which affects this gui around 2/16/21
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
        self.fileKey = tk.StringVar()
        
        self.stormList = ['Choose a storm...'] #if these are empty lists, it crashes the gui
        self.advisoryList = ['Choose an advisory...']
        self.fileList = ['Choose a file...']

        self.iconbitmap('./images/ICO/24px.ico')
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

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.coastalSurgeRButton.grid(row=3, column=1, sticky="W")
        self.riverineRButton.grid(row=3, column=2, sticky="W")
        self.nextButton.grid(row=4, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}!")
        
    def setFloodHazardType(self):
        self.controller.floodHazardType = self.floodHazardType


class floodHazardDataSource(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.floodHazardDataSource = tk.StringVar()

        self.labelFrame = ttk.Label(self, text="2. FLOOD HAZARD SOURCE")
        self.labelDirections = ttk.Label(self, text="Please select a data source")
        self.adcircRButton = ttk.Radiobutton(self, variable=self.floodHazardDataSource,
                                              text="ADCIRC", value="ADCIRC")
        self.adcircRButton.invoke()
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(stormSelection)
                                                                       ,self.setFloodHazardDataSource()
                                                                       ,self.setStormList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(floodHazardType))

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.adcircRButton.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=4, column=1)
        self.nextButton.grid(row=4, column=2)

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}!")
        print(f"Available Storms: ")
        for storm in self.controller.stormList:
            print(storm)
        
    def setFloodHazardDataSource(self):
        self.controller.floodHazardDataSource = self.floodHazardDataSource

    def setStormList(self):
        self.controller.stormList = self.adcircStorms()
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

        self.labelFrame = ttk.Label(self, text="3. STORM SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select a storm")
        self.comboboxStorm = ttk.Combobox(self)
        self.comboboxStorm['values'] = self.controller.stormList
        self.comboboxStorm.config(state='readonly')
        self.comboboxStorm.current(0)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(advisorySelection)
                                                                       ,self.setStormSelection()
                                                                       ,self.setAdvisoryList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(floodHazardDataSource)
                                                                       ,self.clearComboboxStorm()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.comboboxStorm.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=4, column=1, sticky="E")
        self.nextButton.grid(row=4, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.stormSelection.get()}!")
        print(f"Available Advisories:")
        for x in self.controller.advisoryList:
            print(x)

    def setStormSelection(self):
        self.controller.stormSelection.set(self.comboboxStorm.get())

    def setAdvisoryList(self):
        self.controller.advisoryList = self.adcircAdvisories()
        page = self.controller.get_page(advisorySelection)
        page.comboboxAdvisory['values'] = self.controller.advisoryList #update the list

    def adcircAdvisories(self):
        adcircKeys = fhit.connectToAwsS3(fhit.getAwsS3BucketName())
        stormDF = fhit.getHazusKeys(adcircKeys)
        advisories = fhit.getStormNameAdvisoryList(stormDF, self.controller.stormSelection.get())
        return advisories

    def clearComboboxStorm(self):
        self.comboboxStorm.set('Choose a storm...')


class advisorySelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller
        
        self.labelFrame = ttk.Label(self, text="4. ADVISORY SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select an advisory")
        self.comboboxAdvisory = ttk.Combobox(self)
        self.comboboxAdvisory['values'] = self.controller.advisoryList
        self.comboboxAdvisory.config(state='readonly')
        self.comboboxAdvisory.current(0)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(floodDepthGridSelection)
                                                                       ,self.setAdvisorySelection()
                                                                       ,self.setFileList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(stormSelection)
                                                                       ,self.clearComboboxAdvisory()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.comboboxAdvisory.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=5, column=1, sticky="E")
        self.nextButton.grid(row=5, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.stormSelection.get()}, {self.controller.advisorySelection.get()}!")
        print(f"Available Files:")
        for x in self.controller.fileList:
            print(x)
        
    def setAdvisorySelection(self):
        self.controller.advisorySelection.set(self.comboboxAdvisory.get())

    def setFileList(self):
        self.controller.fileList = self.adcircFiles()
        page = self.controller.get_page(floodDepthGridSelection)
        page.comboboxFloodDepthGrid['values'] = self.controller.fileList #update the list
        
    def adcircFiles(self):
        adcircKeys = fhit.connectToAwsS3(fhit.getAwsS3BucketName())
        stormDF = fhit.getHazusKeys(adcircKeys)
        files = fhit.getStormNameAdvisoryFileList(stormDF, self.controller.stormSelection.get(), self.controller.advisorySelection.get())
        #print(f"{self.controller.stormSelection.get()} {self.controller.advisorySelection.get()}") #for debug
        return files

    def clearComboboxAdvisory(self):
        self.comboboxAdvisory.set('Choose an advisory...')

class floodDepthGridSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller
        
        self.labelFrame = ttk.Label(self, text="5. FLOOD DEPTH GRIDS")
        self.labelDirections = ttk.Label(self, text="Please select a depth grid")
        self.comboboxFloodDepthGrid = ttk.Combobox(self)
        self.comboboxFloodDepthGrid.config(values=self.controller.fileList)
        self.comboboxFloodDepthGrid.config(state='readonly')
        self.comboboxFloodDepthGrid.current(0)
        self.importButton = ttk.Button(self, text="Import", command=lambda:[self.setFloodDepthGridSelection()
                                                                           ,self.printSelection()
                                                                           ,self.downloadFile()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(advisorySelection)
                                                                       ,self.clearComboboxFloodDepthGrid()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.comboboxFloodDepthGrid.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=5, column=1, sticky="E")
        self.importButton.grid(row=5, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.stormSelection.get()}, {self.controller.advisorySelection.get()}, {self.controller.floodDepthGridSelection.get()}!")
        
    def setFloodDepthGridSelection(self):
        self.controller.floodDepthGridSelection.set(self.comboboxFloodDepthGrid.get())

    def downloadFile(self):
        floodHazardType = self.controller.floodHazardType.get()
        hazusHazardInputPath = fhit.getHazusHazardInputPath()
        downloadFolder = fhit.HazardInputTypeFolder(hazusHazardInputPath, floodHazardType)
        fhit.createHazardInputTypeFolder(hazusHazardInputPath, floodHazardType)
        fhit.downloadAwsS3File(fhit.getAwsS3BucketName(), self.controller.floodDepthGridSelection.get(), downloadFolder)

    def clearComboboxFloodDepthGrid(self):
        self.comboboxFloodDepthGrid.set('Choose a file...')

if __name__ == "__main__":
    root = floodHazardImportTool()
    root.mainloop()
