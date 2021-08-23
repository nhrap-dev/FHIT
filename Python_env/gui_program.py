"""clindeman
python 3
"""

import tkinter as tk
import tkinter.ttk as ttk
import views as views

class MyApplication(tk.Tk):
    """Main Application/Root window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("Flood Hazard Import Tool")
        self.iconbitmap('./images/ICO/24px.ico')
        self.resizable(width=False, height=False)

        # define the GUI/View
        views.GUI(self).grid(sticky='nsew')
        self.columnconfigure(0, weight=1) #fill in the space

if __name__ == "__main__":
    #TODO break this out into a script of its own
    app = MyApplication()
    app.mainloop()
