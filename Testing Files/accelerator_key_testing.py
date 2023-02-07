from tkinter import *

def donothing(event=None):
   filewin = Toplevel(root)
   button = Button(filewin, text="Cool")
   button.pack()

root = Tk()
menubar = Menu(root)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index",accelerator="Ctrl+H", command=donothing)
menubar.add_cascade(label="Help",underline=1, menu=helpmenu)
root.config(menu=menubar)
root.bind_all("<Control-h>", donothing)
root.mainloop()