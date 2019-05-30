# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 12:40:55 2018

@author: Lenovo
"""

from tkinter import *
root=Tk()
top=Toplevel(root)
lab1=Label(root,text="root")
lab2=Label(top,text="top")
lab1.pack()
lab2.pack()
root.mainloop()