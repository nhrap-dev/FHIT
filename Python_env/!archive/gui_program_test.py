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
#TODO check if internet is available
#TODO check if data source website is available
'''

try:
    import Tkinter as tk #python 2
except ImportError:
    import tkinter as tk #python 3

try:
    import ttk #python 2
except ImportError:
    import tkinter.ttk as ttk #python 3

class SelectHazardTypeSource(ttk.Frame):
    def __init__(self, container):
        super().__init__(container) #inherit from variable to reduce code
        self.columnconfigure(0)
        self.__create_widgets()
    
    def __create_widgets(self):
        self.LabelFrameHazardType = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelFrameHazardType.configure(text='SELECT A HAZARD TYPE')
        self.LabelFrameHazardType.grid(column=0, row=0, padx=10, pady=10, sticky='ew')

        self.comboboxHazardType = ttk.Combobox(self.LabelFrameHazardType)
        #TODO read available types from config
        self.comboboxHazardType['values'] = ['TODO harzard type', 'Riverine', 'Coastal', 'Storm Surge']
        self.comboboxHazardType.config(state='readonly')
        self.comboboxHazardType.current(0)
        self.comboboxHazardType.grid(column=0, row=1, padx=5, pady=5)

        self.LabelFrameHazardSource = tk.LabelFrame(self, font=("Tahoma", "12"), labelanchor='n', borderwidth=2)
        self.LabelFrameHazardSource.configure(text='SELECT A HAZARD SOURCE')
        self.LabelFrameHazardSource.grid(column=0, row=1, padx=10, pady=10, sticky='ew')

        self.comboboxHazardSource = ttk.Combobox(self.LabelFrameHazardSource)
        #TODO adjust values based on chosen hazard type, from config
        self.comboboxHazardSource['values'] = ['TODO hazard source', 'ADCIRC', 'SLOSH']
        self.comboboxHazardSource.config(state='readonly')
        self.comboboxHazardSource.current(0)
        self.comboboxHazardSource.grid(column=0, row=4, padx=5, pady=5)

class SearchParametersDefault(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text='SELECT FLOOD HAZARD SEARCH PARAMETERS').grid(column=0, row=0, sticky='w', columnspan=2)
        ttk.Label(self, text='Choose a Hazard Type and Hazard Source').grid(column=0, row=1, sticky=tk.W)

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

class SelectFileList(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text='SELECT FROM AVAILABLE FILES :').grid(column=0, row=0, sticky='w')
        self.treeviewFiles = ttk.Treeview(self, columns=(1), show='headings')
        self.treeviewFiles.grid(column=0, row=1, sticky='ew')
        self.treeviewFiles.heading(1, text='FILE', anchor='w')

        self.scrollbarFiles = tk.Scrollbar(self)
        self.scrollbarFiles.grid(column=1, row=1, sticky='nsew')
        self.treeviewFiles.config(yscrollcommand=self.scrollbarFiles.set)
        self.scrollbarFiles.config(command=self.treeviewFiles.yview)


class SelectFileProperties(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text='SELECTED FILE PROPERTIES :').grid(column=0, row=0, sticky='w')
        self.treeviewFileProperties = ttk.Treeview(self, columns=(1,2), show='headings')
        self.treeviewFileProperties.grid(column=0, row=1, sticky='ew')
        self.treeviewFileProperties.heading(1, text='PROPERTY')
        self.treeviewFileProperties.heading(2, text='VALUE')

        self.scrollbarFileProperties = tk.Scrollbar(self)
        self.scrollbarFileProperties.grid(column=1, row=1, sticky='ns')
        self.treeviewFileProperties.config(yscrollcommand=self.scrollbarFileProperties.set)
        self.scrollbarFileProperties.config(command=self.treeviewFileProperties.yview)

class Options(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text='OPTIONS :').grid(column=0, row=0, sticky='w')

        ttk.Label(self, text='Input Depth Unit:').grid(column=0, row=1, sticky='w')
        self.comboboxDepthUnit = ttk.Combobox(self)
        self.comboboxDepthUnit['values'] = ['TODO Depth Unit', 'Foot', 'Meter', 'Centimeter']
        self.comboboxDepthUnit.config(state='readonly')
        self.comboboxDepthUnit.current(0)
        #TODO get default value from config based on data source
        self.comboboxDepthUnit.grid(column=1, row=1)

        #TODO clip to study region checkbox/button/wizard

        #TODO checkbox to project?
        #TODO config setting to project to UTM, will require determining projection of file
        # and best UTM zone to project to

        #TODO if file already exists, prompt to overwrite or not; could be config setting for default

class Buttons(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0)
        self.__create_widgets()

    def __create_widgets(self):
        #ttk.Label(self, text='BUTTONS').grid(column=0, row=0, sticky='w')
        #spacer = ttk.Label(self, text='')
        #spacer.grid(column=0, row=0)

        self.buttonDownloadImport = ttk.Button(self, text="Download and Import Selected File").grid(column=0, row=1, padx=5)
        self.buttonBrowseImport = ttk.Button(self, text="Browse for Existing Hazard Data to Import").grid(column=1, row=1, padx=5)
        self.buttonQuit = ttk.Button(self, text="Quit")
        self.buttonQuit.configure(command=root.destroy)
        self.buttonQuit.grid(column=2, row=1, padx=5)

class Left_Control(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0)
        self.__create_widgets()

    def __create_widgets(self):
        SelectHazardTypeSourceFrame = SelectHazardTypeSource(self)
        SelectHazardTypeSourceFrame.grid(column=0, row=0, sticky='nw', padx=10, pady=10)

        SearchParametersADCIRCFrame = SearchParametersADCIRC(self)
        SearchParametersADCIRCFrame.grid(column=0, row=1, sticky='nw', padx=10, pady=10)

class MyApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs) #initialize the inherited class
        parent.title("Flood Hazard Import Tool")
        parent.iconbitmap('./images/ICO/24px.ico') 
        self.__create_widgets()

    def __create_widgets(self):
        Left_ControlFrame = Left_Control(self)
        Left_ControlFrame.grid(column=0, row=0, sticky='ns', rowspan=3, padx=10, pady=10)
        OptionsFrame = Options(self)
        OptionsFrame.grid(column=0, row=1, sticky='sw', padx=20, pady=20)
        SelectFileListFrame = SelectFileList(self)
        SelectFileListFrame.grid(column=1, row=0, sticky='new', padx=10, pady=10)
        SelectFilePropertiesFrame = SelectFileProperties(self)
        SelectFilePropertiesFrame.grid(column=1, row=1, sticky='new', padx=10, pady=10)
        ButtonsFrame = Buttons(self)
        ButtonsFrame.grid(column=1, row=2, sticky='nw', padx=10, pady=10)


def vp_start_gui():
    global root
    root = tk.Tk()
    MyApp(root).pack()
    root.mainloop()

if __name__ == "__main__":
    vp_start_gui()

