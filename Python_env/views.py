"""clindeman
python 3
Widget Classes
"""
#TODO pep8 standards CWL
#TODO break out frames? widgets? CWL
#TODO handle no internet CWL

import tkinter as tk
import tkinter.ttk as ttk
import os
import time
import json
from pathlib import Path
from threading import Thread
import ctypes
import adcirc
import fhitsupport as FHITSupport

class GUI(tk.Frame):
    """Create the controller frame
    """
    def __init__(self, *args):
        super().__init__()

        self.hazard_type_selection = tk.StringVar() # types defined in config
        # modifies hazard source list

        self.hazard_data_source_selection = tk.StringVar() # sources have types in config
        self.hazard_data_source_selection.trace_variable("w", self.trace_when_source_is_updated) # modifies which search parameter frame to show

        self.search_parameters = {} #actions within search parameter frame update the file list
       
        self.file_list_update = tk.BooleanVar()
        self.file_list_update.set(False)
        self.file_list = []

        self.file_selection = tk.StringVar() #trace file selection to update file_selection_properties
        self.file_selection_key = tk.StringVar() #ADCIRC = "name", etc

        self.file_selection_propeties = {}

        #TODO Options settings CWL
        #unit of measurement

        self.create_widgets()

    def create_widgets(self):
        self.SelectHazardTypeSourceFrame = SelectHazardTypeSource(self)
        self.SelectHazardTypeSourceFrame.grid(column=0, row=0, sticky='new', padx=10, pady=10)

        self.show_search_parameters_default_frame()

        #Commented out for IV&V #self.OptionsFrame = Options(self)
        #Commented out for IV&V #self.OptionsFrame.grid(column=0, row=2, sticky='sw', padx=20, pady=20)

        self.SelectFileListFrame = SelectFileList(self)
        self.SelectFileListFrame.grid(column=1, row=0, sticky='new', padx=10, pady=10)

        self.SelectFilePropertiesFrame = SelectFileProperties(self)
        self.SelectFilePropertiesFrame.grid(column=1, row=1, sticky='new', padx=10, pady=10)

        self.ButtonsFrame = Buttons(self)
        self.ButtonsFrame.grid(column=1, row=2, sticky='sw', padx=10, pady=10)

    def show_search_parameters_default_frame(self):
        self.SearchParametersDefaultFrame = SearchParametersDefault(self)
        self.SearchParametersDefaultFrame.grid(column=0, row=1, sticky='new', padx=10, pady=10)

    def destroy_search_parameters_default_frame(self):
        self.SearchParametersDefaultFrame.destroy()

    def show_search_parameters_adcirc_frame(self):
        self.SearchParametersADCIRCFrame = SearchParametersADCIRC(self)
        self.SearchParametersADCIRCFrame.grid(column=0, row=1, sticky='new', padx=10, pady=10)

    def destroy_search_parameters_adcirc_frame(self):
        self.SearchParametersADCIRCFrame.destroy()

    def trace_when_source_is_updated(self, *args):
        #TODO need to make this cleaner to support many different search parameters CWL
        if self.hazard_data_source_selection.get() == "ADCIRC":
            try:
                self.destroy_search_parameters_default_frame()
            except:
                pass
            self.show_search_parameters_adcirc_frame()
        else:
            try:
                self.destroy_search_parameters_adcirc_frame()
            except:
                pass
            self.show_search_parameters_default_frame()

class SelectHazardTypeSource(ttk.Frame):
    """Frame for selecting hazard type and hazard source"""
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        self.columnconfigure(0, weight=1)

        self.hazard_types = self.get_hazard_types()
        self.hazard_sources = ['']

        self.create_widgets()
    
    def create_widgets(self):
        self.LabelFrameHazardType = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='nw', borderwidth=2)
        self.LabelFrameHazardType.configure(text='SELECT A HAZARD TYPE')
        self.LabelFrameHazardType.grid(column=0, row=0, padx=10, pady=10, sticky='ew')

        self.comboboxHazardType = ttk.Combobox(self.LabelFrameHazardType, width=40)
        self.comboboxHazardType.configure(values=self.hazard_types)
        self.comboboxHazardType.config(state='readonly')
        self.comboboxHazardType.bind("<<ComboboxSelected>>", self.__handler_comboboxHazardType)
        self.comboboxHazardType.grid(column=0, row=1, padx=5, pady=5)

        self.LabelFrameHazardSource = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='nw', borderwidth=2)
        self.LabelFrameHazardSource.configure(text='SELECT A HAZARD SOURCE')
        self.LabelFrameHazardSource.grid(column=0, row=1, padx=10, pady=10, sticky='ew')

        self.comboboxHazardSource = ttk.Combobox(self.LabelFrameHazardSource, width=40)
        self.comboboxHazardSource.configure(values=self.hazard_sources)
        self.comboboxHazardSource.config(state='readonly')
        self.comboboxHazardSource.bind("<<ComboboxSelected>>", self.__handler_comboboxHazardSource)
        self.comboboxHazardSource.grid(column=0, row=4, padx=5, pady=5)

    ##TYPE##
    def get_hazard_types(self):
        with open(os.path.join(Path(__file__).parent, "config.json")) as f:
            config_json = json.load(f)
        return config_json['hazard_types']

    def set_hazard_type_selection(self, *args):
        self.controller.hazard_type_selection.set(self.comboboxHazardType.get())
        print(self.controller.hazard_type_selection.get())

    ##SOURCE##
    def __get_hazard_sources(self, hazard_type):
        source_list = []
        with open(os.path.join(Path(__file__).parent, "config.json")) as f:
            config_json = json.load(f)
            for hazard_source in config_json["data_sources"]:
                if hazard_type in hazard_source['hazard_types'] and hazard_source['enabled']:
                    source_list.append(hazard_source['name'])
        return source_list

    def __set_hazard_sources(self, *args):
        hazard_sources = self.__get_hazard_sources(self.controller.hazard_type_selection.get())
        self.comboboxHazardSource.config(values=hazard_sources)
        #print(hazard_sources) #DEBUG

    def __clear_hazard_sources(self, *args):
        self.comboboxHazardSource.set('')
        self.controller.SelectFilePropertiesFrame.clear_file_properties()
        self.controller.SelectFileListFrame.clearFileList()

    def __clear_hazard_data_source_selection(self, *args):
        self.controller.hazard_data_source_selection.set('')
        self.controller.SelectFilePropertiesFrame.clear_file_properties()
        self.controller.SelectFileListFrame.clearFileList()

    def __set_Hazard_Source_Selection(self, *args):
        self.controller.hazard_data_source_selection.set(self.comboboxHazardSource.get())
        print(self.controller.hazard_data_source_selection.get())

    ##HANDLERS## TODO Clean this up CWL
    def __handler_comboboxHazardType(self, *args):
        self.__clear_hazard_data_source_selection()
        self.__clear_hazard_sources()
        self.set_hazard_type_selection()
        self.__set_hazard_sources()

    def __handler_comboboxHazardSource(self, *args):
        self.controller.SelectFilePropertiesFrame.clear_file_properties()
        self.controller.SelectFileListFrame.clearFileList()
        self.__set_Hazard_Source_Selection()
        #load default search params
        #clear file list
        #clear file properties

class SearchParametersDefault(ttk.Frame):
    """Default frame for search parameters; search parameters frame for no data source selected"""
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.LabelframeSearchParameters = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelframeSearchParameters.configure(text='''SELECT FLOOD HAZARD SEARCH PARAMETERS''')
        self.LabelframeSearchParameters.grid(column=0, row=0, padx=10, pady=10)

        ttk.Label(self.LabelframeSearchParameters, text='Choose a Hazard Type and Hazard Source').grid(column=0, row=0, padx=5, pady=5, sticky='w')

class SearchParametersADCIRC(ttk.Frame):
    """ """
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        self.columnconfigure(0, weight=1)

        self.yearSelection = tk.StringVar()
        self.weathertypeSelection = tk.StringVar()
        self.stormSelection = tk.StringVar()
        self.advisorySelection = tk.StringVar()
        self.floodDepthGridSelection = tk.StringVar()
        #self.fileKey = tk.StringVar() #TODO for download CWL

        self.yearList = ['Choose a Year...']
        self.weathertypeList = ["Synoptic", "Tropical"]
        self.stormList = ['Choose a Storm...'] 
        self.advisoryList = ['Choose an Advisory...']

        #TODO handle if website down or data format changed significantly CWL
        self.set_adcirc_data_wpopup() #set self.adcircData attribute with please wait popup
        self.setYearList()

        self.columnconfigure(0)
        self.__create_widgets()

        controller.file_selection.trace_variable("w", self.file_selection_updated)
        
    def popup(self):
        '''Create a popup window'''
        popup_window = tk.Toplevel(self)
        popup_window.transient()
        tk.Label(popup_window, text="Please Wait...", font=(None, 36)).pack()
        self.update()
        popup_window.grab_set()
        return popup_window

    def set_adcirc_data_wpopup(self):
        '''Create popup window while downloading the adcirc data and set Raster Unit'''
        wait_popup = self.popup()
        self.adcircData = adcirc.ADCIRC() 
        self.adcircData.data['Raster Unit'] = self.get_adcric_depth_unit()
        wait_popup.destroy()

    def get_adcric_depth_unit(self):
        with open(os.path.join(Path(__file__).parent, "config.json")) as f:
            config_json = json.load(f)
        temp_dict_a = config_json['data_sources']
        temp_dict_b = list(filter(lambda data_source: data_source['name'] == 'ADCIRC', temp_dict_a))
        depth_unit = temp_dict_b[0]['depth_unit']
        return depth_unit

    def __create_widgets(self):
        self.LabelframeSearchParameters = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelframeSearchParameters.configure(text='''SELECT FLOOD HAZARD SEARCH PARAMETERS''')
        self.LabelframeSearchParameters.grid(column=0, row=0, padx=10, pady=10)

        ## YEAR ##
        ttk.Label(self.LabelframeSearchParameters, text='Year:').grid(column=0, row=1, sticky=tk.W)
        self.comboboxYear = ttk.Combobox(self.LabelframeSearchParameters)
        self.comboboxYear['values'] = self.yearList
        self.comboboxYear.config(state='readonly')
        self.comboboxYear.bind("<<ComboboxSelected>>", self.clearComboboxWeatherType)
        self.comboboxYear.bind("<<ComboboxSelected>>", self.clearComboboxStorm, add="+")
        self.comboboxYear.bind("<<ComboboxSelected>>", self.clearComboboxAdvisory, add="+")
        self.comboboxYear.bind("<<ComboboxSelected>>", self.clearFileList, add="+")
        self.comboboxYear.bind("<<ComboboxSelected>>", self.clear_file_properties, add="+")
        self.comboboxYear.bind("<<ComboboxSelected>>", self.setYearSelection, add="+") #needs to be last to enable next combobox
        self.comboboxYear.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

        ## WEATHER TYPE ##
        ttk.Label(self.LabelframeSearchParameters, text='Weather Type:').grid(column=0, row=2, sticky=tk.W)
        self.comboboxWeatherType = ttk.Combobox(self.LabelframeSearchParameters, width=40)
        self.comboboxWeatherType['values'] = self.weathertypeList
        self.comboboxWeatherType.config(state='disabled')
        self.comboboxWeatherType.current(0)
        self.comboboxWeatherType.bind("<<ComboboxSelected>>", self.clearComboboxStorm)
        self.comboboxWeatherType.bind("<<ComboboxSelected>>", self.clearComboboxAdvisory, add="+")
        self.comboboxWeatherType.bind("<<ComboboxSelected>>", self.clearFileList, add="+")
        self.comboboxWeatherType.bind("<<ComboboxSelected>>", self.clear_file_properties, add="+")
        self.comboboxWeatherType.bind("<<ComboboxSelected>>", self.setWeatherTypeSelection, add="+")
        self.comboboxWeatherType.bind("<<ComboboxSelected>>", self.setStormList, add="+")
        self.comboboxWeatherType.grid(column=1, row=2, sticky='ew', padx=5, pady=5)

        ## STORM ##
        ttk.Label(self.LabelframeSearchParameters, text='Storm/Date:').grid(column=0, row=3, sticky='w')
        self.comboboxStorm = ttk.Combobox(self.LabelframeSearchParameters, width=40)
        self.comboboxStorm['values'] = self.stormList
        self.comboboxStorm.config(state='disabled')
        self.comboboxStorm.current(0)
        self.comboboxStorm.bind("<<ComboboxSelected>>", self.clearComboboxAdvisory)
        self.comboboxStorm.bind("<<ComboboxSelected>>", self.clear_file_properties, add="+")
        self.comboboxStorm.bind("<<ComboboxSelected>>", self.clearFileList, add="+")
        self.comboboxStorm.bind("<<ComboboxSelected>>", self.setStormSelection, add="+")
        self.comboboxStorm.bind("<<ComboboxSelected>>", self.setAdvisoryList, add="+")
        self.comboboxStorm.grid(column=1, row=3, sticky='ew', padx=5, pady=5)

        ## ADVISORY ##
        ttk.Label(self.LabelframeSearchParameters, text='Advisory:').grid(column=0, row=4, sticky='w')
        self.comboboxAdvisory = ttk.Combobox(self.LabelframeSearchParameters)
        self.comboboxAdvisory['values'] = self.advisoryList
        self.comboboxAdvisory.config(state='disabled')
        self.comboboxAdvisory.current(0)
        self.comboboxAdvisory.bind("<<ComboboxSelected>>", self.clear_file_properties)
        self.comboboxAdvisory.bind("<<ComboboxSelected>>", self.setAdvisorySelection, add="+")
        self.comboboxAdvisory.bind("<<ComboboxSelected>>", self.setFileList, add="+")
        self.comboboxAdvisory.grid(column=1, row=4, sticky='ew', padx=5, pady=5)
    
    ## YEAR ##
    def getadcircYears(self):
        years = self.adcircData.get_year_list()
        return years

    def setYearList(self, *args):
        self.yearList = self.getadcircYears()

    def setYearSelection(self, *args):
        self.yearSelection.set(self.comboboxYear.get())
        print(f"You chose, {self.yearSelection.get()}")
        self.comboboxWeatherType.config(state='readonly')

    def clearComboboxYear(self, *args):
        self.comboboxYear.set('Choose a year...')
    
    ### WEATHER TYPE ##
    def setWeatherTypeSelection(self, *args):
        self.weathertypeSelection.set(self.comboboxWeatherType.get())
        print(f"You chose, {self.weathertypeSelection.get()}")
        self.comboboxStorm.config(state='readonly')

    def clearComboboxWeatherType(self, *args):
        self.comboboxWeatherType.set('Choose a weather type...')
        self.comboboxWeatherType.config(state='disabled')

    ## STORM ##
    def adcircStorms(self):
        storms = self.adcircData.get_storm_list(self.yearSelection.get(), self.weathertypeSelection.get())
        return storms

    def setStormList(self, *args):
        self.stormList = self.adcircStorms()
        self.comboboxStorm['values'] = self.stormList #update the list in the combobox
        #print(f"setting storm list: {self.adcircStorms()}") #debug

    def setStormSelection(self, *args):
        self.stormSelection.set(self.comboboxStorm.get())
        print(f"You chose Storm: {self.stormSelection.get()}")
        self.comboboxAdvisory.config(state='readonly')

    def clearComboboxStorm(self, *args):
        self.comboboxStorm.set('Choose a storm...')
        self.comboboxStorm.config(state='disabled')

    ## ADVISORY ##
    def adcircAdvisories(self):
        advisories = self.adcircData.get_advisory_list(self.yearSelection.get(), self.weathertypeSelection.get(), self.stormSelection.get())
        return advisories

    def setAdvisoryList(self, *args):
        self.advisoryList = self.adcircAdvisories()
        self.comboboxAdvisory['values'] = self.advisoryList #update the list in the combobox

    def setAdvisorySelection(self, *args):
        self.advisorySelection.set(self.comboboxAdvisory.get())
        print(f"You chose, {self.advisorySelection.get()}")

    def clearComboboxAdvisory(self, *args):
        self.comboboxAdvisory.set('Choose an advisory...')
        self.comboboxAdvisory.config(state='disabled')

    ## FILE LIST ##
    def adcircFiles(self):
        files = self.adcircData.get_file_list(self.yearSelection.get(), self.weathertypeSelection.get(), self.stormSelection.get(), self.advisorySelection.get())
        return files

    def setFileList(self, *args):
        self.fileList = self.adcircFiles()
        #print(self.fileList)#debug
        self.controller.file_list = self.fileList
        #print(self.controller.file_list)#debug
        self.controller.file_list_update.set(True)
        #print(self.controller.file_list_update.get())#debug

    def clearFileList(self, *args):
        self.controller.file_list = []
        self.controller.file_list_update.set(True)

    def clearFileSelection(self, *args):
        self.controller.file_selection.set('')
        self.controller.file_selection_key.set('')

    ## FILE PROPERTIES ##
    def file_selection_updated(self, *args):
        """For Trace"""
        #print(f'file selection trace {self.controller.file_selection.get()}') #debug
        ugly_dictionary = self.adcircData.get_file_attributes_byname(self.controller.file_selection.get())
        dictionary = self.adcircData.rename_dictionary_keys(ugly_dictionary)
        self.controller.file_selection_propeties = dictionary
        self.controller.file_selection_key.set("name")

    def clear_file_properties(self, *args):
        self.controller.SelectFilePropertiesFrame.clear_file_properties()

class SelectFileList(ttk.Frame):
    """Frame for listing files from search parameters"""
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

        controller.file_list_update.trace_variable("w", self._trace_when_file_list_is_updated)

    def __create_widgets(self):
        ttk.Label(self, text='SELECT FROM AVAILABLE FILES').grid(column=0, row=0, sticky='w')
        self.treeviewFiles = ttk.Treeview(self, columns=(1), show='headings', selectmode="browse")
        self.treeviewFiles.bind("<<TreeviewSelect>>", self.setFileSelection)
        self.treeviewFiles.grid(column=0, row=1, sticky='ew')
        self.treeviewFiles.heading(1, text='FILE', anchor='w')

        self.scrollbarFiles = tk.Scrollbar(self)
        self.scrollbarFiles.grid(column=1, row=1, sticky='nsew')
        self.treeviewFiles.config(yscrollcommand=self.scrollbarFiles.set)
        self.scrollbarFiles.config(command=self.treeviewFiles.yview)

    def selectItem(self, *args):
        curItem = self.treeviewFiles.focus()
        #print(f"selected Item: {self.treeviewFiles.item(curItem)}") #debug
        #print(f"selectItem: {self.treeviewFiles.item(curItem)['values'][0]}") #debug
        return self.treeviewFiles.item(curItem)['values'][0]

    def setFileSelection(self, *args):
        self.controller.file_selection.set(self.selectItem())
        self.controller.ButtonsFrame.ButtonDownloadImport.config(state='enabled')
        print(f"You chose File: {self.controller.file_selection.get()}")

    def clearFileList(self, *args):
        self.treeviewFiles.delete(*self.treeviewFiles.get_children())
        self.controller.ButtonsFrame.ButtonDownloadImport.config(state='disabled')

    def load_data(self, list):
        counter = 0
        for item in list:
            self.treeviewFiles.insert(parent='', index=counter, iid=counter, text='', values=(item))
            counter +=1

    def _trace_when_file_list_is_updated(self, *args):
        #print('file list trace activated') #debug
        #print(self.controller.file_list_update) #debug
        #print(self.controller.file_list) #debug
        self.clearFileList()
        self.load_data(self.controller.file_list)


class SelectFileProperties(ttk.Frame):
    """Frame to show property/value of selected file"""
    def __init__(self, controller):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.controller=controller
        self.create_widgets()

        controller.file_selection.trace_variable("w", self.trace_when_file_is_selected)

    def create_widgets(self):
        ttk.Label(self, text='SELECTED FILE PROPERTIES').grid(column=0, row=0, sticky='w')
        self.treeviewFileProperties = ttk.Treeview(self, columns=(1,2), show='headings')
        self.treeviewFileProperties.column(2, minwidth=200) #TODO appears to not do anything CWL
        self.treeviewFileProperties.grid(column=0, row=1, sticky='ew')
        self.treeviewFileProperties.heading(1, text='PROPERTY', anchor='w')
        self.treeviewFileProperties.heading(2, text='VALUE', anchor='w')

        self.scrollbarFileProperties = tk.Scrollbar(self)
        self.scrollbarFileProperties.grid(column=1, row=1, sticky='ns')
        self.treeviewFileProperties.config(yscrollcommand=self.scrollbarFileProperties.set)
        self.scrollbarFileProperties.config(command=self.treeviewFileProperties.yview)

        self.scrollbarFileProperties_x = tk.Scrollbar(self, orient='horizontal')
        self.scrollbarFileProperties_x.grid(column=0, row=2, sticky='ew')
        self.treeviewFileProperties.config(xscrollcommand=self.scrollbarFileProperties_x.set)
        self.scrollbarFileProperties_x.config(command=self.treeviewFileProperties.xview)

    def clear_file_properties(self, *args):
        self.treeviewFileProperties.delete(*self.treeviewFileProperties.get_children())

    def load_file_properties_data(self, dictionary):
        counter = 0
        for key, value in dictionary.items():
            self.treeviewFileProperties.insert(parent='', index=counter, iid=counter, text='', values=(key, value))
            counter +=1

    def trace_when_file_is_selected(self, *args):
        #print(f"trace when file is selected") #debug
        self.clear_file_properties()
        self.load_file_properties_data(self.controller.file_selection_propeties)

class Buttons(ttk.Frame):
    """Frame for buttons"""
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        self.create_widgets()

    def create_widgets(self):
        self.ButtonDownloadImport = ttk.Button(self, text="Download and Import Selected File", command=self.button_download_command)
        self.ButtonDownloadImport.grid(column=0, row=1, padx=5)
        self.ButtonDownloadImport.config(state='disabled')
        #Commented out for IV&V#self.ButtonBrowseImport = ttk.Button(self, text="Browse for Existing Hazard Data to Import").grid(column=1, row=1, padx=5)
        self.ButtonQuit = ttk.Button(self, text="Quit")
        self.ButtonQuit.configure(command=self.controller.quit) # will quit Tcl interpreter, i.e. IDLE
        self.ButtonQuit.grid(column=2, row=1, padx=5)

    def download_file(self):
        """ 1. Need to know which data source is active
            2. Need to know the file to download
            3. Need to know the options settings for any post processing
                cm or m to ft
                project to appropriate utm"""
        HazusHazardInputPath = FHITSupport.GetHazusHazardInputPath()
        hazardInputType = self.controller.hazard_type_selection.get()
        FHITSupport.CreateHazardInputTypeFolder(HazusHazardInputPath, hazardInputType)
        download_path = FHITSupport.HazardFolderPath(HazusHazardInputPath, hazardInputType)

        datasource = self.controller.hazard_data_source_selection.get()
        file_name = self.controller.file_selection.get()

        if datasource == 'ADCIRC':
            year = self.controller.SearchParametersADCIRCFrame.yearSelection.get()
            weathertype = self.controller.SearchParametersADCIRCFrame.weathertypeSelection.get()
            storm_number = self.controller.SearchParametersADCIRCFrame.stormSelection.get()
            advisory = self.controller.SearchParametersADCIRCFrame.advisorySelection.get()
            key = self.controller.SearchParametersADCIRCFrame.adcircData.aws_functions.get_awskey_from_filename(year, weathertype, storm_number, advisory, file_name)
            self.controller.SearchParametersADCIRCFrame.adcircData.aws_functions.download_awss3_file(key, download_path)
            popup_download_complete = ctypes.windll.user32.MessageBoxW
            Thread(target=lambda :popup_download_complete(None, f'Downloaded: {key}', 'Download Complete', 0)).start()
        else:
            print('did nothing on download button press')

    def popup(self):
        '''Create a popup window'''
        popup_window = tk.Toplevel(self)
        popup_window.transient()
        tk.Label(popup_window, text="Please Wait...", font=(None, 36)).pack()
        self.update()
        popup_window.grab_set()
        return popup_window
    def make_popup(self):
        '''Create popup window while downloading the file'''
        wait_popup = self.popup()
        self.download_file()
        wait_popup.destroy()
    def button_download_command(self):
        '''Create a threaded popup window and downloading file'''
        return Thread(target=self.make_popup, daemon=True).start()

class Options(ttk.Frame):
    """Frame for setting options"""
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text='OPTIONS').grid(column=0, row=0, sticky='w')

        ttk.Label(self, text='Input Depth Unit:').grid(column=0, row=1, sticky='w')
        self.comboboxDepthUnit = ttk.Combobox(self)
        self.comboboxDepthUnit['values'] = ['TODO Depth Unit', 'Foot', 'Meter', 'Centimeter']
        self.comboboxDepthUnit.config(state='readonly')
        self.comboboxDepthUnit.current(0)
        #TODO get default value from config based on data source CWL
        self.comboboxDepthUnit.grid(column=1, row=1)

        #TODO clip to study region checkbox/button/wizard CWL

        #TODO checkbox to project? CWL
        #TODO config setting to project to UTM, will require determining projection of file CWL
        # and best UTM zone to project to CWL

        #TODO if file already exists, prompt to overwrite or not; could be config setting for default CWL
