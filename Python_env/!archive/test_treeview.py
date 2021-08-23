from tkinter import *
from tkinter import ttk

ws = Tk()
ws.title('Treeview Test')

frame = Frame(ws)
frame.pack(pady=20)

tv = ttk.Treeview(frame, columns=(1,2), show='headings')
tv.pack(side=LEFT)

tv.heading(1, text='PROPERTIES')
tv.heading(2, text='VALUE')

sb = Scrollbar(frame, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

tv.config(yscrollcommand=sb.set)
sb.config(command=tv.yview)

dictionary = {'DateTime':'al04'
            ,'Advisory':'30'
            ,'ADCIRC variable':'inunmax'
            ,'Abbreviated ADCIRC grid name':'EGOMv20b'
            ,'Wind Model':'GAHM'
            ,'Wave Model':None
            ,'Ensemble Member Name':'nhcConsensus'
            ,'Operator':'estrabd'
            ,'Machine':'frontera'
            ,'Other':None
            ,'Resolution':'50'
            ,'Upper Left Longitude (Degrees)':'-84.0'
            ,'Upper Left Latitude (Degrees)':'30.5'
            ,'Number of Cells in Longitude':'6000'
            ,'Number of Cells in Latitude':'10000'}

def load_data():
    counter = 0
    for key, value in dictionary.items():
        tv.insert(parent='', index=counter, iid=counter, text='', values=(key, value))
        counter +=1

def clear_data():
    tv.delete(*tv.get_children())

loadButton = ttk.Button(text="Load Data", command=load_data)
loadButton.pack()

clearButton = ttk.Button(text="Clear Data", command=clear_data)
clearButton.pack()

ws.mainloop()