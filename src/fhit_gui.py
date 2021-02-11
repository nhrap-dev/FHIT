'''
2021 Colin Lindman NiyamIT
Flood Hazard Import Tool FHIT GUI
Python 3

TODO:
-populate lists with a default value like hhit
-add code to main script to import actual data
-build up import button to set off processing of the chosen data
-icons https://teams.microsoft.com/_#/files/General?threadId=19%3A4f2ec634fe3245a1bcfec366f1bfb31d%40thread.skype&ctx=channel&context=NewGraphics&rootfolder=%252Fsites%252FHazusToolDevelopment%252FShared%2520Documents%252FGeneral%252FInterface%252FNewGraphics
'''


import tkinter as tk
from tkinter import ttk
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
        self.floodDepthGridSelection = tk.StringVar()
        self.resizable(False, False)

        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky="EW")

        for frameClass in (floodHazardType, floodHazardDataSource, stormSelection, floodDepthGridSelection):
            frame = frameClass(container, self)
            self.frames[frameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.showFrame(floodHazardType)
        
    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class floodHazardType(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

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

##        self.labelFrame.pack()
##        self.labelDirections.pack()
##        self.coastalSurgeRButton.pack()
##        self.riverineRButton.pack()
##        self.nextButton.pack()
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

        self.floodHazardDataSource = tk.StringVar()

        self.labelFrame = ttk.Label(self, text="2. FLOOD HAZARD SOURCE")
        self.labelFiller = ttk.Label(self, text="")
        self.labelDirections = ttk.Label(self, text="Please select a data source")
        self.adcircRButton = ttk.Radiobutton(self, variable=self.floodHazardDataSource,
                                              text="ADCIRC", value="ADCIRC")
        self.adcircRButton.invoke()
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(stormSelection)
                                                                   ,self.setFloodHazardDataSource()
                                                                   ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(floodHazardType))

##        self.labelFrame.pack()
##        self.labelDirections.pack()
##        self.adcircRButton.pack()
##        self.nextButton.pack()
##        self.backButton.pack()
        self.labelFrame.grid(row=1, column=1, columnspan=2, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=2, sticky="EW")
        self.adcircRButton.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}!")
        
    def setFloodHazardDataSource(self):
        root.floodHazardDataSource = self.floodHazardDataSource

class stormSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.stormSelection = tk.StringVar()
        #self.stormSelection.set('test') #debug

        self.labelFrame = ttk.Label(self, text="3. STORM SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select a storm")
        self.labelFiller = ttk.Label(self, text="")
        self.comboboxStorm = ttk.Combobox(self)
        self.comboboxStorm.config(values=('storm1','storm2','storm3'))
        self.comboboxStorm.config(state='readonly')
        self.comboboxStorm.current(0)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(floodDepthGridSelection)
                                                                        ,self.setStormSelection()
                                                                        ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(floodHazardDataSource))

##        self.labelFrame.pack()
##        self.labelDirections.pack()
##        self.comboboxStorm.pack()
##        self.nextButton.pack()
##        self.backButton.pack()
        self.labelFrame.grid(row=1, column=1)
        self.labelDirections.grid(row=2, column=1)
        self.comboboxStorm.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}, {root.stormSelection.get()}!")

    def setStormSelection(self):
        self.stormSelection.set(self.comboboxStorm.get())
        root.stormSelection = self.stormSelection

class floodDepthGridSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.floodDepthGridSelection = tk.StringVar()
        
        self.labelFrame = ttk.Label(self, text="4. FLOOD DEPTH GRIDS")
        self.labelDirections = ttk.Label(self, text="Please select a depth grid")
        self.labelFiller = ttk.Label(self, text="")
        self.comboboxFloodDepthGrid = ttk.Combobox(self)
        self.comboboxFloodDepthGrid.config(values=('depthgrid1','depthgrid2','depthgrid3'))
        self.comboboxFloodDepthGrid.config(state='readonly')
        self.comboboxFloodDepthGrid.current(0)
        self.importButton = ttk.Button(self, text="Import", command=lambda:[self.setFloodDepthGridSelection()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(stormSelection))

##        self.labelFrame.pack()
##        self.labelDirections.pack()
##        self.comboboxFloodDepthGrid.pack()
##        self.importButton.pack()
##        self.backButton.pack()
        self.labelFrame.grid(row=1, column=1)
        self.labelDirections.grid(row=2, column=1)
        self.comboboxFloodDepthGrid.grid(row=3, column=1)
        self.labelFiller.grid(row=4, column=1, columnspan=2, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.importButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {root.floodHazardType.get()}, {root.floodHazardDataSource.get()}, {root.stormSelection.get()}, {root.floodDepthGridSelection.get()}!")
        
    def setFloodDepthGridSelection(self):
        self.floodDepthGridSelection.set(self.comboboxFloodDepthGrid.get())
        root.floodDepthGridSelection = self.floodDepthGridSelection
        #root.floodDepthGridSelection.set(self.floodDepthGridSelection)  #this makes PY_VAR7

if __name__ == "__main__":
    root = floodHazardImportTool()
    root.mainloop()
