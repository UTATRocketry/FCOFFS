
from tkinter import messagebox

def gui_error(msg: str) -> None:
    '''Causes error pop up window with the provided message'''
    messagebox.showerror(title="Program Error", message=msg)

def gui_popup(msg:str) -> None:
    '''Creates window pop up with given message'''
    messagebox.showinfo(title="Program Info", message=msg)
