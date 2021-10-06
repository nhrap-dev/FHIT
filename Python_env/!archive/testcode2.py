from tkinter import Frame,Button,Tk

class Manager(object):
    def __init__(self, gui):
        self.gui = gui
        self.gui.lower_btn.manager = self

    def onClick(self):
        self.gui.upper_btn2.configure(text="changed text")

class GUI(Frame):
    def __init__(self, root):

        Frame.__init__(self,root)

        self.upper_frame=Frame(root)
        self.upper_frame.pack()

        self.lower_frame=Frame(root)
        self.lower_frame.pack()

        self.upper_btn1 = Button(self.upper_frame, text="upper button 1")
        self.upper_btn2 = Button(self.upper_frame, text="upper button 2")
        self.upper_btn1.grid(row=0,column=0)
        self.upper_btn2.grid(row=0,column=1)

        self.lower_btn = CustomButton(self.lower_frame, "lower button 3")
        self.lower_btn.pack()

class CustomButton(Button):
    def __init__(self,master,text):
        Button.__init__(self,master,text=text)

        self.configure(command=self.onClick)
        self.manager = None

    def onClick(self):
        if self.manager:
            self.manager.onClick()
        else:
            print("here I want to change the text of upper button 1")  

root = Tk()
my_gui = GUI(root)
Manager(my_gui)
root.mainloop()