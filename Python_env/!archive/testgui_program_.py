"""clindeman
python 3
"""

import tkinter as tk
import tkinter.ttk as ttk
import os
import json
from pathlib import Path

class GUI(tk.Tk):
    def __init__(self, *args):
        super().__init__()
        self.title("Flood Hazard Import Tool")
        self.iconbitmap('./images/ICO/24px.ico')
        self.__create_widgets()

    def __create_widgets(self):
        Left_ControlFrame = Left_Control(self)
        Left_ControlFrame.grid(column=0, row=0, sticky='ns', rowspan=3, padx=10, pady=10)
        ButtonsFrame = Buttons(self)
        ButtonsFrame.grid(column=1, row=2, sticky='nw', padx=10, pady=10)

class Left_Control(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()

    def __create_widgets(self):
        SelectHazardTypeSourceFrame = SelectHazardTypeSource(self)
        SelectHazardTypeSourceFrame.grid(column=0, row=0, sticky='nw', padx=10, pady=10)
        SearchParametersDefaultFrame = SearchParametersDefault(self)
        SearchParametersDefaultFrame.grid(column=0, row=1, sticky='nw', padx=10, pady=10)
        #TODO turn off default, enable source
        #SearchParametersADCIRCFrame = SearchParametersADCIRC(self)
        #SearchParametersADCIRCFrame.grid(column=0, row=2, sticky='nw', padx=10, pady=10)

class SelectHazardTypeSource(ttk.Frame):
    def __init__(self, container):
        super().__init__(container) #inherit from variable to reduce code
        self.hazard_types = self.__get_hazard_types()
        self.hazard_sources = ['']
        self.hazard_type_selection = tk.StringVar()
        self.hazard_data_source_selection = tk.StringVar()
        self.__create_widgets()
    
    def __create_widgets(self):
        self.LabelFrameHazardType = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelFrameHazardType.configure(text='SELECT A HAZARD TYPE')
        self.LabelFrameHazardType.grid(column=0, row=0, padx=10, pady=10, sticky='ew')

        self.comboboxHazardType = ttk.Combobox(self.LabelFrameHazardType)
        self.comboboxHazardType.configure(values=self.hazard_types)
        self.comboboxHazardType.config(state='readonly')
        self.comboboxHazardType.bind("<<ComboboxSelected>>", self.__handler_comboboxHazardType)
        self.comboboxHazardType.grid(column=0, row=1, padx=5, pady=5)

        self.LabelFrameHazardSource = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelFrameHazardSource.configure(text='SELECT A HAZARD SOURCE')
        self.LabelFrameHazardSource.grid(column=0, row=1, padx=10, pady=10, sticky='ew')

        self.comboboxHazardSource = ttk.Combobox(self.LabelFrameHazardSource)
        self.comboboxHazardSource.configure(values=self.hazard_sources)
        self.comboboxHazardSource.config(state='readonly')
        self.comboboxHazardSource.bind("<<ComboboxSelected>>", self.__handler_comboboxHazardSource)
        self.comboboxHazardSource.grid(column=0, row=4, padx=5, pady=5)

    def __get_hazard_types(self):
        """TODO runs at initialization"""
        with open(os.path.join(Path(__file__).parent, "config.json")) as f:
            config_json = json.load(f)
        return config_json['hazard_types']

    def __set_Hazard_Type_Selection(self, *args):
        self.hazard_type_selection.set(self.comboboxHazardType.get())
        print(self.hazard_type_selection.get())

    def __get_hazard_sources(self, hazard_type):
        source_list = []
        with open(os.path.join(Path(__file__).parent, "config.json")) as f:
            config_json = json.load(f)
            for hazard_source in config_json["data_sources"]:
                if hazard_type in hazard_source['hazard_types'] and hazard_source['enabled']:
                    source_list.append(hazard_source['name'])
        return source_list

    def __set_hazard_sources(self, *args):
        hazard_sources = self.__get_hazard_sources(self.hazard_type_selection.get())
        self.comboboxHazardSource.config(values=hazard_sources)
        print(hazard_sources)

    def __clear_hazard_sources(self, *args):
        self.comboboxHazardSource.set('')

    def __clear_hazard_data_source_selection(self, *args):
        self.hazard_data_source_selection.set('')

    def __handler_comboboxHazardType(self, *args):
        self.__clear_hazard_data_source_selection()
        self.__clear_hazard_sources()
        self.__set_Hazard_Type_Selection()
        self.__set_hazard_sources()

    def __set_Hazard_Source_Selection(self, *args):
        self.hazard_data_source_selection.set(self.comboboxHazardSource.get())
        print(self.hazard_data_source_selection.get())

    def __hide_frame(self, *args):
        SearchParametersDefaultFrame.grid_remove()

    def __handler_comboboxHazardSource(self, *args):
        self.__set_Hazard_Source_Selection()
        self.__hide_frame() #remove default search params
        #show source frame search params
        #remove source frame search params
        #load default search params
        #clear file list
        #clear file properties

class SearchParametersDefault(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()

    def __create_widgets(self):
        self.LabelframeSearchParameters = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelframeSearchParameters.configure(text='''SELECT FLOOD HAZARD SEARCH PARAMETERS :''')
        self.LabelframeSearchParameters.grid(column=0, row=0, padx=10, pady=10)

        ttk.Label(self.LabelframeSearchParameters, text='Choose a Hazard Type and Hazard Source').grid(column=0, row=0, padx=5, pady=5, sticky='w')

class SearchParametersADCIRC(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0)
        self.__create_widgets()
        
    def __create_widgets(self):
        self.LabelframeSearchParameters = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelframeSearchParameters.configure(text='''SELECT FLOOD HAZARD SEARCH PARAMETERS :''')
        self.LabelframeSearchParameters.grid(column=0, row=0, padx=10, pady=10)

        ttk.Label(self.LabelframeSearchParameters, text='Year:').grid(column=0, row=1, sticky=tk.W)
        self.comboboxYear = ttk.Combobox(self.LabelframeSearchParameters,)
        self.comboboxYear['values'] = ['TODO year', '2020', '2021']
        self.comboboxYear.config(state='readonly')
        self.comboboxYear.current(0)
        self.comboboxYear.grid(column=1, row=1, sticky='ew', padx=5, pady=5)
        ttk.Label(self.LabelframeSearchParameters, text='Weather Type:').grid(column=0, row=2, sticky=tk.W)
        self.comboboxWeatherType = ttk.Combobox(self.LabelframeSearchParameters,)
        self.comboboxWeatherType['values'] = ['TODO weather type', 'Synoptic', 'Tropical']
        self.comboboxWeatherType.config(state='readonly')
        self.comboboxWeatherType.current(0)
        self.comboboxWeatherType.grid(column=1, row=2, sticky='ew', padx=5, pady=5)
        ttk.Label(self.LabelframeSearchParameters, text='Storm:').grid(column=0, row=3, sticky='w')
        self.comboboxStorm = ttk.Combobox(self.LabelframeSearchParameters,)
        self.comboboxStorm['values'] = ['TODO storm', 'Storm1', 'Storm2']
        self.comboboxStorm.config(state='readonly')
        self.comboboxStorm.current(0)
        self.comboboxStorm.grid(column=1, row=3, sticky='ew', padx=5, pady=5)
        ttk.Label(self.LabelframeSearchParameters, text='Advisory:').grid(column=0, row=4, sticky='w')
        self.comboboxAdvisory = ttk.Combobox(self.LabelframeSearchParameters,)
        self.comboboxAdvisory['values'] = ['TODO advisory', '1', '2', '3']
        self.comboboxAdvisory.config(state='readonly')
        self.comboboxAdvisory.current(0)
        self.comboboxAdvisory.grid(column=1, row=4, sticky='ew', padx=5, pady=5)



class Buttons(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()

    def __create_widgets(self):
        self.buttonDownloadImport = ttk.Button(self, text="Download and Import Selected File").grid(column=0, row=1, padx=5)
        self.buttonBrowseImport = ttk.Button(self, text="Browse for Existing Hazard Data to Import").grid(column=1, row=1, padx=5)
        self.buttonQuit = ttk.Button(self, text="Quit")
        self.buttonQuit.configure(command=self.quit)#will quit Tcl interpreter, i.e. IDLE
        self.buttonQuit.grid(column=2, row=1, padx=5)

def vp_start_gui():
    root = myApp()
    root.mainloop()

if __name__ == "__main__":
    vp_start_gui()

