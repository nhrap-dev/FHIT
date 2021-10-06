'''
2021 Colin Lindeman NiyamIT clindeman@niyamit.com, colinlindeman@hotmail.com
Flood Hazard Import Tool FHIT
Python 3, Boto3, Pandas

This is a GUI that has one main frame and multiple subframes to act like a multipage wizard.

TODO:
-prompt user to overwrite or not?
-give user feedback/status that the app is doing something, like getting list of storms or downloaded data
-give user feedback that file was downloaded successfully or not
-show just the file name and not the key/path at step 5
-adjust combobox widths to account for longest possible values, static or dynamic
-adcirc made changes to their folder structure around 2/16/21 which affected this gui
'''

import tkinter as tk
from tkinter import ttk
import fhit_functions as fhit
import adcirc
#from windows import set_dpi_awareness

#set_dpi_awareness()

class floodHazardImportTool(tk.Tk):
    '''This is the main frame that controls the other frames/classes.
    '''
    def __init__(self):
        super().__init__()

        self.title("Flood Hazard Import Tool")
        self.frames = dict()
        
        self.floodHazardType = tk.StringVar()
        self.floodHazardDataSource = tk.StringVar()
        self.yearSelection = tk.StringVar()
        self.weathertypeSelection = tk.StringVar()
        self.stormSelection = tk.StringVar()
        self.advisorySelection = tk.StringVar()
        self.floodDepthGridSelection = tk.StringVar()
        self.fileKey = tk.StringVar()
        
        #if these are empty lists, it crashes the gui
        self.yearList = ['Choose a year...']
        self.stormList = ['Choose a storm...'] 
        self.advisoryList = ['Choose an advisory...']
        self.fileList = ['Choose a file...']

        self.iconbitmap('./images/ICO/24px.ico')
        self.resizable(False, False)
        
        container = ttk.Frame(self)
        container.grid(padx=40, pady=40, sticky="EW")

        #each class is a page in the gui
        for frameClass in (floodHazardType, floodHazardDataSource, yearSelection, weathertypeSelection, 
                           stormSelection, advisorySelection, floodDepthGridSelection):
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
                                              text="Storm Surge / Coastal", value="Storm Surge")
        self.coastalSurgeRButton.invoke()
        self.riverineRButton = ttk.Radiobutton(self, variable=self.floodHazardType,
                                          text="Riverine", value="Riverine" )
        self.riverineRButton.config(state='disabled')
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
        self.labelDirections = ttk.Label(self, text="Please select one data source")
        self.RButton1 = ttk.Radiobutton(self, variable=self.floodHazardDataSource,
                                              text="ADCIRC", value="ADCIRC")
        self.RButton1.invoke()
        self.RButton2 = ttk.Radiobutton(self, variable=self.floodHazardDataSource,
                                              text="NWS SLOSH", value="SLOSH")
        self.RButton2.config(state='disabled')
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(yearSelection)
                                                                       ,self.setFloodHazardDataSource()
                                                                       ,self.setYearList()
                                                                       ,self.printSelection()])
        self.backButton = ttk.Button(self, text="Back", command=lambda:controller.showFrame(floodHazardType))

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.RButton1.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.RButton2.grid(row=4, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=5, column=1)
        self.nextButton.grid(row=5, column=2)

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}!")
        print(f"Available Years: ")
        for year in self.controller.yearList:
            print(year)
        
    def setFloodHazardDataSource(self):
        self.controller.floodHazardDataSource = self.floodHazardDataSource

    def setYearList(self):
        self.controller.yearList = self.adcircYears()
        page = self.controller.get_page(yearSelection)
        page.comboboxYear['values'] = self.controller.yearList #update the list

    def adcircYears(self):
        global adcircData
        adcircData = adcirc.ADCIRC()
        years = adcircData.get_year_list()
        return years

class yearSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.labelFrame = ttk.Label(self, text="3. YEAR SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select a year")
        self.comboboxYear = ttk.Combobox(self)
        self.comboboxYear['values'] = self.controller.yearList
        self.comboboxYear.config(state='readonly')
        self.comboboxYear.config(width=40)
        self.comboboxYear.current(0)
        self.comboboxYear.bind("<<ComboboxSelected>>", self.enableNextButton)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(weathertypeSelection)
                                                                       ,self.setYearSelection()
                                                                       ,self.printSelection()])
        self.nextButton.config(state='disabled')
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(floodHazardDataSource)
                                                                       ,self.clearComboboxYear()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.comboboxYear.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=4, column=1, sticky="E")
        self.nextButton.grid(row=4, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.yearSelection.get()}!")

    def setYearSelection(self):
        self.controller.yearSelection.set(self.comboboxYear.get())

    def clearComboboxYear(self):
        self.comboboxYear.set('Choose a year...')
        self.nextButton.config(state='disabled')

    def enableNextButton(self, *args):
        if self.comboboxYear.get() != 'Choose a year...':
            self.nextButton.config(state='normal')


class weathertypeSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.weathertype = tk.StringVar()

        self.labelFrame = ttk.Label(self, text="3. WEATHER TYPE SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select a weather type")
        self.RButton1 = ttk.Radiobutton(self, variable=self.weathertype,
                                              text="Tropical", value="Tropical",
                                              command=self.enableNextButton)
        self.RButton2 = ttk.Radiobutton(self, variable=self.weathertype,
                                              text="Synoptic", value="Synoptic",
                                              command=self.enableNextButton)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(stormSelection)
                                                                       ,self.setWeatherTypeSelection()
                                                                       ,self.setStormList()
                                                                       ,self.printSelection()])
        self.nextButton.config(state='disabled')
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(yearSelection)])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.RButton1.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.RButton2.grid(row=3, column=2, columnspan=4, sticky="EW")
        self.backButton.grid(row=4, column=1, sticky="E")
        self.nextButton.grid(row=4, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.yearSelection.get()}, {self.controller.weathertypeSelection.get()}!")
        print(f"Available Storms:")
        for x in self.controller.stormList:
            print(x)

    def setWeatherTypeSelection(self):
        self.controller.weathertypeSelection.set(self.weathertype.get())

    def setStormList(self):
        self.controller.stormList = self.adcircStorms()
        page = self.controller.get_page(stormSelection)
        page.comboboxStorm['values'] = self.controller.stormList #update the list

    def adcircStorms(self):
        storms = adcircData.get_storm_list(self.controller.yearSelection.get(), self.controller.weathertypeSelection.get())
        return storms

    def enableNextButton(self, *args):
        self.nextButton.config(state='normal')

class stormSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller

        self.labelFrame = ttk.Label(self, text="3. STORM SELECTION")
        self.labelDirections = ttk.Label(self, text="Please select a storm")
        self.comboboxStorm = ttk.Combobox(self)
        self.comboboxStorm['values'] = self.controller.stormList
        self.comboboxStorm.config(state='readonly')
        self.comboboxStorm.config(width=40)
        self.comboboxStorm.current(0)
        self.comboboxStorm.bind("<<ComboboxSelected>>", self.enableNextButton)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(advisorySelection)
                                                                       ,self.setStormSelection()
                                                                       ,self.setAdvisoryList()
                                                                       ,self.printSelection()])
        self.nextButton.config(state='disabled')
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(weathertypeSelection)
                                                                       ,self.clearComboboxStorm()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.comboboxStorm.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=4, column=1, sticky="E")
        self.nextButton.grid(row=4, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.weathertypeSelection.get()}, {self.controller.stormSelection.get()}!")
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
        advisories = adcircData.get_advisory_list(self.controller.yearSelection.get(), self.controller.weathertypeSelection.get(), self.controller.stormSelection.get())
        return advisories

    def clearComboboxStorm(self):
        self.comboboxStorm.set('Choose a storm...')
        self.nextButton.config(state='disabled')

    def enableNextButton(self, *args):
        if self.comboboxStorm.get() != 'Choose a storm...':
            self.nextButton.config(state='normal')


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
        self.comboboxAdvisory.config(width=40)
        self.comboboxAdvisory.bind("<<ComboboxSelected>>", self.enableNextButton)
        self.nextButton = ttk.Button(self, text="Next", command=lambda:[controller.showFrame(floodDepthGridSelection)
                                                                       ,self.setAdvisorySelection()
                                                                       ,self.setFileList()
                                                                       ,self.printSelection()])
        self.nextButton.config(state='disabled')
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(stormSelection)
                                                                       ,self.clearComboboxAdvisory()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.comboboxAdvisory.grid(row=3, column=1, columnspan=4, sticky="EW")
        self.backButton.grid(row=5, column=1, sticky="E")
        self.nextButton.grid(row=5, column=2, sticky="W")

    def printSelection(self):
        print(f"You chose, {self.controller.floodHazardType.get()}, {self.controller.floodHazardDataSource.get()}, {self.controller.weathertypeSelection.get()}, {self.controller.stormSelection.get()}, {self.controller.advisorySelection.get()}!")
        print(f"Available Files:")
        for x in self.controller.fileList:
            print(x)
        
    def setAdvisorySelection(self):
        self.controller.advisorySelection.set(self.comboboxAdvisory.get())

    def setFileList(self):
        self.controller.fileList = self.adcircFiles()
        page = self.controller.get_page(floodDepthGridSelection)
        for item in self.controller.fileList:
            page.listboxFiles.insert('end', item)
        
    def adcircFiles(self):
        files = adcircData.get_file_list(self.controller.yearSelection.get(), self.controller.weathertypeSelection.get(), self.controller.stormSelection.get(), self.controller.advisorySelection.get())
        return files

    def clearComboboxAdvisory(self):
        self.comboboxAdvisory.set('Choose an advisory...')
        self.nextButton.config(state='disabled')

    def enableNextButton(self, *args):
        if self.comboboxAdvisory.get() != 'Choose an advisory...':
            self.nextButton.config(state='normal')


class floodDepthGridSelection(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller=controller
        
        self.labelFrame = ttk.Label(self, text="5. FLOOD DEPTH GRIDS")
        self.labelDirections = ttk.Label(self, text="Please select a depth grid")
        self.listboxFiles = tk.Listbox(self, width=100)
        self.listboxFiles.bind('<<ListboxSelect>>', self.printSelection, add="+")
        self.listboxFiles.bind('<<ListboxSelect>>', self.updateMetadataTable, add="+")
        self.listboxFiles.bind('<<ListboxSelect>>', self.enableImportButton, add="+")
        self.importButton = ttk.Button(self, text="Import", command=lambda:[self.setFloodDepthGridSelection()
                                                                           ,self.printSelection()
                                                                           ,self.downloadFile()])
        #Can this be better? programmatically generated from lists?
        #TODO Year
        self.tableLabel1 = ttk.Label(self, text='DateTime:')
        self.metadata1 = tk.StringVar()
        self.tableValue1 = ttk.Label(self, textvariable=self.metadata1)
        self.tableLabel2 = ttk.Label(self, text='Advisory:')
        self.metadata2 = tk.StringVar()
        self.tableValue2 = ttk.Label(self, textvariable=self.metadata2)
        self.tableLabel3 = ttk.Label(self, text='ADCIRC variable mapped to raster (VarName):')
        self.metadata3 = tk.StringVar()
        self.tableValue3 = ttk.Label(self, textvariable=self.metadata3)
        self.tableLabel4 = ttk.Label(self, text='Abbreviated ADCIRC grid name (GridNameAbbrev):')
        self.metadata4 = tk.StringVar()
        self.tableValue4 = ttk.Label(self, textvariable=self.metadata4)
        self.tableLabel5 = ttk.Label(self, text='Wind Model:')
        self.metadata5 = tk.StringVar()
        self.tableValue5 = ttk.Label(self, textvariable=self.metadata5)
        self.tableLabel6 = ttk.Label(self, text='Wave Model:')
        self.metadata6 = tk.StringVar()
        self.tableValue6 = ttk.Label(self, textvariable=self.metadata6)
        self.tableLabel7 = ttk.Label(self, text='Ensemble member name (EnsName):')
        self.metadata7 = tk.StringVar()
        self.tableValue7 = ttk.Label(self, textvariable=self.metadata7)
        self.tableLabel8 = ttk.Label(self, text='Operator:')
        self.metadata8 = tk.StringVar()
        self.tableValue8 = ttk.Label(self, textvariable=self.metadata8)
        self.tableLabel9 = ttk.Label(self, text='Machine:')
        self.metadata9 = tk.StringVar()
        self.tableValue9 = ttk.Label(self, textvariable=self.metadata9)
        self.tableLabel10 = ttk.Label(self, text='Other:')
        self.metadata10 = tk.StringVar()
        self.tableValue10 = ttk.Label(self, textvariable=self.metadata10)
        self.tableLabel11 = ttk.Label(self, text='Resolution (meters):')
        self.metadata11 = tk.StringVar()
        self.tableValue11 = ttk.Label(self, textvariable=self.metadata11)
        self.tableLabel12 = ttk.Label(self, text='Upper Left Longtude (ullo)(degrees):')
        self.metadata12 = tk.StringVar()
        self.tableValue12 = ttk.Label(self, textvariable=self.metadata12)
        self.tableLabel13 = ttk.Label(self, text='Upper Left Latitude (ulla)(degrees):')
        self.metadata13 = tk.StringVar()
        self.tableValue13 = ttk.Label(self, textvariable=self.metadata13)
        self.tableLabel14 = ttk.Label(self, text='Number of cells in lon (nx):')
        self.metadata14 = tk.StringVar()
        self.tableValue14 = ttk.Label(self, textvariable=self.metadata14)
        self.tableLabel15 = ttk.Label(self, text='Number of cells in lat (ny):')
        self.metadata15 = tk.StringVar()
        self.tableValue15 = ttk.Label(self, textvariable=self.metadata15)
        ##self.tableLabel16 = ttk.Label(self, text='Size (mb):')
        ##self.metadata16 = tk.StringVar()
        ##self.tableValue16 = ttk.Label(self, textvariable=self.metadata16)
        ##self.tableLabel17 = ttk.Label(self, text='Last Modified:')
        ##self.metadata17 = tk.StringVar()
        ##self.tableValue17 = ttk.Label(self, textvariable=self.metadata17)
        
        self.importButton.config(state='disabled')
        self.backButton = ttk.Button(self, text="Back", command=lambda:[controller.showFrame(advisorySelection)
                                                                       ,self.clearlistboxFiles()])

        self.labelFrame.grid(row=1, column=1, columnspan=4, sticky="EW")
        self.labelDirections.grid(row=2, column=1, columnspan=4, sticky="EW")
        self.listboxFiles.grid(row=3, column=1, columnspan=4, sticky='EW')
        
        self.tableLabel1.grid(row=4, column=1, sticky='EW')
        self.tableValue1.grid(row=4, column=2, sticky='EW')
        self.tableLabel2.grid(row=5, column=1, sticky='EW')
        self.tableValue2.grid(row=5, column=2, sticky='EW')
        self.tableLabel3.grid(row=6, column=1, sticky='EW')
        self.tableValue3.grid(row=6, column=2, sticky='EW')
        self.tableLabel4.grid(row=7, column=1, sticky='EW')
        self.tableValue4.grid(row=7, column=2, sticky='EW')
        self.tableLabel5.grid(row=8, column=1, sticky='EW')
        self.tableValue5.grid(row=8, column=2, sticky='EW')
        self.tableLabel6.grid(row=9, column=1, sticky='EW')
        self.tableValue6.grid(row=9, column=2, sticky='EW')
        self.tableLabel7.grid(row=10, column=1, sticky='EW')
        self.tableValue7.grid(row=10, column=2, sticky='EW')
        self.tableLabel8.grid(row=11, column=1, sticky='EW')
        self.tableValue8.grid(row=11, column=2, sticky='EW')
        self.tableLabel9.grid(row=12, column=1, sticky='EW')
        self.tableValue9.grid(row=12, column=2, sticky='EW')
        self.tableLabel10.grid(row=13, column=1, sticky='EW')
        self.tableValue10.grid(row=13, column=2, sticky='EW')
        self.tableLabel11.grid(row=14, column=1, sticky='EW')
        self.tableValue11.grid(row=14, column=2, sticky='EW')
        self.tableLabel12.grid(row=15, column=1, sticky='EW')
        self.tableValue12.grid(row=15, column=2, sticky='EW')
        self.tableLabel13.grid(row=16, column=1, sticky='EW')
        self.tableValue13.grid(row=16, column=2, sticky='EW')
        self.tableLabel14.grid(row=17, column=1, sticky='EW')
        self.tableValue14.grid(row=17, column=2, sticky='EW')
        self.tableLabel15.grid(row=18, column=1, sticky='EW')
        self.tableValue15.grid(row=18, column=2, sticky='EW')
        ##self.tableLabel16.grid(row=19, column=1, sticky='EW')
        ##self.tableValue16.grid(row=19, column=2, sticky='EW')
        ##self.tableLabel17.grid(row=20, column=1, sticky='EW')
        ##self.tableValue17.grid(row=20, column=2, sticky='EW')
        
        self.backButton.grid(row=100, column=1, sticky="E")
        self.importButton.grid(row=100, column=2, sticky="W")

    def printSelection(self, *args):
        selected_indices = self.listboxFiles.curselection()
        selected_file = ",".join([self.listboxFiles.get(i) for i in selected_indices])
        print(f"You chose, {selected_file}")
        
    def updateMetadataTable(self, *args):
        selected_indices = self.listboxFiles.curselection()
        selected_file = ",".join([self.listboxFiles.get(i) for i in selected_indices])
        fileMetadata = adcircData.parse_adcirc_filename(selected_file)
        self.metadata1.set(fileMetadata['StormNumber'])
        self.metadata2.set(fileMetadata['Advisory'])
        self.metadata3.set(fileMetadata['VarName'])
        self.metadata4.set(fileMetadata['GridNameAbbrev'])
        self.metadata5.set(fileMetadata['WindModel'])
        self.metadata6.set(fileMetadata['WaveModel'])
        self.metadata7.set(fileMetadata['EnsName'])
        self.metadata8.set(fileMetadata['Operator'])
        self.metadata9.set(fileMetadata['Machine'])
        self.metadata10.set(fileMetadata['Other'])
        self.metadata11.set(fileMetadata['res'])
        self.metadata12.set(fileMetadata['ullo'])
        self.metadata13.set(fileMetadata['ulla'])
        self.metadata14.set(fileMetadata['nx'])
        self.metadata15.set(fileMetadata['ny'])
        ##self.metadata16.set(fileMetadata['size'])
        ##self.metadata17.set(fileMetadata['lastmodified'])

    def setFloodDepthGridSelection(self):
        selected_indices = self.listboxFiles.curselection()
        selected_file = ",".join([self.listboxFiles.get(i) for i in selected_indices])
        self.controller.floodDepthGridSelection.set(selected_file)

    def downloadFile(self):
        floodHazardType = self.controller.floodHazardType.get()
        hazusHazardInputPath = fhit.getHazusHazardInputPath()
        downloadFolder = fhit.HazardInputTypeFolder(hazusHazardInputPath, floodHazardType)
        fhit.createHazardInputTypeFolder(hazusHazardInputPath, floodHazardType)
        awsKey = adcircData.get_awskey_from_filename(self.controller.yearSelection.get()
                                                     ,self.controller.weathertypeSelection.get()
                                                     ,self.controller.stormSelection.get()
                                                     ,self.controller.advisorySelection.get() 
                                                     ,self.controller.floodDepthGridSelection.get())
        adcircData.download_awss3_file(awsKey, downloadFolder)

    def clearlistboxFiles(self):
        self.metadata1.set('')
        self.metadata2.set('')
        self.metadata3.set('')
        self.metadata4.set('')
        self.metadata5.set('')
        self.metadata6.set('')
        self.metadata7.set('')
        self.metadata8.set('')
        self.metadata9.set('')
        self.metadata10.set('')
        self.metadata11.set('')
        self.metadata12.set('')
        self.metadata13.set('')
        self.metadata14.set('')
        self.metadata15.set('')
        self.listboxFiles.delete(0, tk.END)
        self.importButton.config(state='disabled')

    def enableImportButton(self, *args):
        self.importButton.config(state='normal')

if __name__ == "__main__":
    root = floodHazardImportTool()
    root.mainloop()
